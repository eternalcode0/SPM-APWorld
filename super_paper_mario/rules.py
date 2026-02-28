"""All things that define logical access between regions and locations"""

import typing
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

from BaseClasses import CollectionState
from entrance_rando import (
    Entrance,
    EntranceType,
    ERPlacementState,
    bake_target_group_lookup,
    disconnect_entrance_for_randomization,
)
from entrance_rando import randomize_entrances as er_randomize_entrances
from Options import Toggle
from rule_builder.rules import False_, Has, HasAll, HasAny, HasGroupUnique, OptionFilter, Rule, True_

from .data import GAME
from .names import EventName as E
from .names import ItemName as I
from .names import LocationName as L
from .names import RegionName as R
from .options import (
    ChapterDoorAccess,
    EntranceRando,
    FlipsidePitAccess,
    FlopsidePitAccess,
    ObscureTricks,
    ShuffleAbilities,
)

if typing.TYPE_CHECKING:
    from . import SuperPaperMarioWorld


class EGroup(IntEnum):
    """An Entrance Group for entrance_rando"""

    NONE = 0
    # Transportation
    PIPE = 1
    DOOR = 2
    ELEVATOR_UP = 3
    ELEVATOR_DOWN = 4
    PORTAL = 5  # Chapter 4 Space Wormholes
    JUMP = 6
    FALL = 7
    # Chapter
    HUB = 1 << 3
    CHAP_1 = 2 << 3
    CHAP_2 = 3 << 3
    CHAP_3 = 4 << 3
    CHAP_4 = 5 << 3
    CHAP_5 = 6 << 3
    CHAP_6 = 7 << 3
    CHAP_7 = 8 << 3
    CHAP_8 = 9 << 3
    # Bitmasks
    TRANSPORTATION_MASK = 0b00_0111
    CHAPTER_MASK = 0b111_1000


transportation_matching_group_lookup = {
    EGroup.DOOR: [EGroup.DOOR, EGroup.PORTAL],
    EGroup.PIPE: [EGroup.PIPE],
    EGroup.ELEVATOR_UP: [EGroup.ELEVATOR_DOWN],
    EGroup.ELEVATOR_DOWN: [EGroup.ELEVATOR_UP],
    EGroup.PORTAL: [EGroup.PORTAL, EGroup.DOOR],
    EGroup.JUMP: [EGroup.FALL],
    EGroup.FALL: [EGroup.JUMP],
}


def get_target_groups(group: int) -> list[int]:
    """Return the list of applicable destination entrances by their EGroup. Intended to be used with
    `bake_target_er_lookup`"""
    # Transportation must match the transportation dictionary values
    # Chapter must match
    transportation = group & EGroup.TRANSPORTATION_MASK
    chapter = group & EGroup.CHAPTER_MASK
    return [pair | chapter for pair in transportation_matching_group_lookup[transportation]]


@dataclass
class EntranceRule:
    fr: R
    to: R
    rule: Callable[[CollectionState], bool] | typing.Any | None = None
    name: str | None = None
    group: EGroup = EGroup.NONE
    etype: EntranceType = EntranceType.TWO_WAY


@dataclass
class LocationRule:
    loc: L
    rule: Callable[[CollectionState], bool] | typing.Any | None = None


fr = "fr"
to = "to"
rule = "rule"
name = "name"
group = "group"
etype = "etype"

loc = "loc"


@dataclass
class HasChapterKey(Rule["SuperPaperMarioWorld"], game=GAME):
    chapter_key: I
    subchapter_key: I

    def _instantiate(self, world: "SuperPaperMarioWorld") -> Rule.Resolved:
        # if world.options.chapter_door_access == ChapterDoorAccess.option_subchapters_locked:
        #     return Has(self.chapter_key.value).resolve(world)
        # if world.options.chapter_door_access == ChapterDoorAccess.option_chapter_locked:
        #     return Has(self.subchapter_key.value).resolve(world)
        if world.options.chapter_door_access == ChapterDoorAccess.option_open:
            return True_().resolve(world)
        raise NotImplementedError(f"Unknown chapter_door_access option: {world.options.chapter_door_access}")


@dataclass
class CanFleepTreasureSpot(Rule["SuperPaperMarioWorld"], game=GAME):
    map: I

    def _instantiate(self, world: "SuperPaperMarioWorld") -> Rule.Resolved:
        if world.options.treasure_maps.treasures_open:
            return Has(I.PIXL_FLEEP).resolve(world)
        if world.options.treasure_maps.treasures_standard:
            return HasAll(I.PIXL_FLEEP, self.map).resolve(world)
        if world.options.treasure_maps.treasures_disabled:
            return False_().resolve(world)
        raise NotImplementedError(f"Unknown treasure maps option: {world.options.treasure_maps}")


class RuleHolder:
    """Accessibility container for common Rules & Filers"""

    # OptionFilters
    shuffle_ability_filter = OptionFilter(ShuffleAbilities, Toggle.option_true)
    flipside_pit_access_filter = OptionFilter(FlipsidePitAccess, FlipsidePitAccess.option_closed, operator="ne")

    # Base Rules
    can_flip = Has(I.CHARACTER_MARIO) & (
        Has(I.ABILITY_FLIP, options=[shuffle_ability_filter], filtered_resolution=True)
    )
    can_float = Has(I.CHARACTER_PEACH) & (
        Has(I.ABILITY_UMBRELLA, options=[shuffle_ability_filter], filtered_resolution=True)
    )
    can_fire = Has(I.CHARACTER_BOWSER) & (
        Has(I.ABILITY_FIRE, options=[shuffle_ability_filter], filtered_resolution=True)
    )
    can_super_jump = Has(I.CHARACTER_LUIGI) & (
        Has(I.ABILITY_SUPER_JUMP, options=[shuffle_ability_filter], filtered_resolution=True)
    )
    can_break_hard_blocks = HasAny(I.PIXL_BOOMER, I.PIXL_CUDGE, I.PIXL_THUDLEY) | can_fire

    # chapter 2 rules
    mi110_door_group = (
        # Luigi jumps to the doors without touching the blocks
        can_super_jump
        |
        # Bowser builds up speed on carrie and jumps at the blocks while breathing fire
        (can_fire & Has(I.PIXL_CARRIE))
        |
        # Bowser too big to cudge the blocks
        (HasAny(I.CHARACTER_LUIGI, I.CHARACTER_MARIO, I.CHARACTER_PEACH) & Has(I.PIXL_CUDGE))
        |
        # The normal way to break the blocks
        Has(I.PIXL_BOOMER)
    )


def connect_regions(world: "SuperPaperMarioWorld") -> list[Entrance]:
    """Connects all the regions together with the appropriate rules.
    Returns the list of entrances that can be randomized.
    """

    def create_entrance(
        world: "SuperPaperMarioWorld",
        from_region: R,
        to_region: R,
        rule: typing.Callable[[CollectionState], bool] | Rule[typing.Any] | None = None,
        name: str | None = None,
        group: int = 0,
        type: EntranceType = EntranceType.TWO_WAY,
        force_creation: bool = False,
    ) -> Entrance | None:
        if from_region not in world.rm or to_region not in world.rm:
            return None
        entrance = world.create_entrance(world.rm[from_region], world.rm[to_region], rule, name, force_creation)
        if entrance is not None:
            entrance.randomization_group = group
            entrance.randomization_type = type
        return entrance

    all_entrances = [
        create_entrance(world, edata.fr, edata.to, edata.rule, edata.name, edata.group, edata.etype)
        for edata in ENTRANCE_DATA
    ]
    return [
        entrance
        for entrance in all_entrances
        if entrance is not None
        and entrance.randomization_group > 0
        and entrance.randomization_type == EntranceType.TWO_WAY
    ]


