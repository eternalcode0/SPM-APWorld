"""All things that define logical access between regions and locations"""
import typing
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

from BaseClasses import CollectionState
from entrance_rando import EntranceType
from Options import Toggle
from rule_builder.rules import Has, HasAll, HasAny, OptionFilter, Rule, True_

from .data import GAME
from .names import EventName as E
from .names import ItemName as I
from .names import LocationName as L
from .names import RegionName as R
from .options import (
    ChapterKeysLock,
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
        if world.options.chapter_keys_lock == ChapterKeysLock.option_subchapters_locked:
            return Has(self.chapter_key.value).resolve(world)
        if world.options.chapter_keys_lock == ChapterKeysLock.option_chapter_locked:
            return Has(self.subchapter_key.value).resolve(world)
        return True_().resolve(world)  # == ChapterKeysLock.option_open


def create_entrance(world: "SuperPaperMarioWorld",
    from_region: R,
    to_region: R,
    rule: typing.Callable[[CollectionState], bool] | Rule[typing.Any] | None = None,
    name: str | None = None,
    group: int = 0,
    type: EntranceType = EntranceType.TWO_WAY,
    force_creation: bool = False,
    ):
    entrance = world.create_entrance(world.rm[from_region], world.rm[to_region], rule, name, force_creation)
    if entrance is not None:
        entrance.randomization_group = group
        entrance.randomization_type = type


class RuleHolder:
    """Accessibility container for common Rules & Filers"""

    # OptionFilters
    shuffle_ability_filter = OptionFilter(ShuffleAbilities, Toggle.option_true)
    flipside_pit_access_filter = OptionFilter(FlipsidePitAccess, FlipsidePitAccess.option_closed, operator="ne")

    # Base Rules
    can_flip = (
        Has(I.CHARACTER_MARIO) &
        (Has(I.ABILITY_FLIP) | shuffle_ability_filter)
    )
    can_float = (
        Has(I.CHARACTER_PEACH) &
        (Has(I.ABILITY_UMBRELLA) | shuffle_ability_filter)
    )
    can_fire = (
        Has(I.CHARACTER_BOWSER) &
        (Has(I.ABILITY_FIRE) | shuffle_ability_filter)
    )
    can_super_jump = (
        Has(I.CHARACTER_LUIGI) &
        (Has(I.ABILITY_SUPER_JUMP) | shuffle_ability_filter)
    )
    can_break_hard_blocks = (
        HasAny(I.PIXL_BOOMER, I.PIXL_CUDGE, I.PIXL_THUDLEY) |
        can_fire
    )


def connect_regions(world: "SuperPaperMarioWorld") -> None:
    """Assign all of the location/event collection rules as well as the completion condition"""

    _ = [create_entrance(world, edata.fr, edata.to, edata.rule, edata.name, edata.group, edata.etype)
        for edata in ENTRANCE_DATA]


def set_rules(world: "SuperPaperMarioWorld") -> None:
    world.set_completion_rule(Has(E.VICTORY))

    _ = [world.set_rule(world.lm[ldata.loc], ldata.rule)
        for ldata in LOCATION_DATA
        if ldata.loc in world.lm]


# Set to the following if ER with chapter doors is ever figured out
# { group: EGroup.HUB | EGroup.DOOR, etype: EntranceType.ONE_WAY }
CHAPTER_DOOR_ER = { etype: EntranceType.ONE_WAY }


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
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_1_KEY)
    , name: "Flopside Tower - Black Door [1-1]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC12_L_TOWER
    , to: R.LS201
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_2_KEY)
    , name: "Flopside Tower - Black Door [1-2]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC12_L_TOWER
    , to: R.LS301
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_3_KEY)
    , name: "Flopside Tower - Black Door [1-3]"
    , **CHAPTER_DOOR_ER
    },
    { fr: R.MAC12_L_TOWER
    , to: R.LS401
    , rule: HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_4_KEY)
    , name: "Flopside Tower - Black Door [1-4]"
    , **CHAPTER_DOOR_ER
    },
    #endregion
    #region Flipside
    { fr: R.MAC02_L_TOWER
    , to: R.MAC01_LAYER1
    , name: "Flipside Tower - Fall"
    , group: EGroup.HUB | EGroup.FALL
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
    , group: EGroup.ELEVATOR_UP | EGroup.HUB
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
    , to: R.L_FLIPSIDE_PIT_ENTRANCE
    , rule: RuleHolder.can_super_jump | Has(E.SWITCH_FLIPSIDE_PIT_CAGE)
    , name: "Flipside B2 - Layer 1 -> Cage"
    },
    { fr: R.L_FLIPSIDE_PIT_ENTRANCE
    , to: R.MAC05_LAYER2
    , rule: RuleHolder.can_flip
    , name: "Flipside B2 - Layer 1 Cage -> 2"
    },
    { fr: R.MAC05_LAYER2
    , to: R.L_FLIPSIDE_PIT_ENTRANCE
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
    , rule: True_(options=[OptionFilter(FlopsidePitAccess, FlopsidePitAccess.option_open)])
    },
    { fr: R.MAC15_LAYER1
    , to: R.MAC12_LAYER1
    , name: "Flopside B2 - Layer 2 - Blue Pipe"
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
    }
    #endregion
]

ENTRANCE_DATA: list[EntranceRule] = [EntranceRule(**edata) for edata in ENTRANCE_RULES]


LOCATION_RULES = [
    #region Flipside
    { loc: L.FLIPSIDE_HEART_PILLAR_RED
    , rule: Has(I.RED_PURE_HEART)
    },
    { loc: L.FLIPSIDE_3F_EAT_A_SPICY_SOUP
    , rule: True_()  # MOD: will this require spicy soup in the itempool?
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
    { loc: L.FLIPSIDE_HEART_PILLAR_GREEN
    , rule: HasAll(I.PIXL_THUDLEY, I.GREEN_PURE_HEART)
    },
    { loc: L.FLIPSIDE_B1_3D_CHEST
    , rule: RuleHolder.can_flip
    },
    { loc: L.FLIPSIDE_B2_CHEST_AFTER_PIPE
    , rule: Has(E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK)
    },
    { loc: L.FLIPSIDE_HEART_PILLAR_ORANGE
    , rule: (RuleHolder.can_float
            # Throeau places a squig below the pillars to jump off of
            | Has(I.PIXL_THOREAU, options=[OptionFilter(ObscureTricks, Toggle.option_true)])
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
]

LOCATION_DATA: list[LocationRule] = [LocationRule(**ldata) for ldata in LOCATION_RULES]