def randomize_entrances(world: "SuperPaperMarioWorld", entrances: list[Entrance]) -> ERPlacementState:
    _ = [disconnect_entrance_for_randomization(entrance) for entrance in entrances]
    target_group_lookup = bake_target_group_lookup(world, get_target_groups)
    return er_randomize_entrances(
        world, world.options.randomize_entrances.value == EntranceRando.option_coupled, target_group_lookup, True
    )


def set_rules(world: "SuperPaperMarioWorld") -> None:
    world.set_completion_rule(Has(E.VICTORY))

    _ = [
        world.set_rule(world.lm[ldata.loc], ldata.rule)
        for ldata in LOCATION_DATA
        if ldata.loc in world.lm and ldata.rule
    ]


CHAPTER_DOOR_ER = {group: EGroup.HUB | EGroup.DOOR, etype: EntranceType.ONE_WAY}


ENTRANCE_RULES = [
    #region Chapter Doors
    { fr: R.MAC02_L_TOWER
    , to: R.HE101
    , rule: HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_1_KEY)
    , name: "Flipside Tower - Red Door [1-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.HE201
    , rule: HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_2_KEY)
    , name: "Flipside Tower - Red Door [1-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.HE301
    , rule: HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_3_KEY)
    , name: "Flipside Tower - Red Door [1-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.HE401
    , rule: HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_4_KEY)
    , name: "Flipside Tower - Red Door [1-4]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.MI101
    , rule: HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_1_KEY)
    , name: "Flipside Tower - Orange Door [2-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.MI201
    , rule: HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_2_KEY)
    , name: "Flipside Tower - Orange Door [2-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.MI301
    , rule: HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_3_KEY)
    , name: "Flipside Tower - Orange Door [2-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.MI401
    , rule: HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_4_KEY)
    , name: "Flipside Tower - Orange Door [2-4]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.TA101
    , rule: HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_1_KEY)
    , name: "Flipside Tower - Yellow Door [3-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.TA201
    , rule: HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_2_KEY)
    , name: "Flipside Tower - Yellow Door [3-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.TA301
    , rule: HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_3_KEY)
    , name: "Flipside Tower - Yellow Door [3-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.TA401
    , rule: HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_4_KEY)
    , name: "Flipside Tower - Yellow Door [3-4]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.SP101
    , rule: HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_1_KEY)
    , name: "Flipside Tower - Green Door [4-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.SP201
    , rule: HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_2_KEY)
    , name: "Flipside Tower - Green Door [4-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.SP301
    , rule: HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_3_KEY)
    , name: "Flipside Tower - Green Door [4-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.SP401
    , rule: HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_4_KEY)
    , name: "Flipside Tower - Green Door [4-4]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.GN101
    , rule: HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_1_KEY)
    , name: "Flipside Tower - Cyan Door [5-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.GN201
    , rule: HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_2_KEY)
    , name: "Flipside Tower - Cyan Door [5-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.GN301
    , rule: HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_3_KEY)
    , name: "Flipside Tower - Cyan Door [5-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.GN401
    , rule: HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_4_KEY)
    , name: "Flipside Tower - Cyan Door [5-4]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.WA101
    , rule: HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_1_KEY)
    , name: "Flipside Tower - Blue Door [6-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.WA201
    , rule: HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_2_KEY)
    , name: "Flipside Tower - Blue Door [6-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.WA301
    , rule: HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_3_KEY)
    , name: "Flipside Tower - Blue Door [6-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.WA401
    , rule: HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_4_KEY)
    , name: "Flipside Tower - Blue Door [6-4]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.AN101
    , rule: HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_1_KEY)
    , name: "Flipside Tower - Black Door [7-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.AN201
    , rule: HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_2_KEY)
    , name: "Flipside Tower - Black Door [7-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.AN301
    , rule: HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_3_KEY)
    , name: "Flipside Tower - Black Door [7-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC02_L_TOWER
    , to: R.AN401
    , rule: HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_4_KEY)
    , name: "Flipside Tower - Black Door [7-4]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC12_L_TOWER
    , to: R.LS101
    # TODO: use the new attribute field resolvers once they're merged
    # otherwise grabbing the pure_hearts_required setting from here is a pain
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_1_KEY) & HasGroupUnique("Pure Heart", 8)
    , name: "Flopside Tower - Black Door [8-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC12_L_TOWER
    , to: R.LS201
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_2_KEY) & HasGroupUnique("Pure Heart", 8)
    , name: "Flopside Tower - Black Door [8-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC12_L_TOWER
    , to: R.LS301
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_3_KEY) & HasGroupUnique("Pure Heart", 8)
    , name: "Flopside Tower - Black Door [8-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC12_L_TOWER
    , to: R.LS401
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_4_KEY) & HasGroupUnique("Pure Heart", 8)
    , name: "Flopside Tower - Black Door [8-4]"
    , **CHAPTER_DOOR_ER
    },
    #endregion
    #region Flipside
    { fr: R.MAC02_L_TOWER
    , to: R.MAC01_LAYER1
    , name: "Flipside Tower - Fall"
    , group: EGroup.HUB | EGroup.FALL
    , etype: EntranceType.ONE_WAY
    },
    { fr: R.MAC02_L_TOWER
    , to: R.MAC02_LAYER1
    , name: "Flipside Tower - Elevator Down"
    },
    { fr: R.MAC01_LAYER1
    , to: R.MAC02_LAYER1
    , name: "Flipside 3F - Layer 1 - Elevator Down"
    , group: EGroup.ELEVATOR_DOWN | EGroup.HUB
    },
    { fr: R.MAC01_LAYER2
    , to: R.MAC02_LAYER2
    , name: "Flipside 3F - Layer 2 - Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC02_LAYER1
    , to: R.MAC02_L_TOWER
    , name: "Flipside Tower - Elevator Up"
    },
    { fr: R.MAC02_LAYER1
    , to: R.MAC09_LAYER3
    , name: "Flipside 2F - Layer 1 - Elevator Down"
    # MOD: This elevator doesn't work until GSW(0, 53), after chapter 1-4 cleared, before intermission
    , rule: True_()
    , group: EGroup.ELEVATOR_DOWN | EGroup.HUB
    },
    { fr: R.MAC02_LAYER1
    , to: R.MAC01_LAYER1
    , name: "Flipside 2F - Layer 1 - Elevator Up"
    # TODO: Figure out why this entrance in particular screws over ER. Probably too few possible placements?
    # , group: EGroup.ELEVATOR_UP | EGroup.HUB
    },
    { fr: R.MAC02_LAYER1
    , to: R.MAC05_LAYER1
    , rule: RuleHolder.can_flip
    , name: "Flipside 2F - Layer 1 - Left Blue Pipe"
    },
    { fr: R.MAC02_LAYER1
    , to: R.MAC12_LAYER1
    , name: "Flipside 2F - Layer 1 - Right Blue Pipe"
    },
    { fr: R.MAC02_LAYER1
    , to: R.MAC02_LAYER2
    , rule: RuleHolder.can_flip & Has(I.OLD_KEY)
    , name: "Flipside 2F - Layer 1 -> 2"
    },
    { fr: R.MAC02_LAYER2
    , to: R.MAC01_LAYER2
    , rule: RuleHolder.can_break_hard_blocks
    , name: "Flipside 2F - Layer 2 - Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC02_LAYER2
    , to: R.MAC02_LAYER3
    , rule: RuleHolder.can_flip
    , name: "Flipside 2F - Layer 2 -> 3"
    },
    { fr: R.MAC02_LAYER3
    , to: R.MAC06_LAYER1
    , name: "Flipside 2F Outskirts - Layer 3 - Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC02_LAYER3
    , to: R.MAC02_LAYER2
    , rule: RuleHolder.can_flip
    , name: "Flipside 2F - Layer 3 -> 2"
    },
    { fr: R.MAC03_LAYER1
    , to: R.MAC09_LAYER1
    , name: "Flipside 1F - Mirror Hall - Right Door"
    , group: EGroup.DOOR | EGroup.HUB
    },
    { fr: R.MAC03_LAYER1
    , to: R.MAC03_LAYER2
    , rule: RuleHolder.can_flip
    , name: "Flipside 1F - Mirror Hall - Layer 1 -> 2"
    },
    { fr: R.MAC04_LAYER1
    , to: R.MAC04_ITTY_BITS
    , rule: Has(I.PIXL_DOTTIE)
    , name: "Flipside B1 - Shrink to Itty Bits"
    },
    { fr: R.MAC04_LAYER1
    , to: R.MAC04_BAR
    , rule: RuleHolder.can_flip
    , name: "Flipside B1 - Flip to Bar's backrooms"
    },
    { fr: R.MAC04_BAR
    , to: R.MAC30
    , name: "Flipside B1 - Bar's backroom pipe"
    },
    { fr: R.MAC05_LAYER1
    , to: R.MAC04_LAYER1
    , name: "Flipside B2 - Layer 1 - Elevator Up"
    },
    { fr: R.MAC05_LAYER1
    , to: R.MAC02_LAYER1
    , rule: RuleHolder.can_flip
    , name: "Flipside B2 - Layer 1 - Blue Pipe"
    },
    { fr: R.MAC05_LAYER1
    , to: R.L_FLIPSIDE_PIT
    # TODO: more access logic for individual floors
    , rule: Has(E.SWITCH_FLIPSIDE_PIT_CAGE, options=[RuleHolder.flipside_pit_access_filter])
    , name: "Flipside B2 - Layer 1 - Sealed Pipe"
    },
    { fr: R.MAC05_LAYER1
    , to: R.L_FLIPSIDE_PIT_TOP
    , rule: RuleHolder.can_super_jump | Has(E.SWITCH_FLIPSIDE_PIT_CAGE)
    , name: "Flipside B2 - Layer 1 -> Cage"
    },
    { fr: R.L_FLIPSIDE_PIT_TOP
    , to: R.MAC05_LAYER2
    , rule: RuleHolder.can_flip
    , name: "Flipside B2 - Layer 1 Cage -> 2"
    },
    { fr: R.MAC05_LAYER2
    , to: R.L_FLIPSIDE_PIT_TOP
    , rule: HasAll(I.CHARACTER_MARIO, I.PIXL_TIPPI)
    , name: "Flipside B2 Outskirts - Layer 2 -> 1 Cage"
    },
    { fr: R.MAC05_LAYER2
    , to: R.MAC07_LAYER2
    , name: "Flipside B2 Outskirts - Layer 2 - Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC06_LAYER1
    , to: R.MAC02_LAYER3
    , name: "Flipside 1F Outskirts - Layer 1 - Right Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC06_LAYER1
    , to: R.MAC07_LAYER2
    # Bowser *barely* has enough room to stand to break the blocks
    , rule: RuleHolder.can_break_hard_blocks
    , name: "Flipside 1F Outskirts - Layer 1 - Left Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC06_LAYER1
    , to: R.MAC08
    , name: "Flipside 1F Outskirts - Layer 1 - Chasm Fall"
    },
    { fr: R.MAC06_LAYER1
    , to: R.MAC06_LAYER2
    , rule: RuleHolder.can_flip
    , name: "Flipside 1F Outskirts - Layer 1 -> 2"
    },
    { fr: R.MAC06_LAYER2
    , to: R.MAC06_LAYER1
    , rule: RuleHolder.can_flip
    , name: "Flipside 1F Outskirts - Layer 2 -> 1"
    },
    { fr: R.MAC07_LAYER2
    , to: R.MAC05_LAYER2
    , name: "Flipside B1 Outskirts - Layer 1 - Right Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC07_LAYER2
    , to: R.MAC06_LAYER1
    , name: "Flipside B1 Outskirts - Layer 1 - Left Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC07_LAYER2
    , to: R.MAC07_LAYER1
    , rule: RuleHolder.can_flip & Has(E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK)
    , name: "Flipside B1 Outskirts - Layer 2 -> 1"
    },
    { fr: R.MAC08
    , to: R.MAC06_LAYER1
    , name: "Flipside 1F - Jump Out"
    },
    { fr: R.MAC09_LAYER1
    , to: R.MAC03_LAYER1
    , name: "Flipside 1F - Door"
    , group: EGroup.HUB | EGroup.DOOR
    },
    { fr: R.MAC09_LAYER1
    , to: R.MAC09_LAYER2
    # Standing outside Mirror Hall, you don't need Fleep. You just walk thru the wall
    , rule: RuleHolder.can_flip
    , name: "Flipside 1F - Layer 1 -> 2"
    },
    { fr: R.MAC09_LAYER2
    , to: R.MAC09_LAYER1
    , rule: Has(I.PIXL_FLEEP) & RuleHolder.can_flip
    , name: "Flipside 1F - Layer 2 -> 1"
    },
    { fr: R.MAC09_LAYER2
    , to: R.MAC09_LAYER3
    , rule: Has(I.PIXL_BOOMER) & RuleHolder.can_flip
    , name: "Flipside 1F - Layer 2 -> 3"
    },
    { fr: R.MAC09_LAYER3
    , to: R.MAC02_LAYER1
    , name: "Flipside 1F - Elevator Up"
    , group: EGroup.ELEVATOR_UP | EGroup.HUB
    },
    { fr: R.MAC09_LAYER3
    , to: R.MAC04_LAYER1
    # MOD: This elevator only works starting at GSW(0, 73), getting boomer
    , rule: True_()
    , name: "Flipside 1F - Elevator Down"
    , group: EGroup.ELEVATOR_DOWN | EGroup.HUB
    },
    { fr: R.MAC09_LAYER3
    , to: R.MAC09_LAYER2
    , rule: Has(I.PIXL_BOOMER) & RuleHolder.can_flip
    , name: "Flipside 1F - Layer 3 -> 2"
    },
    #endregion
    #region Flopside
    { fr: R.MAC12_L_TOWER
    , to: R.MAC11_LAYER1
    , name: "Flopside Tower - Fall"
    , etype: EntranceType.ONE_WAY
    },
    { fr: R.MAC12_L_TOWER
    , to: R.MAC12_LAYER1
    , name: "Flopside Tower - Elevator Down"
    },
    { fr: R.MAC11_LAYER1
    , to: R.MAC12_LAYER1
    , name: "Flopside 3F - Layer 1 - Elevator Down"
    },
    { fr: R.MAC11_LAYER2
    , to: R.MAC12_LAYER2
    , name: "Flopside 3F - Layer 2 - Right Pipe"
    },
    { fr: R.MAC12_LAYER1
    , to: R.MAC12_L_TOWER
    , name: "Flopside Tower - Elevator Up"
    },
    { fr: R.MAC12_LAYER1
    , to: R.MAC11_LAYER1
    , name: "Flopside 2F - Layer 1 - Elevator Up"
    , group: EGroup.ELEVATOR_UP | EGroup.HUB
    },
    { fr: R.MAC12_LAYER1
    , to: R.MAC19_LAYER3
    , name: "Flopside 2F - Layer 1 - Elevator Down"
    , group: EGroup.ELEVATOR_DOWN | EGroup.HUB
    },
    { fr: R.MAC12_LAYER1
    , to: R.MAC15_LAYER1
    , name: "Flopside 2F - Layer 1 - Left Blue Pipe"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC12_LAYER1
    , to: R.MAC02_LAYER1
    , name: "Flopside 2F - Layer 1 - Right Blue Pipe"
    },
    { fr: R.MAC12_LAYER1
    , to: R.MAC12_LAYER2
    , name: "Flopside 2F - Layer 1 -> 2"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC12_LAYER2
    , to: R.MAC11_LAYER2
    , name: "Flopside 2F - Layer 2 - Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC12_LAYER2
    , to: R.MAC12_LAYER1
    , name: "Flopside 2F - Layer 2 -> 1"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC12_LAYER2
    , to: R.MAC12_LAYER3
    , name: "Flopside 2F - Layer 2 -> 3"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC12_LAYER3
    , to: R.MAC16_LAYER1
    , name: "Flopside 2F - Layer 3 - Blocked Pipe"
    , group: EGroup.PIPE | EGroup.HUB
    },
    { fr: R.MAC12_LAYER3
    , to: R.MAC12_LAYER2
    , name: "Flopside 2F - Layer 3 -> 2"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC14_RIGHT
    , to: R.MAC15_LAYER1
    , name: "Flopside B1 - Elevator Down"
    },
    { fr: R.MAC14_RIGHT
    , to: R.MAC19_LAYER3
    , name: "Flopside B1 - Elevator Up"
    },
    { fr: R.MAC14_RIGHT
    , to: R.MAC14_LEFT
    , name: "Flopside B1 - Right -> Left"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC14_RIGHT
    , to: R.MAC14_L_BACK_BEVERAGARIUM
    , name: "Flopside B1 - Beveragarium"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC14_LEFT
    , to: R.MAC14_L_ITTY_BITS
    , name: "Flopside B1 - Itty Bits"
    , rule: Has(I.PIXL_DOTTIE)
    },
    { fr: R.MAC14_LEFT
    , to: R.MAC14_RIGHT
    , name: "Flopside B1 - Left -> Right"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC15_LAYER1
    , to: R.L_FLOPSIDE_PIT
    , name: "Flopside B2 - Layer 1 - Sealed Pipe"
    # TODO: More access rules
    , rule: (
        True_(options=[OptionFilter(FlopsidePitAccess, FlopsidePitAccess.option_open)]) |
        HasAll(E.COMPLETED_FLIPSIDE_PIT, E.FLEEP_FLOPSIDE_PIT_CAGE, options=[OptionFilter(FlopsidePitAccess, FlopsidePitAccess.option_normal)]) |
        Has(E.FLEEP_FLOPSIDE_PIT_CAGE, options=[OptionFilter(FlopsidePitAccess, FlopsidePitAccess.option_no_flipside)]))
    },
    { fr: R.MAC15_LAYER1
    , to: R.MAC12_LAYER1
    , name: "Flopside B2 - Layer 2 - Blue Pipe"
    },
    { fr: R.MAC15_LAYER1
    , to: R.L_FLOPSIDE_PIT_TOP
    , name: "Flopside B2 - Layer 1 -> Top of Cage"
    , rule: RuleHolder.can_super_jump
    },
    { fr: R.MAC15_LAYER1
    , to: R.MAC14_RIGHT
    , name: "Flopside B2 - Layer 1 - Elevator Up"
    },
    { fr: R.MAC15_LAYER2
    , to: R.MAC18
    , name: "Flopside B2 - Layer 2 - Chasm Fall"
    },
    { fr: R.MAC15_LAYER2
    , to: R.MAC17_LAYER2
    , name: "Flopside B2 - Layer 2 - Pipe"
    },
    { fr: R.MAC15_LAYER2
    , to: R.L_FLOPSIDE_PIT_TOP
    , name: "Flopside B2 - Layer 2 - Cage Top"
    , rule: (RuleHolder.can_super_jump | Has(I.PIXL_TIPPI)) & RuleHolder.can_flip
    },
    { fr: R.L_FLOPSIDE_PIT_TOP
    , to: R.MAC15_LAYER1
    , name: "Flopside B2 Cage Top - Drop"
    },
    { fr: R.L_FLOPSIDE_PIT_TOP
    , to: R.MAC15_LAYER2
    , name: "Flopside B2 Cage Top - Layer 2"
    },
    { fr: R.MAC16_LAYER1
    , to: R.MAC12_LAYER3
    , name: "Flopside 1F Outskirts - Layer 1 - Left Blocked Pipe"
    },
    { fr: R.MAC16_LAYER1
    , to: R.MAC17_LAYER1
    , name: "Flopside 1F Outskirts - Layer 1 - Right Pipe"
    },
    { fr: R.MAC16_LAYER1
    , to: R.MAC16_LAYER2
    , name: "Flopside 1F Outskirts - Layer 1 -> 2"
    },
    { fr: R.MAC16_LAYER2
    , to: R.MAC16_LAYER1
    , name: "Flopside 1F Outskirts - Layer 2 -> 1"
    },
    { fr: R.MAC17_LAYER1
    , to: R.MAC15_LAYER2
    , name: "Flopside B1 Outskirts - Left Pipe"
    },
    { fr: R.MAC17_LAYER1
    , to: R.MAC16_LAYER1
    , name: "Flopside B1 Outskirts - Right Pipe"
    },
    { fr: R.MAC17_LAYER2
    , to: R.MAC17_LAYER1
    , name: "Flopside B1 Outskirts - Layer 2 -> 1"
    # TODO: Double-check rule
    , rule: RuleHolder.can_flip & Has(I.CHARACTER_LUIGI)
    },
    { fr: R.MAC18
    , to: R.MAC15_LAYER1
    , name: "Flopside B2 - Jump Out"
    },
    { fr: R.MAC19_LAYER1
    , to: R.MAC03_LAYER2
    , name: "Flopside 1F - Layer 1 - Door"
    , group: EGroup.HUB | EGroup.DOOR
    },
    { fr: R.MAC19_LAYER1
    , to: R.MAC19_LAYER2
    , name: "Flopside 1F - Layer 1 -> 2"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MAC19_LAYER2
    , to: R.MAC19_LAYER1
    , name: "Flopside 1F - Layer 2 -> 1"
    , rule: RuleHolder.can_flip & Has(I.PIXL_FLEEP)
    },
    { fr: R.MAC19_LAYER2
    , to: R.MAC19_LAYER3
    , name: "Flopside 1F - Layer 2 -> 3"
    , rule: RuleHolder.can_flip & Has(I.PIXL_BOOMER)
    },
    { fr: R.MAC19_LAYER3
    , to: R.MAC12_LAYER1
    , name: "Flopside 1F - Layer 3 - Elevator Up"
    , group: EGroup.ELEVATOR_UP | EGroup.HUB
    },
    { fr: R.MAC19_LAYER3
    , to: R.MAC14_RIGHT
    , name: "Flopside 1F - Layer 3 - Elevator Down"
    , group: EGroup.ELEVATOR_UP | EGroup.HUB
    },
    { fr: R.MAC19_LAYER3
    , to: R.MAC19_LAYER2
    , name: "Flopside 1F - Layer 3 -> 2"
    },
    { fr: R.MAC03_LAYER2
    , to: R.MAC19_LAYER1
    , name: "Flopside 1F - Mirror Hall - Left Door"
    , group: EGroup.DOOR | EGroup.HUB
    },
    { fr: R.MAC03_LAYER2
    , to: R.MAC03_LAYER1
    , name: "Flipside 1F - Mirror Hall - Layer 2 -> 1"
    },
    #endregion
    #region Chapter 1-1
    #TODO: ER settings
    { fr: R.HE101
    , to: R.HE106
    , rule: Has(I.PIXL_TIPPI)
    , name: f"{R.HE101} - Bestovius' House, Hidden Door"
    },
    { fr: R.HE101
    , to: R.HE103
    , name: f"{R.HE101} - Front Pipe near Bestovius' House"
    },
    { fr: R.HE101
    , to: R.HE102
    , name: f"{R.HE101} - Sealed Door"
    , rule: RuleHolder.can_flip
    },
    { fr: R.HE102
    , to: R.HE101
    , name: f"{R.HE102} - Left Door"
    },
    { fr: R.HE102
    , to: R.HE104
    , name: f"{R.HE102} - Right Door"
    , rule: RuleHolder.can_flip | RuleHolder.can_float
    },
    { fr: R.HE103
    , to: R.HE101
    , name: f"{R.HE103} - Right Pipe"
    },
    { fr: R.HE104
    , to: R.HE102
    , name: f"{R.HE104} - Left Door"
    },
    { fr: R.HE104
    , to: R.HE105
    , name: f"{R.HE104} - Right Door"
    , rule: RuleHolder.can_flip | RuleHolder.can_super_jump
    },
    { fr: R.HE105
    , to: R.HE104
    , name: f"{R.HE105} - Left Door"
    },
    { fr: R.HE106
    , to: R.HE101
    , name: f"{R.HE106} - Door"
    },
    #endregion
    #region Chapter 1-2
    { fr: R.HE201
    , to: R.HE202
    , name: f"{R.HE201} - Right Door"
    },
    { fr: R.HE201
    , to: R.HE202
    , name: f"{R.HE201} - Hidden Shortcut Door"
    , rule: RuleHolder.can_flip
    },
    { fr: R.HE202
    , to: R.HE201
    , name: f"{R.HE202} - Left Door"
    },
    { fr: R.HE202
    , to: R.HE203
    , name: f"{R.HE202} - Right Door"
    , rule: RuleHolder.can_flip | (RuleHolder.can_float & RuleHolder.can_super_jump & Has(I.PIXL_DASHELL))
    },
    { fr: R.HE203
    , to: R.HE208
    , name: f"{R.HE203} - Pipe behind bricks"
    , rule: RuleHolder.can_flip
    },
    { fr: R.HE203
    , to: R.HE206
    , name: f"{R.HE203} - Pipe in house behind partition"
    , rule: RuleHolder.can_flip
    },
    { fr: R.HE203
    , to: R.HE202
    , name: f"{R.HE203} - Left Door"
    },
    { fr: R.HE203
    , to: R.HE204
    , name: f"{R.HE203} - Red's House"
    },
    { fr: R.HE203
    , to: R.HE205
    , name: f"{R.HE203} - Green's House"
    , rule: RuleHolder.can_flip | RuleHolder.can_float | Has(I.PIXL_DASHELL)
    },
    { fr: R.HE204
    , to: R.HE203
    , name: f"{R.HE204} - Door"
    },
    { fr: R.HE205
    , to: R.HE203
    , name: f"{R.HE205} - Door"
    },
    { fr: R.HE206
    , to: R.HE203
    , name: f"{R.HE206} - Left Pipe"
    },
    { fr: R.HE206
    , to: R.HE209
    , name: f"{R.HE206} - Right Door"
    },
    { fr: R.HE207
    , to: R.HE209
    , name: f"{R.HE207} - Door"
    , rule: Has(I.PIXL_THOREAU)
    },
    { fr: R.HE208
    , to: R.HE203
    , name: f"{R.HE208} - Door"
    },
    { fr: R.HE209
    , to: R.HE206
    , name: f"{R.HE209} - Left Door"
    },
    { fr: R.HE209
    , to: R.HE207
    , name: f"{R.HE209} - Right Door"
    , rule: Has(I.PIXL_TIPPI)
    },
    #endregion
    #region Chapter 1-3
    { fr: R.HE301
    , to: R.HE303
    , name: f"{R.HE301} - Door below red palm tree"
    },
    { fr: R.HE301
    , to: R.HE302
    , name: f"{R.HE301} - Right door"
    },
    { fr: R.HE302
    , to: R.HE301
    , name: f"{R.HE302} - Left Door"
    },
    { fr: R.HE303
    , to: R.HE305
    , name: f"{R.HE303} - Pipe on floating bricks"
    # TODO: Double-check rules
    , rule: RuleHolder.can_flip | RuleHolder.can_float | Has(I.PIXL_DASHELL)
            | (Has(I.PIXL_THOREAU) & RuleHolder.can_super_jump)
    },
    { fr: R.HE303
    , to: R.HE301
    , name: f"{R.HE303} - Left Door"
    },
    { fr: R.HE303
    , to: R.HE304
    , name: f"{R.HE303} - Right Door"
    , rule: RuleHolder.can_flip | RuleHolder.can_float | HasAny(I.PIXL_DASHELL, I.PIXL_THOREAU)
    },
    { fr: R.HE304
    , to: R.HE303
    , name: f"{R.HE304} - Left Door"
    },
    { fr: R.HE304
    , to: R.HE306
    , name: f"{R.HE304} - Right Door"
    },
    { fr: R.HE305
    , to: R.HE303
    , name: f"{R.HE305} - Pipe"
    },
    { fr: R.HE306
    , to: R.HE307
    , name: f"{R.HE306} - Left door on floating bricks"
    },
    { fr: R.HE306
    , to: R.HE304
    , name: f"{R.HE306} - Door on ground"
    },
    { fr: R.HE306
    , to: R.HE308
    , name: f"{R.HE306} - Right door on floating bricks"
    },
    { fr: R.HE307
    , to: R.HE306
    , name: f"{R.HE307} - Door"
    },
    { fr: R.HE308
    , to: R.HE306
    , name: f"{R.HE308} - Door"
    },
    #endregion
    # Chapter 1-4
    { fr: R.HE401
    , to: R.HE402
    , name: f"{R.HE401} - Door"
    },
    { fr: R.HE402
    , to: R.HE401
    , name: f"{R.HE402} - Left Door"
    },
    { fr: R.HE402
    , to: R.HE403
    , name: f"{R.HE402} - Right Door"
    },
    { fr: R.HE403
    , to: R.HE402
    , name: f"{R.HE403} - Left Door"
    },
    { fr: R.HE403
    , to: R.HE405
    , name: f"{R.HE403} - Middle Door"
    # MOD: Will ruins keys be split into 3 separate ids for each door? If so we don't need full key logic here for ER.
    , rule: Has(I.RUINS_KEY, count=3, options=[OptionFilter(EntranceRando, Toggle.option_true)])
            | Has(I.RUINS_KEY)
    },
    { fr: R.HE403
    , to: R.HE404
    , name: f"{R.HE403} - Right Door"
    , rule: RuleHolder.can_flip
    },
    { fr: R.HE404
    , to: R.HE403
    , name: f"{R.HE404} - Door"
    },
    { fr: R.HE405
    , to: R.HE403
    , name: f"{R.HE405} - Left Door"
    },
    { fr: R.HE405
    , to: R.HE406
    , name: f"{R.HE405} - Right Upper Door"
    },
    { fr: R.HE405
    , to: R.HE412
    , name: f"{R.HE405} - Right Lower Door"
    , rule: Has(I.RUINS_KEY, count=3, options=[OptionFilter(EntranceRando, Toggle.option_true)])
            | Has(I.RUINS_KEY, count=2)
    },
    { fr: R.HE406
    , to: R.HE405
    , name: f"{R.HE406} - Door"
    },
    { fr: R.HE407
    , to: R.HE412
    , name: f"{R.HE407} - Left Door"
    },
    { fr: R.HE407
    , to: R.HE408
    , name: f"{R.HE407} - Right Door"
    , rule: Has(I.RUINS_KEY, count=3)
    },
    { fr: R.HE408
    , to: R.HE407
    , name: f"{R.HE408} - Lower Door"
    },
    { fr: R.HE408
    , to: R.HE409
    , name: f"{R.HE408} - Upper Door"
    , rule: RuleHolder.can_flip
    },
    { fr: R.HE409
    , to: R.HE410
    , name: f"{R.HE409} - Pipe"
    },
    { fr: R.HE409
    , to: R.HE408
    , name: f"{R.HE409} - Door"
    },
    { fr: R.HE410
    , to: R.HE411
    , name: f"{R.HE410} - Door"
    },
    { fr: R.HE411
    , to: R.HE410
    , name: f"{R.HE411} - Door"
    },
    { fr: R.HE412
    , to: R.HE405
    , name: f"{R.HE412} - Left Door"
    },
    { fr: R.HE412
    , to: R.HE407
    , name: f"{R.HE412} - Right Door"
    , rule: Has(I.PIXL_TIPPI)
    },
    #endregion
    #region Chapter 2-1
    { fr: R.MI101
    , to: R.MI105
    , name: f"{R.MI101} - Pipe"
    , rule: (RuleHolder.can_float | Has(I.PIXL_DASHELL)) & (RuleHolder.can_flip | RuleHolder.can_super_jump)
    },
    { fr: R.MI101
    , to: R.MI108
    , name: f"{R.MI101} - Locked Door"
    , rule: (RuleHolder.can_float | Has(I.PIXL_DASHELL)) & Has(I.DOOR_KEY_21)
    },
    { fr: R.MI102
    , to: R.MI110
    , name: f"{R.MI102} - Bottom Door"
    },
    { fr: R.MI102
    , to: R.MI110  # TODO: split out this and the connection above for ER
    , name: f"{R.MI102} - Top Door"
    },
    { fr: R.MI103
    , to: R.MI110
    , name: f"{R.MI103} - Bottom Door"
    },
    { fr: R.MI103
    , to: R.MI110
    , name: f"{R.MI103} - Top Door"
    },
    { fr: R.MI104
    , to: R.MI110
    , name: f"{R.MI104} - Door"
    },
    { fr: R.MI105
    , to: R.MI101
    , name: f"{R.MI105} - Pipe"
    },
    { fr: R.MI106
    , to: R.MI110
    , name: f"{R.MI106} - Right Pipe"
    },
    { fr: R.MI106
    , to: R.MI107
    , name: f"{R.MI106} - Left Pipe"
    },
    { fr: R.MI107
    , to: R.MI106
    , name: f"{R.MI107} - Pipe"
    },
    { fr: R.MI108
    , to: R.MI101
    , name: f"{R.MI108} - Left Door"
    },
    { fr: R.MI108
    , to: R.MI109
    , name: f"{R.MI108} - Middle Door"
    },
    { fr: R.MI108
    , to: R.MI111
    , name: f"{R.MI108} - Right Door"
    , rule: Has(E.SWITCH_GLOAM_VALLEY_BACKGROUND)
    },
    { fr: R.MI109
    , to: R.MI108
    , name: f"{R.MI109} - Door"
    },
    { fr: R.MI110
    , to: R.MI106
    , name: f"{R.MI110} - Pipe"
    , rule: RuleHolder.mi110_door_group
    },
    { fr: R.MI110
    , to: R.MI111
    , name: f"{R.MI110} - Ground Door"
    , rule: RuleHolder.mi110_door_group
    },
    { fr: R.MI110
    , to: R.MI104
    , name: f"{R.MI110} - Left Elevated Door (Switch)"
    , rule: RuleHolder.mi110_door_group
    },
    { fr: R.MI110
    , to: R.MI102
    , name: f"{R.MI110} - Middle Left Elevated Door"
    , rule: RuleHolder.mi110_door_group
    },
    { fr: R.MI110
    , to: R.MI103
    , name: f"{R.MI110} - Middle Elevated Door"
    , rule: RuleHolder.mi110_door_group
    },
    { fr: R.MI111
    , to: R.MI108
    , name: f"{R.MI111} - Left Door"
    },
    { fr: R.MI111
    , to: R.MI110
    , name: f"{R.MI111} - Right Door"
    },
    #endregion
    #region Chapter 2-2
    { fr: R.MI201
    , to: R.MI202
    , name: f"{R.MI201} - Mansion Front Door"
    },
    { fr: R.MI202
    , to: R.MI201
    , name: f"{R.MI202} - Mansion Front Door"
    },
    { fr: R.MI202
    , to: R.MI203
    , name: f"{R.MI202} - Door Behind Curtains"
    , rule: RuleHolder.can_flip
    },
    { fr: R.MI203
    , to: R.MI202
    , name: f"{R.MI203} - Far Left Door"
    },
    { fr: R.MI203
    , to: R.MI207
    , name: f"{R.MI203} - Bottom Right, Left Door"
    },
    { fr: R.MI203
    , to: R.MI204
    , name: f"{R.MI203} - Top Right, Left Door"
    },
    { fr: R.MI203
    , to: R.MI205
    , name: f"{R.MI203} - Top Right, Middle Door"
    },
    { fr: R.MI203
    , to: R.MI206
    , name: f"{R.MI203} - Top Right, Right Door"
    },
    { fr: R.MI203
    , to: R.MI208
    , name: f"{R.MI203} - Bottom Right, Right Door"
    , rule: Has(I.HOUSE_KEY)
    },
    { fr: R.MI204
    , to: R.MI203
    , name: f"{R.MI204} - Door"
    },
    { fr: R.MI204
    , to: R.MI209
    , name: f"{R.MI204} - Pit Trap"
    # , etype: EntranceType.ONE_WAY
    },
    { fr: R.MI205
    , to: R.MI203
    , name: f"{R.MI205} - Door"
    },
    { fr: R.MI205
    , to: R.MI210
    , name: f"{R.MI205} - Pit Trap"
    # , etype: EntranceType.ONE_WAY
    },
    { fr: R.MI206
    , to: R.MI203
    , name: f"{R.MI206} - Door"
    },
    { fr: R.MI207
    , to: R.MI203
    , name: f"{R.MI207} - Door"
    },
    { fr: R.MI207
    , to: R.MI211
    , name: f"{R.MI207} - Pit Trap"
    # , etype: EntranceType.ONE_WAY
    },
    { fr: R.MI208
    , to: R.MI203
    , name: f"{R.MI208} - Door"
    },
    { fr: R.MI209
    , to: R.MI204
    , name: f"{R.MI209} - Pipe"
    # Need boomer to defeat the shlurp
    , rule: Has(I.PIXL_BOOMER)
    },
    { fr: R.MI210
    , to: R.MI205
    , name: f"{R.MI210} - Pipe"
    # Bowser can hit the switch from a distance while carrie zooms him out just barely fast enough
    # Anyone can hit the switch and zoom out with dashell in time
    , rule: (RuleHolder.can_fire & Has(I.PIXL_CARRIE)) | HasAny(I.PIXL_BOOMER, I.PIXL_DASHELL)
    },
    { fr: R.MI211
    , to: R.MI207
    , name: f"{R.MI211} - Pipe"
    # Same as above
    , rule: (RuleHolder.can_fire & Has(I.PIXL_CARRIE)) | HasAny(I.PIXL_BOOMER, I.PIXL_DASHELL)
    },
    #endregion
    #region 2-3
    { fr: R.MI301
    , to: R.MI302
    , name: f"{R.MI301} - Top Left Door"
    },
    { fr: R.MI301
    , to: R.MI303
    , name: f"{R.MI301} - Top Middle Door"
    },
    { fr: R.MI301
    , to: R.MI304
    , name: f"{R.MI301} - Top Right Door"
    },
    { fr: R.MI301
    , to: R.MI305
    , name: f"{R.MI301} - Lower Left Door"
    , rule: RuleHolder.can_float | HasAny(I.PIXL_CARRIE, I.PIXL_DASHELL)
    },
    { fr: R.MI301
    , to: R.MI306
    , name: f"{R.MI301} - Lower Right Door"
    },
    { fr: R.MI302
    , to: R.MI301
    , name: f"{R.MI302} - Door"
    },
    { fr: R.MI303
    , to: R.MI301
    , name: f"{R.MI303} - Door"
    },
    { fr: R.MI304
    , to: R.MI301
    , name: f"{R.MI304} - Door"
    },
    { fr: R.MI305
    , to: R.MI301
    , name: f"{R.MI305} - Door"
    },
    { fr: R.MI306
    , to: R.MI301
    , name: f"{R.MI306} - Door"
    },
    #endregion
    #region Chapter 2-4
    # this chapter has to have the most connections of all time
    { fr: R.MI401
    , to: R.MI402
    , name: f"{R.MI401} - Left Door"
    },
    { fr: R.MI401
    , to: R.MI403
    , name: f"{R.MI401} - Right Door"
    },
    { fr: R.MI402
    , to: R.MI401
    , name: f"{R.MI402} - Left Door"
    },
    { fr: R.MI402
    , to: R.MI404
    , name: f"{R.MI402} - Right Door"
    },
    { fr: R.MI403
    , to: R.MI401
    , name: f"{R.MI403} - Bottom Left Door"
    },
    { fr: R.MI403
    , to: R.MI404
    , name: f"{R.MI403} - Bottom Right Door"
    },
    { fr: R.MI403
    , to: R.MI405
    , name: f"{R.MI403} - Top Right Door"
    },
    { fr: R.MI404
    , to: R.MI406
    , name: f"{R.MI404} - Top Left Door"
    },
    { fr: R.MI404
    , to: R.MI402
    , name: f"{R.MI404} - Middle Floating Door"
    },
    { fr: R.MI404
    , to: R.MI403
    , name: f"{R.MI404} - Bottom Right Door"
    },
    { fr: R.MI405
    , to: R.MI403
    , name: f"{R.MI405} - Left Door"
    },
    { fr: R.MI405
    , to: R.MI406
    , name: f"{R.MI405} - Right Door"
    },
    { fr: R.MI406
    , to: R.MI409
    , name: f"{R.MI406} - Top Right Door"
    },
    { fr: R.MI406
    , to: R.MI405
    , name: f"{R.MI406} - Bottom Right Door"
    },
    { fr: R.MI406
    , to: R.MI404
    , name: f"{R.MI406} - Bottom Left Door"
    },
    { fr: R.MI407
    , to: R.MI408
    , name: f"{R.MI407} - Top Left Door"
    },
    { fr: R.MI407
    , to: R.MI410
    , name: f"{R.MI407} - Top Right Door"
    },
    { fr: R.MI407
    , to: R.MI409
    , name: f"{R.MI407} - Bottom Left Door"
    },
    { fr: R.MI408
    , to: R.MI410
    , name: f"{R.MI408} - Top Left Door"
    },
    { fr: R.MI408
    , to: R.MI411
    , name: f"{R.MI408} - Top Right Door"
    },
    { fr: R.MI408
    , to: R.MI407
    , name: f"{R.MI408} - Bottom Left Door"
    },
    { fr: R.MI408
    , to: R.MI410
    , name: f"{R.MI408} - Bottom Right Door"
    },
    { fr: R.MI409
    , to: R.MI406
    , name: f"{R.MI409} - Left Door"
    },
    { fr: R.MI409
    , to: R.MI407
    , name: f"{R.MI409} - Bottom Door"
    },
    # MI409 Top door can't be entered
    { fr: R.MI410
    , to: R.MI408
    , name: f"{R.MI410} - Top Left Door"
    },
    { fr: R.MI410
    , to: R.MI411
    , name: f"{R.MI410} - Top Right Door"
    },
    { fr: R.MI410
    , to: R.MI408
    , name: f"{R.MI410} - Bottom Left Door"
    },
    { fr: R.MI410
    , to: R.MI407
    , name: f"{R.MI410} - Bottom Right Door"
    },
    { fr: R.MI411
    , to: R.MI415
    , name: f"{R.MI411} - Top Left Door"
    },
    # { fr: R.MI411
    # , to: R.MI411
    # , name: f"{R.MI411} - Top Right Door"  # TODO: double-check, i don't think this door can be entered
    # },
    { fr: R.MI411
    , to: R.MI410
    , name: f"{R.MI411} - Bottom Left Door"
    },
    { fr: R.MI411
    , to: R.MI409
    , name: f"{R.MI411} - Bottom Right Door"
    },
    { fr: R.MI412
    , to: R.MI415
    , name: f"{R.MI412} - Left Door"
    },
    { fr: R.MI412
    , to: R.MI413
    , name: f"{R.MI412} - Men's Bathroom Door"
    },
    { fr: R.MI412
    , to: R.MI414
    , name: f"{R.MI412} - Women's Bathroom Door"
    },
    { fr: R.MI413
    , to: R.MI412
    , name: f"{R.MI413} - Door"
    },
    { fr: R.MI414
    , to: R.MI412
    , name: f"{R.MI414} - Door"
    },
    { fr: R.MI415
    , to: R.MI411
    , name: f"{R.MI415} - Bottom Door"
    },
    { fr: R.MI415
    , to: R.MI412
    , name: f"{R.MI415} - Top Door"
    },
    #endregion
    #region 3-1
    # { fr: R.TA101
    # , to: R.TA102
    # , name: f"{R.TA101} - Door in the sky"  # doa1_l
    # },
    # { fr: R.TA101
    # , to: R.TA103
    # , name: f"{R.TA101} - Fall between Red Pipes"  # Entrance has an empty name
    # , etype: EntranceType.ONE_WAY
    # },
    # { fr: R.TA101
    # , to: R.MAC02_L_TOWER
    # , name: f"{R.TA101} - Left Red Pipe"  # dokan_m
    # , etype: EntranceType.ONE_WAY
    # },
    # { fr: R.TA101
    # , to: R.MAC02_L_TOWER
    # , name: f"{R.TA101} - Right Red Pipe"  # dokan_m2
    # , etype: EntranceType.ONE_WAY
    # },
    # { fr: R.TA101
    # , to: R.MAC02_L_TOWER
    # , name: f"{R.TA101} - Right Background Pipe"  # hai_dokan_03
    # , etype: EntranceType.ONE_WAY
    # },
    #endregion
]  # fmt: skip


ENTRANCE_DATA: list[EntranceRule] = [EntranceRule(**edata) for edata in ENTRANCE_RULES]  # ty: ignore[invalid-argument-type]


LOCATION_RULES = [
    #region Flipside
    { loc: L.FLIPSIDE_HEART_PILLAR_RED
    , rule: Has(I.RED_PURE_HEART)
    },
    { loc: L.FLIPSIDE_3F_EAT_A_SPICY_SOUP
    , rule: True_()  # MOD: will this require spicy soup in the itempool?
    },
    { loc: L.FLEEP_MAP_REVEAL_01
    , rule: CanFleepTreasureSpot(I.MAP_1)
    },
    { loc: L.FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS
    , rule: Has(I.PIXL_TIPPI)
    },
    { loc: L.FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK
    , rule: Has(I.PIXL_PICCOLO)
    },
    { loc: L.PICCOLO_FETCH_MERLUVLEE
    , rule: Has(I.TRAINING_MACHINE)
    },
    { loc: L.FLEEP_MAP_REVEAL_02
    , rule: CanFleepTreasureSpot(I.MAP_2)
    },
    { loc: L.FLIPSIDE_HEART_PILLAR_GREEN
    , rule: HasAll(I.PIXL_THUDLEY, I.GREEN_PURE_HEART)
    },
    { loc: L.FLIPSIDE_B1_3D_CHEST
    , rule: RuleHolder.can_flip
    },
    { loc: L.FLEEP_MAP_REVEAL_03
    , rule: CanFleepTreasureSpot(I.MAP_3)
    },
    { loc: L.FLEEP_MAP_REVEAL_04
    , rule: CanFleepTreasureSpot(I.MAP_4)
    },
    { loc: L.FLIPSIDE_B2_CHEST_AFTER_PIPE
    , rule: Has(E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK)
    },
    { loc: L.FLIPSIDE_HEART_PILLAR_ORANGE
    , rule: (RuleHolder.can_float
            # Throeau places a squig below the pillars to jump off of
            | Has(I.PIXL_THOREAU, options=[OptionFilter(ObscureTricks, Toggle.option_true)], filtered_resolution=True)
            ) & Has(I.ORANGE_PURE_HEART)
    },
    { loc: L.FLIPSIDE_HEART_PILLAR_YELLOW
    , rule: RuleHolder.can_flip & HasAll(I.YELLOW_PURE_HEART, I.PIXL_SLIM)
    },
    #endregion
    #region Flopside
    { loc: L.FLOPSIDE_HEART_PILLAR_CYAN
    , rule: Has(I.CYAN_PURE_HEART)
    },
    { loc: L.FLEEP_MAP_REVEAL_05
    , rule: CanFleepTreasureSpot(I.MAP_5)
    },
    { loc: L.FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK
    , rule: Has(I.PIXL_PICCOLO)
    },
    { loc: L.FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS
    , rule: Has(I.PIXL_TIPPI)
    },
    { loc: L.PICCOLO_FETCH_MERLEE
    , rule: Has(I.CRYSTAL_BALL)
    },
    { loc: L.FLOPSIDE_HEART_PILLAR_WHITE
    , rule: Has(I.WHITE_PURE_HEART)
    },
    { loc: E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK
    , rule: RuleHolder.can_flip & Has(I.PIXL_CUDGE)
    },
    { loc: E.FLEEP_FLOPSIDE_PIT_CAGE
    , rule: Has(I.PIXL_FLEEP)
    },
    { loc: L.FLOPSIDE_B2_CHEST_AFTER_PIPE
    , rule: Has(E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK)
    },
    { loc: L.FLOPSIDE_HEART_PILLAR_BLUE
    , rule: Has(I.BLUE_PURE_HEART)
    },
    { loc: L.FLOPSIDE_HEART_PILLAR_PURPLE
    # Luigi can make the jump w/o super jump
    , rule: HasAll(I.PURPLE_PURE_HEART, I.CHARACTER_LUIGI)
    },
    { loc: E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK
    , rule: Has(I.PIXL_CUDGE)
    },
    #endregion
    #region Chapter 1-1
    { loc: L.C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY
    , rule: RuleHolder.can_flip
    },
    { loc: L.C11_OPEN_ITEM_BEHIND_PIPE
    , rule: RuleHolder.can_flip
    },
    { loc: L.C11_CHEST_AFTER_STAR_BLOCK
    , rule: RuleHolder.can_flip
    },
    { loc: L.C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM
    , rule: RuleHolder.can_flip
    },
    { loc: L.C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM
    , rule: RuleHolder.can_flip
    },
    #endregion
    #region Chapter 1-2
    { loc: L.C12_CHEST_IN_SHORTCUT
    , rule: RuleHolder.can_flip
    },
    { loc: L.C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE
    , rule: RuleHolder.can_flip | RuleHolder.can_float | Has(I.PIXL_DASHELL)
    },
    { loc: L.C12_STAR_BLOCK
    # MOD: Will Watchitt still require having Thoreau to tell Green to build the bridge?
    , rule: (RuleHolder.can_flip & Has(I.PIXL_THOREAU)) | RuleHolder.can_float | Has(I.PIXL_DASHELL)
    },
    { loc: L.C12_OPEN_ITEM_BEHIND_GREENS_BED
    , rule: RuleHolder.can_flip
    },
    #endregion
    #region Chapter 1-3
    { loc: L.C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM
    , rule: RuleHolder.can_flip
    },
    { loc: L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM
    , rule: RuleHolder.can_flip
    },
    { loc: L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM
    , rule: RuleHolder.can_flip
    },
    #endregion
    #region Chapter 1-4
    # MOD: THOREAU has to be patched to always be thrown at *Mario's* height!
    # Otherwise this has to be updated to always require mario.
    { loc: L.C14_OPEN_KEY_BEHIND_BLOCKS
    , rule: HasAll(I.PIXL_THOREAU, E.SWITCH_YOLD_RUINS_SQUIG_ROOM)
    },
    { loc: E.SWITCH_YOLD_RUINS_SQUIG_ROOM
    , rule: RuleHolder.can_super_jump | Has(I.PIXL_THOREAU)
    },
    { loc: L.C14_HIDDEN_CHEST_AFTER_3D_PATH
    , rule: RuleHolder.can_flip
    },
    { loc: L.C14_OPEN_KEY_BEHIND_BLOCKS
    , rule: RuleHolder.can_flip
    },
    #endregion
    #region Chapter 2-1
    { loc: E.SWITCH_GLOAM_VALLEY_UNDERGROUND
    , rule: RuleHolder.can_flip & Has(I.PIXL_BOOMER)
    },
    { loc: L.C21_LEFT_CHEST_BEFORE_STAR_BLOCK
    , rule: RuleHolder.can_flip
    },
    { loc: L.C21_RIGHT_CHEST_BEFORE_STAR_BLOCK
    , rule: RuleHolder.can_flip
    },
    { loc: L.C21_CHEST_BEHIND_BOOMER_CHEST
    , rule: RuleHolder.can_flip & Has(I.PIXL_BOOMER)
    },
    { loc: E.SWITCH_GLOAM_VALLEY_BACKGROUND
    , rule: RuleHolder.can_float | Has(I.PIXL_DASHELL)
    },
    #endregion
    #region Chapter 2-2
    { loc: L.C22_CHEST_ON_ROOF
    , rule: RuleHolder.can_flip
    },
    { loc: L.C22_CHEST_ABOVE_SPIKE_ROOF
    , rule: RuleHolder.can_flip & (HasAny(I.PIXL_BOOMER, I.PIXL_CUDGE) | RuleHolder.can_fire)
    },
    #endregion
    #region Chapter 2-3
    { loc: E.OPEN_THE_RUBEE_VAULT
    , rule: RuleHolder.can_flip & Has(I.PIXL_SLIM)
    },
    { loc: L.FLEEP_MAP_REVEAL_15
    , rule: CanFleepTreasureSpot(I.MAP_15)
    },
    { loc: L.C23_STAR_BLOCK
    , rule: Has(E.OPEN_THE_RUBEE_VAULT)
    },
    #endregion
    #region Chapter 2-4
    { loc: L.FLEEP_MAP_REVEAL_16
    , rule: CanFleepTreasureSpot(I.MAP_16)
    },
    { loc: L.C24_OPEN_ITEM_BEHIND_ROOM_08_SIGN
    , rule: RuleHolder.can_flip & Has(I.PIXL_BOOMER)
    },
    { loc: L.FLEEP_MAP_REVEAL_17
    , rule: CanFleepTreasureSpot(I.MAP_17)
    },
    { loc: L.C24_YELLOW_PURE_HEART
    , rule: Has(I.PIXL_THOREAU)  # TODO: Add more ways to defeat mimi
    },
    #endregion
]  # fmt: skip

LOCATION_DATA: list[LocationRule] = [LocationRule(**ldata) for ldata in LOCATION_RULES]  # ty: ignore[invalid-argument-type]
