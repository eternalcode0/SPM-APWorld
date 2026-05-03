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
from NetUtils import JSONMessagePart
from Options import Toggle
from rule_builder.field_resolvers import FromOption
from rule_builder.rules import (
    And,
    False_,
    Has,
    HasAll,
    HasAny,
    HasGroupUnique,
    OptionFilter,
    Or,
    Rule,
    True_,
    WrapperRule,
)
from typing_extensions import TypedDict, override
from worlds.AutoWorld import World

from .names import EventName as E
from .names import ItemName as I
from .names import LocationName as L
from .names import RegionName as R
from .options import (
    ChapterDoorAccess,
    EntranceRando,
    FlipsidePitAccess,
    PureHeartsRequired,
    ShuffleAbilities,
    TrickBowserBumps,
    TrickEnemyJumps,
)
from .types import GAME, SPMWorldBase


class EGroup(IntEnum):
    """An Entrance Group for entrance_rando"""

    NONE = 0
    # Chapter
    CHAP_1 = 1
    CHAP_2 = 2
    CHAP_3 = 3
    CHAP_4 = 4
    CHAP_5 = 5
    CHAP_6 = 6
    CHAP_7 = 7
    CHAP_8 = 8
    HUB = 9


er_within_chapter = lambda group: [group]
er_anywhere_targets = [i for i in range(1, 10)]
er_anywhere = lambda group: er_anywhere_targets


@dataclass(kw_only=True)
class EntranceRule:
    fr: R
    to: R
    rule: Rule | Rule[SPMWorldBase] | None = None
    name: str | None = None
    group: EGroup | int = EGroup.NONE
    etype: EntranceType = EntranceType.TWO_WAY


@dataclass
class LocationRule:
    loc: L | E
    rule: Rule | Rule[SPMWorldBase]


@dataclass
class HasChapterKey(Rule[SPMWorldBase], game=GAME):
    chapter_key: I
    subchapter_key: I

    _OPEN_SUBCHAPTER_KEYS: typing.ClassVar[list[I]] = [
        I.CHAPTER_1_1_KEY,
        I.CHAPTER_2_1_KEY,
        I.CHAPTER_3_1_KEY,
        I.CHAPTER_4_1_KEY,
        I.CHAPTER_5_1_KEY,
        I.CHAPTER_6_1_KEY,
        I.CHAPTER_7_1_KEY,
        I.CHAPTER_8_1_KEY,
    ]

    @override
    def _instantiate(self, world: SPMWorldBase) -> Rule.Resolved:
        # if world.options.chapter_door_access == ChapterDoorAccess.option_subchapters_locked:
        #     return Has(self.chapter_key.value).resolve(world)
        # if world.options.chapter_door_access == ChapterDoorAccess.option_chapter_locked:
        #     return Has(self.subchapter_key.value).resolve(world)
        if (
            world.options.chapter_door_access
            == ChapterDoorAccess.option_subchapters_open
        ):
            return True_().resolve(world)
        if world.options.chapter_door_access == ChapterDoorAccess.option_chapters_open:
            # In this mode the subchapter keys are event items, except for X-1 keys, they're implied access.
            if self.subchapter_key in self._OPEN_SUBCHAPTER_KEYS:
                return True_().resolve(world)
            return Has(self.subchapter_key).resolve(world)
        # if world.options.chapter_door_access == ChapterDoorAccess.option_chapter_locked:
        #     return Has(self.chapter_key).resolve(world)
        # if world.options.chapter_door_access == ChapterDoorAccess.option_subchapter_locked:
        #     return Has(self.subchapter_key).resolve(world)
        raise NotImplementedError(
            f"Unknown chapter_door_access option: {world.options.chapter_door_access}"
        )


@dataclass
class CanFleepTreasureSpot(Rule[SPMWorldBase], game=GAME):
    map: I

    @override
    def _instantiate(self, world: SPMWorldBase) -> Rule.Resolved:
        if world.options.treasure_maps.treasures_open:
            return Has(I.PIXL_FLEEP).resolve(world)
        if world.options.treasure_maps.treasures_standard:
            return HasAll(I.PIXL_FLEEP, self.map).resolve(world)
        if world.options.treasure_maps.treasures_disabled:
            return False_().resolve(world)
        raise NotImplementedError(
            f"Unknown treasure maps option: {world.options.treasure_maps}"
        )


@dataclass
class OutOfLogic(Rule[SPMWorldBase], game=GAME):
    option: OptionFilter

    @override
    def _instantiate(self, world: SPMWorldBase) -> Rule.Resolved:
        return self.Resolved(
            in_logic=self.option.check(world.options),
            # TODO: don't use string of option, it obscures the value name of the setting (TrickThroaueJumps == 1)
            ofilter=str(self.option),
            item_name=getattr(world, "glitches_item_name", ""),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    class Resolved(Rule.Resolved):
        in_logic: bool = False
        ofilter: str = ""
        item_name: str = ""

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has(self.item_name, self.player)

        @override
        def explain_json(
            self, state: CollectionState | None = None
        ) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            return [
                {
                    "type": "color",
                    "color": "green" if self.in_logic else "yellow",
                    "text": str(self),
                }
            ]

        @override
        def __str__(self) -> str:
            return f"{'LogicTrick' if self.in_logic else 'OutOfLogic'}[{self.ofilter}]"


# This is mostly a copy of DrTChops' Macro rule but without the actual macro'ing.
# If a rule needed macro'ing then it isn't being stored as a variable properly, hence renamed this to Describe
# https://github.com/drtchops/Archipelago/blob/57eb8106cc7a1e46546482fc4019e3cab983bcf6/worlds/astalon/logic/custom_rules.py#L289
@dataclass
class Describe(WrapperRule[SPMWorldBase], game=GAME):
    name: str

    @override
    def _instantiate(self, world: SPMWorldBase) -> Rule.Resolved:
        return self.Resolved(
            self.child.resolve(world),
            self.name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(WrapperRule.Resolved):
        name: str

        @override
        def explain_json(
            self, state: CollectionState | None = None
        ) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            return [
                {
                    "type": "color",
                    "color": "green" if self(state) else "salmon",
                    "text": str(self),
                }
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            suffix = ""
            if state is not None:
                suffix = " ✓" if self(state) else " ✕"
            return f"{self.name}{suffix}"

        @override
        def __str__(self) -> str:
            return self.name


class SPMRules:
    """Accessibility container for common Rules & Filters"""

    # OptionFilters
    shuffle_ability_filter = OptionFilter(ShuffleAbilities, Toggle.option_true)
    flipside_pit_access_filter = OptionFilter(
        FlipsidePitAccess, FlipsidePitAccess.option_closed, operator="ne"
    )

    # Base Rules
    can_flip = Describe(
        Has(I.CHARACTER_MARIO)
        & (
            Has(
                I.ABILITY_FLIP,
                options=[shuffle_ability_filter],
                filtered_resolution=True,
            )
        ),
        "Mario flips",
        # Use Mario to flip to the 3rd dimension with A
    )
    can_float = Describe(
        Has(I.CHARACTER_PEACH)
        & (
            Has(
                I.ABILITY_UMBRELLA,
                options=[shuffle_ability_filter],
                filtered_resolution=True,
            )
        ),
        "Peach floats",
        # Use Peach to float by holding jump
    )
    can_fire = Describe(
        Has(I.CHARACTER_BOWSER)
        & (
            Has(
                I.ABILITY_FIRE,
                options=[shuffle_ability_filter],
                filtered_resolution=True,
            )
        ),
        "Bowser breaths fire",
        # Use Bowser to breath fire, breaking blocks or activating switches
    )
    can_luigi_jump = Describe(
        Has(I.CHARACTER_LUIGI),
        "Luigi jumps",  # Luigi has slightly higher jump height even without super jump
    )
    can_super_jump = Describe(
        Has(I.CHARACTER_LUIGI)
        & (
            Has(
                I.ABILITY_SUPER_JUMP,
                options=[shuffle_ability_filter],
                filtered_resolution=True,
            )
        ),
        "Luigi super jumps",
        # Luigi super jumps by holding down
    )
    can_break_hard_blocks = Describe(
        HasAny(I.PIXL_BOOMER, I.PIXL_CUDGE, I.PIXL_THUDLEY) | can_fire,
        "Break hard blocks",
    )
    can_climb_ladder = Describe(
        HasAny(I.CHARACTER_LUIGI, I.CHARACTER_MARIO, I.CHARACTER_PEACH),
        "Climb Ladders",  # Bowser too chunky, I def missed locations that need this rule
    )

    # chapter 2 rules
    mi110_door_group = (
        # Luigi jumps to the doors without touching the blocks
        can_super_jump
        |
        # Bowser builds up speed on carrie and jumps at the blocks while breathing fire
        (can_fire & Has(I.PIXL_CARRIE))
        |
        # Bowser too big to cudge the blocks
        (
            HasAny(I.CHARACTER_LUIGI, I.CHARACTER_MARIO, I.CHARACTER_PEACH)
            & Has(I.PIXL_CUDGE)
        )
        |
        # The normal way to break the blocks
        Has(I.PIXL_BOOMER)
    )

    # Tricks
    single_bowser_bump = And[SPMWorldBase](can_fire, Has(I.PIXL_CARRIE)) & OutOfLogic(
        OptionFilter(TrickBowserBumps, TrickBowserBumps.option_disabled, "ne")
    )
    multiple_bowser_bumps = And[SPMWorldBase](
        can_fire,
        Has(I.PIXL_CARRIE),
    ) & OutOfLogic(
        OptionFilter(TrickBowserBumps, TrickBowserBumps.option_multiple),
    )
    throeau_jump = Has(I.PIXL_THOREAU) & OutOfLogic(
        OptionFilter(TrickEnemyJumps, TrickEnemyJumps.option_setup)
    )


def connect_regions(world: SPMWorldBase) -> list[Entrance]:
    """Connects all the regions together with the appropriate rules.
    Returns the list of entrances that can be randomized.
    """

    def create_entrance(
        world: SPMWorldBase,
        from_region: R,
        to_region: R,
        rule: typing.Callable[[CollectionState], bool]
        | Rule
        | Rule[SPMWorldBase]
        | None = None,
        name: str | None = None,
        group: int = 0,
        type: EntranceType = EntranceType.TWO_WAY,
        force_creation: bool = False,
    ) -> Entrance | None:
        if from_region not in world.rm or to_region not in world.rm:
            return None
        entrance = world.create_entrance(
            world.rm[from_region], world.rm[to_region], rule, name, force_creation
        )
        if entrance is not None:
            entrance.randomization_group = group
            entrance.randomization_type = type
        return entrance

    all_entrances = [
        create_entrance(
            world, edata.fr, edata.to, edata.rule, edata.name, edata.group, edata.etype
        )
        for edata in ENTRANCE_RULES
    ]
    return [
        entrance
        for entrance in all_entrances
        if entrance is not None and entrance.randomization_group > 0
    ]


def randomize_entrances(
    world: SPMWorldBase, entrances: list[Entrance]
) -> ERPlacementState:
    _ = [
        disconnect_entrance_for_randomization(
            entrance, one_way_target_name=f"[ONE-WAY]{entrance.name}"
        )
        for entrance in entrances
    ]
    target_group_lookup = bake_target_group_lookup(world, er_anywhere)
    coupled = world.options.randomize_entrances.value == EntranceRando.option_coupled
    return er_randomize_entrances(world, coupled, target_group_lookup)


def set_rules(world: SPMWorldBase) -> None:
    world.set_completion_rule(Has(E.VICTORY))

    _ = [
        world.set_rule(world.lm[ldata.loc], ldata.rule)
        for ldata in LOCATION_RULES
        if ldata.loc in world.lm
    ]


class ERSettings(TypedDict):
    """This literally only exists to make ty happy with kwargs spread on EntranceRule"""

    group: EGroup | int
    etype: EntranceType


CHAPTER_DOOR_ER: ERSettings = {"group": 0, "etype": EntranceType.ONE_WAY}


ALL_RULES: list[EntranceRule | LocationRule] = [
    # region Chapter Doors
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.HE101,
        rule=HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_1_KEY),
        name="Flipside Tower - Red Door [1-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.HE201,
        rule=HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_2_KEY),
        name="Flipside Tower - Red Door [1-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.HE301,
        rule=HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_3_KEY),
        name="Flipside Tower - Red Door [1-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.HE401,
        rule=HasChapterKey(I.CHAPTER_1_KEY, I.CHAPTER_1_4_KEY),
        name="Flipside Tower - Red Door [1-4]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.MI101_BOTTOM_LEFT,
        rule=HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_1_KEY),
        name="Flipside Tower - Orange Door [2-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.MI201,
        rule=HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_2_KEY),
        name="Flipside Tower - Orange Door [2-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.MI301,
        rule=HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_3_KEY),
        name="Flipside Tower - Orange Door [2-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.MI401,
        rule=HasChapterKey(I.CHAPTER_2_KEY, I.CHAPTER_2_4_KEY),
        name="Flipside Tower - Orange Door [2-4]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.TA101,
        rule=HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_1_KEY),
        name="Flipside Tower - Yellow Door [3-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.TA201,
        rule=HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_2_KEY),
        name="Flipside Tower - Yellow Door [3-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.TA301,
        rule=HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_3_KEY),
        name="Flipside Tower - Yellow Door [3-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.TA401,
        rule=HasChapterKey(I.CHAPTER_3_KEY, I.CHAPTER_3_4_KEY),
        name="Flipside Tower - Yellow Door [3-4]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.SP101,
        rule=HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_1_KEY),
        name="Flipside Tower - Green Door [4-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.SP201,
        rule=HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_2_KEY),
        name="Flipside Tower - Green Door [4-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.SP301,
        rule=HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_3_KEY),
        name="Flipside Tower - Green Door [4-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.SP401,
        rule=HasChapterKey(I.CHAPTER_4_KEY, I.CHAPTER_4_4_KEY),
        name="Flipside Tower - Green Door [4-4]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.GN101,
        rule=HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_1_KEY),
        name="Flipside Tower - Cyan Door [5-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.GN201,
        rule=HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_2_KEY),
        name="Flipside Tower - Cyan Door [5-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.GN301,
        rule=HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_3_KEY),
        name="Flipside Tower - Cyan Door [5-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.GN401,
        rule=HasChapterKey(I.CHAPTER_5_KEY, I.CHAPTER_5_4_KEY),
        name="Flipside Tower - Cyan Door [5-4]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.WA101,
        rule=HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_1_KEY),
        name="Flipside Tower - Blue Door [6-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.WA201,
        rule=HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_2_KEY),
        name="Flipside Tower - Blue Door [6-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.WA301,
        rule=HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_3_KEY),
        name="Flipside Tower - Blue Door [6-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.WA401,
        rule=HasChapterKey(I.CHAPTER_6_KEY, I.CHAPTER_6_4_KEY),
        name="Flipside Tower - Blue Door [6-4]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.AN101,
        rule=HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_1_KEY),
        name="Flipside Tower - Purple Door [7-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.AN201,
        rule=HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_2_KEY),
        name="Flipside Tower - Purple Door [7-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.AN301,
        rule=HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_3_KEY),
        name="Flipside Tower - Purple Door [7-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.AN401,
        rule=HasChapterKey(I.CHAPTER_7_KEY, I.CHAPTER_7_4_KEY),
        name="Flipside Tower - Purple Door [7-4]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC12_L_TOWER,
        to=R.LS101,
        rule=HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_1_KEY)
        & HasGroupUnique("Pure Heart", count=FromOption(PureHeartsRequired)),
        name="Flopside Tower - Black Door [8-1]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC12_L_TOWER,
        to=R.LS201,
        rule=HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_2_KEY)
        & HasGroupUnique("Pure Heart", count=FromOption(PureHeartsRequired)),
        name="Flopside Tower - Black Door [8-2]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC12_L_TOWER,
        to=R.LS301,
        rule=HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_3_KEY)
        & HasGroupUnique("Pure Heart", count=FromOption(PureHeartsRequired)),
        name="Flopside Tower - Black Door [8-3]",
        **CHAPTER_DOOR_ER,
    ),
    EntranceRule(
        fr=R.MAC12_L_TOWER,
        to=R.LS401,
        rule=HasChapterKey(I.CHAPTER_8_KEY, I.CHAPTER_8_4_KEY)
        & HasGroupUnique("Pure Heart", count=FromOption(PureHeartsRequired)),
        name="Flopside Tower - Black Door [8-4]",
        **CHAPTER_DOOR_ER,
    ),
    # endregion
    # region Flipside
    EntranceRule(
        fr=R.MAC02_L_TOWER,
        to=R.MAC01_LAYER1,
        name="Flipside Tower - Fall",
        group=EGroup.HUB,
        etype=EntranceType.ONE_WAY,
    ),
    EntranceRule(
        fr=R.MAC02_L_TOWER, to=R.MAC02_LAYER1, name="Flipside Tower - Elevator Down"
    ),
    EntranceRule(
        fr=R.MAC01_LAYER1,
        to=R.MAC02_LAYER1,
        name="Flipside 3F - Layer 1 - Elevator Down",
        group=EGroup.HUB,
    ),
    LocationRule(L.FLIPSIDE_HEART_PILLAR_RED, Has(I.RED_PURE_HEART)),
    # MOD: will this require spicy soup in the itempool?
    LocationRule(L.FLIPSIDE_3F_EAT_A_SPICY_SOUP, True_()),
    LocationRule(L.FLEEP_MAP_REVEAL_01, CanFleepTreasureSpot(I.MAP_1)),
    EntranceRule(
        fr=R.MAC01_LAYER2,
        to=R.MAC02_LAYER2,
        name="Flipside 3F - Layer 2 - Pipe",
        group=EGroup.HUB,
    ),
    LocationRule(L.FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS, Has(I.PIXL_TIPPI)),
    LocationRule(L.FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK, Has(I.PIXL_PICCOLO)),
    EntranceRule(
        fr=R.MAC02_LAYER1, to=R.MAC02_L_TOWER, name="Flipside Tower - Elevator Up"
    ),
    # MOD: This elevator doesn't work until GSW(0, 53), after chapter 1-4 cleared, before intermission
    EntranceRule(
        fr=R.MAC02_LAYER1,
        to=R.MAC09_LAYER3,
        name="Flipside 2F - Layer 1 - Elevator Down",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC02_LAYER1,
        to=R.MAC01_LAYER1,
        name="Flipside 2F - Layer 1 - Elevator Up",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC02_LAYER1,
        to=R.MAC05_LAYER1,
        rule=SPMRules.can_flip,
        name="Flipside 2F - Layer 1 - Left Blue Pipe",
    ),
    EntranceRule(
        fr=R.MAC02_LAYER1,
        to=R.MAC12_LAYER1,
        name="Flipside 2F - Layer 1 - Right Blue Pipe",
    ),
    EntranceRule(
        fr=R.MAC02_LAYER1,
        to=R.MAC02_LAYER2,
        rule=SPMRules.can_flip & Has(I.OLD_KEY),
        name="Flipside 2F - Layer 1 -> 2",
    ),
    LocationRule(L.PICCOLO_FETCH_MERLUVLEE, Has(I.TRAINING_MACHINE)),
    EntranceRule(
        fr=R.MAC02_LAYER2,
        to=R.MAC01_LAYER2,
        rule=SPMRules.can_break_hard_blocks,
        name="Flipside 2F - Layer 2 - Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC02_LAYER2,
        to=R.MAC02_LAYER3,
        rule=SPMRules.can_flip,
        name="Flipside 2F - Layer 2 -> 3",
    ),
    EntranceRule(
        fr=R.MAC02_LAYER3,
        to=R.MAC06_LAYER1,
        name="Flipside 2F Outskirts - Layer 3 - Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC02_LAYER3,
        to=R.MAC02_LAYER2,
        rule=SPMRules.can_flip,
        name="Flipside 2F - Layer 3 -> 2",
    ),
    LocationRule(
        L.FLIPSIDE_HEART_PILLAR_GREEN, HasAll(I.PIXL_THUDLEY, I.GREEN_PURE_HEART)
    ),
    EntranceRule(
        fr=R.MAC03_LAYER1,
        to=R.MAC09_LAYER1,
        name="Flipside 1F - Mirror Hall - Right Door",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC03_LAYER1,
        to=R.MAC03_LAYER2,
        rule=SPMRules.can_flip,
        name="Flipside 1F - Mirror Hall - Layer 1 -> 2",
    ),
    LocationRule(L.FLEEP_MAP_REVEAL_02, CanFleepTreasureSpot(I.MAP_2)),
    EntranceRule(
        fr=R.MAC04_LAYER1,
        to=R.MAC04_ITTY_BITS,
        rule=Has(I.PIXL_DOTTIE),
        name="Flipside B1 - Shrink to Itty Bits",
    ),
    EntranceRule(
        fr=R.MAC04_LAYER1,
        to=R.MAC04_BAR,
        rule=SPMRules.can_flip,
        name="Flipside B1 - Flip to Bar's backrooms",
    ),
    LocationRule(L.FLIPSIDE_B1_3D_CHEST, SPMRules.can_flip),
    LocationRule(L.FLEEP_MAP_REVEAL_03, CanFleepTreasureSpot(I.MAP_3)),
    EntranceRule(
        fr=R.MAC04_BAR,
        to=R.MAC30,
        name="Flipside B1 - Bar's backroom pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(fr=R.MAC04_BAR, to=R.MAC04_LAYER1, name="Flipside B1 - Bar's flip"),
    EntranceRule(
        fr=R.MAC05_LAYER1,
        to=R.MAC04_LAYER1,
        name="Flipside B2 - Layer 1 - Elevator Up",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC05_LAYER1,
        to=R.MAC02_LAYER1,
        rule=SPMRules.can_flip,
        name="Flipside B2 - Layer 1 - Blue Pipe",
        group=EGroup.HUB,
    ),
    # TODO: more access logic for individual floors
    EntranceRule(
        fr=R.MAC05_LAYER1,
        to=R.L_FLIPSIDE_PIT,
        rule=Has(
            E.SWITCH_FLIPSIDE_PIT_CAGE, options=[SPMRules.flipside_pit_access_filter]
        ),
        name="Flipside B2 - Layer 1 - Sealed Pipe",
    ),
    EntranceRule(
        fr=R.MAC05_LAYER1,
        to=R.L_FLIPSIDE_PIT_TOP,
        rule=SPMRules.can_super_jump | Has(E.SWITCH_FLIPSIDE_PIT_CAGE),
        name="Flipside B2 - Layer 1 -> Cage",
    ),
    EntranceRule(
        fr=R.L_FLIPSIDE_PIT_TOP,
        to=R.MAC05_LAYER2,
        rule=SPMRules.can_flip,
        name="Flipside B2 - Layer 1 Cage -> 2",
    ),
    EntranceRule(
        fr=R.MAC05_LAYER2,
        to=R.L_FLIPSIDE_PIT_TOP,
        rule=HasAll(I.CHARACTER_MARIO, I.PIXL_TIPPI),
        name="Flipside B2 Outskirts - Layer 2 -> 1 Cage",
    ),
    EntranceRule(
        fr=R.MAC05_LAYER2,
        to=R.MAC07_LAYER2,
        name="Flipside B2 Outskirts - Layer 2 - Pipe",
        group=EGroup.HUB,
    ),
    LocationRule(
        L.FLIPSIDE_B2_CHEST_AFTER_PIPE, Has(E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK)
    ),
    EntranceRule(
        fr=R.MAC06_LAYER1,
        to=R.MAC02_LAYER3,
        name="Flipside 1F Outskirts - Layer 1 - Right Pipe",
        group=EGroup.HUB,
    ),
    # Bowser *barely* has enough room to stand to break the blocks
    EntranceRule(
        fr=R.MAC06_LAYER1,
        to=R.MAC07_LAYER2,
        rule=SPMRules.can_break_hard_blocks,
        name="Flipside 1F Outskirts - Layer 1 - Left Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC06_LAYER1,
        to=R.MAC08,
        name="Flipside 1F Outskirts - Layer 1 - Chasm Fall",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC06_LAYER1,
        to=R.MAC06_LAYER2,
        rule=SPMRules.can_flip,
        name="Flipside 1F Outskirts - Layer 1 -> 2",
    ),
    EntranceRule(
        fr=R.MAC06_LAYER2,
        to=R.MAC06_LAYER1,
        rule=SPMRules.can_flip,
        name="Flipside 1F Outskirts - Layer 2 -> 1",
    ),
    LocationRule(
        L.FLIPSIDE_HEART_PILLAR_ORANGE,
        (SPMRules.can_float | SPMRules.throeau_jump) & Has(I.ORANGE_PURE_HEART),
    ),
    EntranceRule(
        fr=R.MAC07_LAYER2,
        to=R.MAC05_LAYER2,
        name="Flipside B1 Outskirts - Layer 1 - Right Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC07_LAYER2,
        to=R.MAC06_LAYER1,
        name="Flipside B1 Outskirts - Layer 1 - Left Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC07_LAYER2,
        to=R.MAC07_LAYER1,
        rule=SPMRules.can_flip & Has(E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK),
        name="Flipside B1 Outskirts - Layer 2 -> 1",
    ),
    LocationRule(
        L.FLIPSIDE_HEART_PILLAR_YELLOW,
        SPMRules.can_flip & HasAll(I.YELLOW_PURE_HEART, I.PIXL_SLIM),
    ),
    EntranceRule(
        fr=R.MAC08, to=R.MAC06_LAYER1, name="Flipside 1F - Jump Out", group=EGroup.HUB
    ),
    EntranceRule(
        fr=R.MAC09_LAYER1,
        to=R.MAC03_LAYER1,
        name="Flipside 1F - Door",
        group=EGroup.HUB,
    ),
    # Standing outside Mirror Hall, you don't need Fleep. You just walk thru the wall
    EntranceRule(
        fr=R.MAC09_LAYER1,
        to=R.MAC09_LAYER2,
        rule=SPMRules.can_flip,
        name="Flipside 1F - Layer 1 -> 2",
    ),
    EntranceRule(
        fr=R.MAC09_LAYER2,
        to=R.MAC09_LAYER1,
        rule=Has(I.PIXL_FLEEP) & SPMRules.can_flip,
        name="Flipside 1F - Layer 2 -> 1",
    ),
    EntranceRule(
        fr=R.MAC09_LAYER2,
        to=R.MAC09_LAYER3,
        rule=Has(I.PIXL_BOOMER) & SPMRules.can_flip,
        name="Flipside 1F - Layer 2 -> 3",
    ),
    EntranceRule(
        fr=R.MAC09_LAYER3,
        to=R.MAC02_LAYER1,
        name="Flipside 1F - Elevator Up",
        group=EGroup.HUB,
    ),
    # MOD: This elevator only works starting at GSW(0, 73), getting boomer
    EntranceRule(
        fr=R.MAC09_LAYER3,
        to=R.MAC04_LAYER1,
        rule=True_(),
        name="Flipside 1F - Elevator Down",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC09_LAYER3,
        to=R.MAC09_LAYER2,
        rule=Has(I.PIXL_BOOMER) & SPMRules.can_flip,
        name="Flipside 1F - Layer 3 -> 2",
    ),
    # endregion
    # region Flopside
    EntranceRule(
        fr=R.MAC12_L_TOWER,
        to=R.MAC11_LAYER1,
        name="Flopside Tower - Fall",
        etype=EntranceType.ONE_WAY,
    ),
    EntranceRule(
        fr=R.MAC12_L_TOWER, to=R.MAC12_LAYER1, name="Flopside Tower - Elevator Down"
    ),
    EntranceRule(
        fr=R.MAC11_LAYER1,
        to=R.MAC12_LAYER1,
        name="Flopside 3F - Layer 1 - Elevator Down",
        group=EGroup.HUB,
    ),
    LocationRule(L.FLOPSIDE_HEART_PILLAR_CYAN, Has(I.CYAN_PURE_HEART)),
    LocationRule(L.FLEEP_MAP_REVEAL_05, CanFleepTreasureSpot(I.MAP_5)),
    EntranceRule(
        fr=R.MAC11_LAYER2,
        to=R.MAC12_LAYER2,
        name="Flopside 3F - Layer 2 - Right Pipe",
        group=EGroup.HUB,
    ),
    LocationRule(L.FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK, Has(I.PIXL_PICCOLO)),
    LocationRule(L.FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS, Has(I.PIXL_TIPPI)),
    EntranceRule(
        fr=R.MAC12_LAYER1, to=R.MAC12_L_TOWER, name="Flopside Tower - Elevator Up"
    ),
    EntranceRule(
        fr=R.MAC12_LAYER1,
        to=R.MAC11_LAYER1,
        name="Flopside 2F - Layer 1 - Elevator Up",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER1,
        to=R.MAC19_LAYER3,
        name="Flopside 2F - Layer 1 - Elevator Down",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER1,
        to=R.MAC15_LAYER1,
        name="Flopside 2F - Layer 1 - Left Blue Pipe",
        rule=SPMRules.can_flip,
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER1,
        to=R.MAC02_LAYER1,
        name="Flopside 2F - Layer 1 - Right Blue Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER1,
        to=R.MAC12_LAYER2,
        name="Flopside 2F - Layer 1 -> 2",
        rule=SPMRules.can_flip,
    ),
    LocationRule(L.PICCOLO_FETCH_MERLEE, Has(I.CRYSTAL_BALL)),
    EntranceRule(
        fr=R.MAC12_LAYER2,
        to=R.MAC11_LAYER2,
        name="Flopside 2F - Layer 2 - Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER2,
        to=R.MAC12_LAYER1,
        name="Flopside 2F - Layer 2 -> 1",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER2,
        to=R.MAC12_LAYER3,
        name="Flopside 2F - Layer 2 -> 3",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER3,
        to=R.MAC16_LAYER1,
        name="Flopside 2F - Layer 3 - Blocked Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC12_LAYER3,
        to=R.MAC12_LAYER2,
        name="Flopside 2F - Layer 3 -> 2",
        rule=SPMRules.can_flip,
    ),
    LocationRule(L.FLOPSIDE_HEART_PILLAR_WHITE, Has(I.WHITE_PURE_HEART)),
    EntranceRule(
        fr=R.MAC14_RIGHT,
        to=R.MAC15_LAYER1,
        name="Flopside B1 - Elevator Down",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC14_RIGHT,
        to=R.MAC19_LAYER3,
        name="Flopside B1 - Elevator Up",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC14_RIGHT,
        to=R.MAC14_LEFT,
        name="Flopside B1 - Right -> Left",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(
        fr=R.MAC14_RIGHT,
        to=R.MAC14_L_BACK_BEVERAGARIUM,
        name="Flopside B1 - Beveragarium",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(
        fr=R.MAC14_LEFT,
        to=R.MAC14_L_ITTY_BITS,
        name="Flopside B1 - Itty Bits",
        rule=Has(I.PIXL_DOTTIE),
    ),
    EntranceRule(
        fr=R.MAC14_LEFT,
        to=R.MAC14_RIGHT,
        name="Flopside B1 - Left -> Right",
        rule=SPMRules.can_flip,
    ),
    # TODO: More access rules
    EntranceRule(
        fr=R.MAC15_LAYER1,
        to=R.L_FLOPSIDE_PIT,
        name="Flopside B2 - Layer 1 - Sealed Pipe",
        rule=False_(),
    ),
    EntranceRule(
        fr=R.MAC15_LAYER1,
        to=R.MAC12_LAYER1,
        name="Flopside B2 - Layer 2 - Blue Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC15_LAYER1,
        to=R.L_FLOPSIDE_PIT_TOP,
        name="Flopside B2 - Layer 1 -> Top of Cage",
        rule=SPMRules.can_super_jump,
    ),
    EntranceRule(
        fr=R.MAC15_LAYER1,
        to=R.MAC14_RIGHT,
        name="Flopside B2 - Layer 1 - Elevator Up",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC15_LAYER2,
        to=R.MAC18,
        name="Flopside B2 - Layer 2 - Chasm Fall",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC15_LAYER2,
        to=R.MAC17_LAYER2,
        name="Flopside B2 - Layer 2 - Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC15_LAYER2,
        to=R.L_FLOPSIDE_PIT_TOP,
        name="Flopside B2 - Layer 2 - Cage Top",
        rule=(SPMRules.can_super_jump | Has(I.PIXL_TIPPI)) & SPMRules.can_flip,
    ),
    LocationRule(
        E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK, SPMRules.can_flip & Has(I.PIXL_CUDGE)
    ),
    LocationRule(
        L.FLOPSIDE_B2_CHEST_AFTER_PIPE, Has(E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK)
    ),
    EntranceRule(
        fr=R.L_FLOPSIDE_PIT_TOP, to=R.MAC15_LAYER1, name="Flopside B2 Cage Top - Drop"
    ),
    EntranceRule(
        fr=R.L_FLOPSIDE_PIT_TOP,
        to=R.MAC15_LAYER2,
        name="Flopside B2 Cage Top - Layer 2",
    ),
    LocationRule(E.FLEEP_FLOPSIDE_PIT_CAGE, Has(I.PIXL_FLEEP)),
    EntranceRule(
        fr=R.MAC16_LAYER1,
        to=R.MAC12_LAYER3,
        name="Flopside 1F Outskirts - Layer 1 - Left Blocked Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC16_LAYER1,
        to=R.MAC17_LAYER1,
        name="Flopside 1F Outskirts - Layer 1 - Right Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC16_LAYER1,
        to=R.MAC16_LAYER2,
        name="Flopside 1F Outskirts - Layer 1 -> 2",
    ),
    EntranceRule(
        fr=R.MAC16_LAYER2,
        to=R.MAC16_LAYER1,
        name="Flopside 1F Outskirts - Layer 2 -> 1",
    ),
    LocationRule(L.FLOPSIDE_HEART_PILLAR_BLUE, Has(I.BLUE_PURE_HEART)),
    EntranceRule(
        fr=R.MAC17_LAYER2,
        to=R.MAC15_LAYER2,
        name="Flopside B1 Outskirts - Left Pipe",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC17_LAYER2,
        to=R.MAC16_LAYER1,
        name="Flopside B1 Outskirts - Right Pipe",
        group=EGroup.HUB,
    ),
    # TODO: More access rules
    EntranceRule(
        fr=R.MAC17_LAYER2,
        to=R.MAC17_LAYER1,
        name="Flopside B1 Outskirts - Layer 2 -> 1",
        rule=SPMRules.can_flip & Has(I.CHARACTER_LUIGI),
    ),
    LocationRule(
        L.FLOPSIDE_HEART_PILLAR_PURPLE, HasAll(I.PURPLE_PURE_HEART, I.CHARACTER_LUIGI)
    ),
    LocationRule(E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK, Has(I.PIXL_CUDGE)),
    EntranceRule(
        fr=R.MAC18, to=R.MAC15_LAYER1, name="Flopside B2 - Jump Out", group=EGroup.HUB
    ),
    EntranceRule(
        fr=R.MAC19_LAYER1,
        to=R.MAC03_LAYER2,
        name="Flopside 1F - Layer 1 - Door",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC19_LAYER1,
        to=R.MAC19_LAYER2,
        name="Flopside 1F - Layer 1 -> 2",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(
        fr=R.MAC19_LAYER2,
        to=R.MAC19_LAYER1,
        name="Flopside 1F - Layer 2 -> 1",
        rule=SPMRules.can_flip & Has(I.PIXL_FLEEP),
    ),
    EntranceRule(
        fr=R.MAC19_LAYER2,
        to=R.MAC19_LAYER3,
        name="Flopside 1F - Layer 2 -> 3",
        rule=SPMRules.can_flip & Has(I.PIXL_BOOMER),
    ),
    EntranceRule(
        fr=R.MAC19_LAYER3,
        to=R.MAC12_LAYER1,
        name="Flopside 1F - Layer 3 - Elevator Up",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC19_LAYER3,
        to=R.MAC14_RIGHT,
        name="Flopside 1F - Layer 3 - Elevator Down",
        group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC19_LAYER3, to=R.MAC19_LAYER2, name="Flopside 1F - Layer 3 -> 2"
    ),
    EntranceRule(
        fr=R.MAC03_LAYER2,
        to=R.MAC19_LAYER1,
        name="Flopside 1F - Mirror Hall - Left Door",
        # group=EGroup.HUB,
    ),
    EntranceRule(
        fr=R.MAC03_LAYER2,
        to=R.MAC03_LAYER1,
        name="Flipside 1F - Mirror Hall - Layer 2 -> 1",
    ),
    LocationRule(L.FLEEP_MAP_REVEAL_04, CanFleepTreasureSpot(I.MAP_4)),
    # endregion
    # region Chapter 1-1
    # TODO: ER settings
    EntranceRule(
        fr=R.HE101,
        to=R.HE106,
        rule=Has(I.PIXL_TIPPI),
        name=f"{R.HE101} - Bestovius' House, Hidden Door",
    ),
    EntranceRule(
        fr=R.HE101, to=R.HE103, name=f"{R.HE101} - Front Pipe near Bestovius' House"
    ),
    EntranceRule(
        fr=R.HE101, to=R.HE102, name=f"{R.HE101} - Sealed Door", rule=SPMRules.can_flip
    ),
    LocationRule(L.C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY, SPMRules.can_flip),
    LocationRule(L.FLEEP_MAP_REVEAL_06, CanFleepTreasureSpot(I.MAP_6)),
    EntranceRule(fr=R.HE102, to=R.HE101, name=f"{R.HE102} - Left Door"),
    EntranceRule(
        fr=R.HE102,
        to=R.HE104,
        name=f"{R.HE102} - Right Door",
        rule=SPMRules.can_flip | SPMRules.can_float,
    ),
    LocationRule(L.C11_OPEN_ITEM_BEHIND_PIPE, SPMRules.can_flip),
    EntranceRule(fr=R.HE103, to=R.HE101, name=f"{R.HE103} - Right Pipe"),
    EntranceRule(fr=R.HE104, to=R.HE102, name=f"{R.HE104} - Left Door"),
    EntranceRule(
        fr=R.HE104,
        to=R.HE105,
        name=f"{R.HE104} - Right Door",
        rule=SPMRules.can_flip | SPMRules.can_super_jump,
    ),
    EntranceRule(fr=R.HE105, to=R.HE104, name=f"{R.HE105} - Left Door"),
    LocationRule(L.C11_CHEST_AFTER_STAR_BLOCK, SPMRules.can_flip),
    EntranceRule(fr=R.HE106, to=R.HE101, name=f"{R.HE106} - Door"),
    LocationRule(L.C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM, SPMRules.can_flip),
    LocationRule(L.C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM, SPMRules.can_flip),
    # endregion
    # region Chapter 1-2
    EntranceRule(fr=R.HE201, to=R.HE202, name=f"{R.HE201} - Right Door"),
    EntranceRule(
        fr=R.HE201,
        to=R.HE202,
        name=f"{R.HE201} - Hidden Shortcut Door",
        rule=SPMRules.can_flip,
    ),
    LocationRule(L.C12_CHEST_IN_SHORTCUT, SPMRules.can_flip),
    LocationRule(L.FLEEP_MAP_REVEAL_07, CanFleepTreasureSpot(I.MAP_7)),
    EntranceRule(fr=R.HE202, to=R.HE201, name=f"{R.HE202} - Left Door"),
    EntranceRule(
        fr=R.HE202,
        to=R.HE203,
        name=f"{R.HE202} - Right Door",
        rule=SPMRules.can_flip
        | (SPMRules.can_float & SPMRules.can_super_jump & Has(I.PIXL_DASHELL)),
    ),
    EntranceRule(
        fr=R.HE203,
        to=R.HE208,
        name=f"{R.HE203} - Pipe behind bricks",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(
        fr=R.HE203,
        to=R.HE206,
        name=f"{R.HE203} - Pipe in house behind partition",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(fr=R.HE203, to=R.HE202, name=f"{R.HE203} - Left Door"),
    EntranceRule(fr=R.HE203, to=R.HE204, name=f"{R.HE203} - Red's House"),
    EntranceRule(
        fr=R.HE203,
        to=R.HE205,
        name=f"{R.HE203} - Green's House",
        rule=SPMRules.can_flip | SPMRules.can_float | Has(I.PIXL_DASHELL),
    ),
    LocationRule(
        L.C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE,
        SPMRules.can_flip | SPMRules.can_float | Has(I.PIXL_DASHELL),
    ),
    # MOD: Will Watchitt still require having Thoreau to tell Green to build the bridge?
    LocationRule(
        L.C12_STAR_BLOCK,
        (SPMRules.can_flip & Has(I.PIXL_THOREAU))
        | SPMRules.can_float
        | Has(I.PIXL_DASHELL),
    ),
    EntranceRule(fr=R.HE204, to=R.HE203, name=f"{R.HE204} - Door"),
    EntranceRule(fr=R.HE205, to=R.HE203, name=f"{R.HE205} - Door"),
    LocationRule(L.C12_OPEN_ITEM_BEHIND_GREENS_BED, SPMRules.can_flip),
    LocationRule(L.FLEEP_MAP_REVEAL_08, CanFleepTreasureSpot(I.MAP_8)),
    EntranceRule(fr=R.HE206, to=R.HE203, name=f"{R.HE206} - Left Pipe"),
    EntranceRule(fr=R.HE206, to=R.HE209, name=f"{R.HE206} - Right Door"),
    EntranceRule(
        fr=R.HE207, to=R.HE209, name=f"{R.HE207} - Door", rule=Has(I.PIXL_THOREAU)
    ),
    EntranceRule(fr=R.HE208, to=R.HE203, name=f"{R.HE208} - Door"),
    EntranceRule(fr=R.HE209, to=R.HE206, name=f"{R.HE209} - Left Door"),
    EntranceRule(
        fr=R.HE209, to=R.HE207, name=f"{R.HE209} - Right Door", rule=Has(I.PIXL_TIPPI)
    ),
    # endregion
    # region Chapter 1-3
    EntranceRule(fr=R.HE301, to=R.HE303, name=f"{R.HE301} - Door below red palm tree"),
    EntranceRule(fr=R.HE301, to=R.HE302, name=f"{R.HE301} - Right door"),
    LocationRule(L.C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM, SPMRules.can_flip),
    EntranceRule(fr=R.HE302, to=R.HE301, name=f"{R.HE302} - Left Door"),
    LocationRule(L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM, SPMRules.can_flip),
    LocationRule(L.FLEEP_MAP_REVEAL_09, CanFleepTreasureSpot(I.MAP_9)),
    # TODO: Double-check rules
    EntranceRule(
        fr=R.HE303,
        to=R.HE305,
        name=f"{R.HE303} - Pipe on floating bricks",
        rule=SPMRules.can_flip
        | SPMRules.can_float
        | Has(I.PIXL_DASHELL)
        | (Has(I.PIXL_THOREAU) & SPMRules.can_super_jump),
    ),
    EntranceRule(fr=R.HE303, to=R.HE301, name=f"{R.HE303} - Left Door"),
    EntranceRule(
        fr=R.HE303,
        to=R.HE304,
        name=f"{R.HE303} - Right Door",
        rule=SPMRules.can_flip
        | SPMRules.can_float
        | HasAny(I.PIXL_DASHELL, I.PIXL_THOREAU),
    ),
    EntranceRule(fr=R.HE304, to=R.HE303, name=f"{R.HE304} - Left Door"),
    EntranceRule(fr=R.HE304, to=R.HE306, name=f"{R.HE304} - Right Door"),
    EntranceRule(fr=R.HE305, to=R.HE303, name=f"{R.HE305} - Pipe"),
    EntranceRule(
        fr=R.HE306, to=R.HE307, name=f"{R.HE306} - Left door on floating bricks"
    ),
    EntranceRule(fr=R.HE306, to=R.HE304, name=f"{R.HE306} - Door on ground"),
    EntranceRule(
        fr=R.HE306, to=R.HE308, name=f"{R.HE306} - Right door on floating bricks"
    ),
    LocationRule(L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM, SPMRules.can_flip),
    EntranceRule(fr=R.HE307, to=R.HE306, name=f"{R.HE307} - Door"),
    LocationRule(L.FLEEP_MAP_REVEAL_10, CanFleepTreasureSpot(I.MAP_10)),
    EntranceRule(fr=R.HE308, to=R.HE306, name=f"{R.HE308} - Door"),
    # endregion
    # Chapter 1-4
    EntranceRule(fr=R.HE401, to=R.HE402, name=f"{R.HE401} - Door"),
    EntranceRule(fr=R.HE402, to=R.HE401, name=f"{R.HE402} - Left Door"),
    EntranceRule(fr=R.HE402, to=R.HE403, name=f"{R.HE402} - Right Door"),
    EntranceRule(fr=R.HE403, to=R.HE402, name=f"{R.HE403} - Left Door"),
    # MOD: Will ruins keys be split into 3 separate ids for each door? If so we don't need full key logic here for ER.
    EntranceRule(
        fr=R.HE403,
        to=R.HE405,
        name=f"{R.HE403} - Middle Door",
        rule=Has(
            I.RUINS_KEY,
            count=3,
            options=[OptionFilter(EntranceRando, Toggle.option_true)],
        )
        | Has(I.RUINS_KEY),
    ),
    EntranceRule(
        fr=R.HE403, to=R.HE404, name=f"{R.HE403} - Right Door", rule=SPMRules.can_flip
    ),
    EntranceRule(fr=R.HE404, to=R.HE403, name=f"{R.HE404} - Door"),
    EntranceRule(fr=R.HE405, to=R.HE403, name=f"{R.HE405} - Left Door"),
    EntranceRule(fr=R.HE405, to=R.HE406, name=f"{R.HE405} - Right Upper Door"),
    EntranceRule(
        fr=R.HE405,
        to=R.HE412,
        name=f"{R.HE405} - Right Lower Door",
        rule=Has(
            I.RUINS_KEY,
            count=3,
            options=[OptionFilter(EntranceRando, Toggle.option_true)],
        )
        | Has(I.RUINS_KEY, count=2),
    ),
    # MOD: THOREAU has to be patched to always be thrown at *Mario's* height!
    # Otherwise this has to be updated to always require mario.
    LocationRule(
        L.C14_OPEN_KEY_BEHIND_BLOCKS,
        HasAll(I.PIXL_THOREAU, E.SWITCH_YOLD_RUINS_SQUIG_ROOM),
    ),
    LocationRule(L.C14_OPEN_KEY_BEHIND_BLOCKS, SPMRules.can_flip),
    EntranceRule(fr=R.HE406, to=R.HE405, name=f"{R.HE406} - Door"),
    LocationRule(
        E.SWITCH_YOLD_RUINS_SQUIG_ROOM, SPMRules.can_luigi_jump | Has(I.PIXL_THOREAU)
    ),
    EntranceRule(fr=R.HE407, to=R.HE412, name=f"{R.HE407} - Left Door"),
    EntranceRule(
        fr=R.HE407,
        to=R.HE408,
        name=f"{R.HE407} - Right Door",
        rule=Has(I.RUINS_KEY, count=3),
    ),
    LocationRule(L.C14_HIDDEN_CHEST_AFTER_3D_PATH, SPMRules.can_flip),
    EntranceRule(fr=R.HE408, to=R.HE407, name=f"{R.HE408} - Lower Door"),
    EntranceRule(
        fr=R.HE408, to=R.HE409, name=f"{R.HE408} - Upper Door", rule=SPMRules.can_flip
    ),
    EntranceRule(fr=R.HE409, to=R.HE410, name=f"{R.HE409} - Pipe"),
    EntranceRule(fr=R.HE409, to=R.HE408, name=f"{R.HE409} - Door"),
    EntranceRule(fr=R.HE410, to=R.HE411, name=f"{R.HE410} - Door"),
    EntranceRule(fr=R.HE411, to=R.HE410, name=f"{R.HE411} - Door"),
    LocationRule(L.FLEEP_MAP_REVEAL_11, CanFleepTreasureSpot(I.MAP_11)),
    EntranceRule(fr=R.HE412, to=R.HE405, name=f"{R.HE412} - Left Door"),
    EntranceRule(
        fr=R.HE412, to=R.HE407, name=f"{R.HE412} - Right Door", rule=Has(I.PIXL_TIPPI)
    ),
    # endregion
    # region Chapter 2-1
    EntranceRule(
        fr=R.MI101_BOTTOM_LEFT,
        to=R.MI101_BOTTOM_RIGHT,
        name=f"{R.MI101_BOTTOM_LEFT} - Jump to Bottom Right Corner",
        rule=Or(SPMRules.can_float, HasAny(I.PIXL_DASHELL, I.PIXL_CARRIE)),
    ),
    EntranceRule(
        fr=R.MI101_BOTTOM_RIGHT,
        to=R.MI108,
        name=f"{R.MI101_BOTTOM_RIGHT} - Locked Door",
        rule=Has(I.DOOR_KEY_21),
    ),
    EntranceRule(
        fr=R.MI101_BOTTOM_RIGHT,
        to=R.MI101_BOTTOM_LEFT,
        name=f"{R.MI101_BOTTOM_RIGHT} - Fall to the Bottom Left",
    ),
    # Luigi doesn't need super jump
    EntranceRule(
        fr=R.MI101_BOTTOM_RIGHT,
        to=R.MI101_TOP_RIGHT,
        name=f"{R.MI101_BOTTOM_RIGHT} - Jump to Upper Platforms",
        rule=Or(
            SPMRules.can_flip | SPMRules.can_luigi_jump | SPMRules.multiple_bowser_bumps
        ),
    ),
    EntranceRule(fr=R.MI101_TOP_RIGHT, to=R.MI105, name=f"{R.MI101_TOP_RIGHT} - Pipe"),
    EntranceRule(
        fr=R.MI101_TOP_RIGHT,
        to=R.MI101_BOTTOM_RIGHT,
        name=f"{R.MI101_TOP_RIGHT} - Fall",
    ),
    EntranceRule(fr=R.MI102, to=R.MI110, name=f"{R.MI102} - Bottom Door"),
    EntranceRule(
        fr=R.MI102,
        to=R.MI110,  # TODO: split out this and the connection above for ER
        name=f"{R.MI102} - Top Door",
    ),
    LocationRule(
        E.SWITCH_GLOAM_VALLEY_UNDERGROUND, SPMRules.can_flip & Has(I.PIXL_BOOMER)
    ),
    EntranceRule(fr=R.MI103, to=R.MI110, name=f"{R.MI103} - Bottom Door"),
    EntranceRule(fr=R.MI103, to=R.MI110, name=f"{R.MI103} - Top Door"),
    EntranceRule(fr=R.MI104, to=R.MI110, name=f"{R.MI104} - Door"),
    LocationRule(L.C21_LEFT_CHEST_BEFORE_STAR_BLOCK, SPMRules.can_flip),
    LocationRule(L.C21_RIGHT_CHEST_BEFORE_STAR_BLOCK, SPMRules.can_flip),
    LocationRule(L.FLEEP_MAP_REVEAL_12, CanFleepTreasureSpot(I.MAP_12)),
    EntranceRule(fr=R.MI105, to=R.MI101_TOP_RIGHT, name=f"{R.MI105} - Pipe"),
    EntranceRule(fr=R.MI106, to=R.MI110, name=f"{R.MI106} - Right Pipe"),
    EntranceRule(fr=R.MI106, to=R.MI107, name=f"{R.MI106} - Left Pipe"),
    EntranceRule(fr=R.MI107, to=R.MI106, name=f"{R.MI107} - Pipe"),
    LocationRule(
        L.C21_CHEST_BEHIND_BOOMER_CHEST, SPMRules.can_flip & Has(I.PIXL_BOOMER)
    ),
    EntranceRule(fr=R.MI108, to=R.MI101_BOTTOM_RIGHT, name=f"{R.MI108} - Left Door"),
    EntranceRule(fr=R.MI108, to=R.MI109, name=f"{R.MI108} - Middle Door"),
    EntranceRule(
        fr=R.MI108,
        to=R.MI111,
        name=f"{R.MI108} - Right Door",
        rule=Has(E.SWITCH_GLOAM_VALLEY_BACKGROUND),
    ),
    LocationRule(
        E.SWITCH_GLOAM_VALLEY_BACKGROUND, SPMRules.can_float | Has(I.PIXL_DASHELL)
    ),
    EntranceRule(fr=R.MI109, to=R.MI108, name=f"{R.MI109} - Door"),
    EntranceRule(
        fr=R.MI110, to=R.MI106, name=f"{R.MI110} - Pipe", rule=SPMRules.mi110_door_group
    ),
    EntranceRule(
        fr=R.MI110,
        to=R.MI111,
        name=f"{R.MI110} - Ground Door",
        rule=SPMRules.mi110_door_group,
    ),
    EntranceRule(
        fr=R.MI110,
        to=R.MI104,
        name=f"{R.MI110} - Left Elevated Door (Switch)",
        rule=SPMRules.mi110_door_group,
    ),
    EntranceRule(
        fr=R.MI110,
        to=R.MI102,
        name=f"{R.MI110} - Middle Left Elevated Door",
        rule=SPMRules.mi110_door_group,
    ),
    EntranceRule(
        fr=R.MI110,
        to=R.MI103,
        name=f"{R.MI110} - Middle Elevated Door",
        rule=SPMRules.mi110_door_group,
    ),
    EntranceRule(fr=R.MI111, to=R.MI108, name=f"{R.MI111} - Left Door"),
    EntranceRule(fr=R.MI111, to=R.MI110, name=f"{R.MI111} - Right Door"),
    # endregion
    # region Chapter 2-2
    EntranceRule(fr=R.MI201, to=R.MI202, name=f"{R.MI201} - Mansion Front Door"),
    LocationRule(L.C22_CHEST_ON_ROOF, SPMRules.can_flip),
    LocationRule(L.FLEEP_MAP_REVEAL_13, CanFleepTreasureSpot(I.MAP_13)),
    EntranceRule(fr=R.MI202, to=R.MI201, name=f"{R.MI202} - Mansion Front Door"),
    EntranceRule(
        fr=R.MI202,
        to=R.MI203,
        name=f"{R.MI202} - Door Behind Curtains",
        rule=SPMRules.can_flip,
    ),
    EntranceRule(fr=R.MI203, to=R.MI202, name=f"{R.MI203} - Far Left Door"),
    EntranceRule(fr=R.MI203, to=R.MI207, name=f"{R.MI203} - Bottom Right, Left Door"),
    EntranceRule(fr=R.MI203, to=R.MI204, name=f"{R.MI203} - Top Right, Left Door"),
    EntranceRule(fr=R.MI203, to=R.MI205, name=f"{R.MI203} - Top Right, Middle Door"),
    EntranceRule(fr=R.MI203, to=R.MI206, name=f"{R.MI203} - Top Right, Right Door"),
    EntranceRule(
        fr=R.MI203,
        to=R.MI208,
        name=f"{R.MI203} - Bottom Right, Right Door",
        rule=Has(I.HOUSE_KEY),
    ),
    LocationRule(L.FLEEP_MAP_REVEAL_14, CanFleepTreasureSpot(I.MAP_14)),
    EntranceRule(fr=R.MI204, to=R.MI203, name=f"{R.MI204} - Door"),
    # , etype=EntranceType.ONE_WAY
    EntranceRule(fr=R.MI204, to=R.MI209, name=f"{R.MI204} - Pit Trap"),
    EntranceRule(fr=R.MI205, to=R.MI203, name=f"{R.MI205} - Door"),
    # , etype=EntranceType.ONE_WAY
    EntranceRule(fr=R.MI205, to=R.MI210, name=f"{R.MI205} - Pit Trap"),
    EntranceRule(fr=R.MI206, to=R.MI203, name=f"{R.MI206} - Door"),
    LocationRule(
        L.C22_CHEST_ABOVE_SPIKE_ROOF,
        SPMRules.can_flip & (HasAny(I.PIXL_BOOMER, I.PIXL_CUDGE) | SPMRules.can_fire),
    ),
    EntranceRule(fr=R.MI207, to=R.MI203, name=f"{R.MI207} - Door"),
    # , etype=EntranceType.ONE_WAY
    EntranceRule(fr=R.MI207, to=R.MI211, name=f"{R.MI207} - Pit Trap"),
    EntranceRule(fr=R.MI208, to=R.MI203, name=f"{R.MI208} - Door"),
    # Need boomer to defeat the shlurp
    EntranceRule(
        fr=R.MI209, to=R.MI204, name=f"{R.MI209} - Pipe", rule=Has(I.PIXL_BOOMER)
    ),
    # Bowser can hit the switcEntranceRule(from a distance while carrie zooms him out just barely fast enough
    # Anyone can hit the switch and zoom out with dashell in time
    EntranceRule(
        fr=R.MI210,
        to=R.MI205,
        name=f"{R.MI210} - Pipe",
        rule=(SPMRules.can_fire & Has(I.PIXL_CARRIE))
        | HasAny(I.PIXL_BOOMER, I.PIXL_DASHELL),
    ),
    # Same as above
    EntranceRule(
        fr=R.MI211,
        to=R.MI207,
        name=f"{R.MI211} - Pipe",
        rule=(SPMRules.can_fire & Has(I.PIXL_CARRIE))
        | HasAny(I.PIXL_BOOMER, I.PIXL_DASHELL),
    ),
    # endregion
    # region Chapter 2-3
    EntranceRule(fr=R.MI301, to=R.MI302, name=f"{R.MI301} - Top Left Door"),
    EntranceRule(fr=R.MI301, to=R.MI303, name=f"{R.MI301} - Top Middle Door"),
    EntranceRule(fr=R.MI301, to=R.MI304, name=f"{R.MI301} - Top Right Door"),
    EntranceRule(
        fr=R.MI301,
        to=R.MI305,
        name=f"{R.MI301} - Lower Left Door",
        rule=SPMRules.can_float | HasAny(I.PIXL_CARRIE, I.PIXL_DASHELL),
    ),
    EntranceRule(fr=R.MI301, to=R.MI306, name=f"{R.MI301} - Lower Right Door"),
    LocationRule(E.OPEN_THE_RUBEE_VAULT, SPMRules.can_flip & Has(I.PIXL_SLIM)),
    EntranceRule(fr=R.MI302, to=R.MI301, name=f"{R.MI302} - Door"),
    EntranceRule(fr=R.MI303, to=R.MI301, name=f"{R.MI303} - Door"),
    EntranceRule(fr=R.MI304, to=R.MI301, name=f"{R.MI304} - Door"),
    EntranceRule(fr=R.MI305, to=R.MI301, name=f"{R.MI305} - Door"),
    EntranceRule(fr=R.MI306, to=R.MI301, name=f"{R.MI306} - Door"),
    LocationRule(L.C23_STAR_BLOCK, Has(E.OPEN_THE_RUBEE_VAULT)),
    LocationRule(L.FLEEP_MAP_REVEAL_15, CanFleepTreasureSpot(I.MAP_15)),
    # endregion
    # region Chapter 2-4
    # this chapter has to have the most connections of all time
    EntranceRule(fr=R.MI401, to=R.MI402, name=f"{R.MI401} - Left Door"),
    EntranceRule(fr=R.MI401, to=R.MI403, name=f"{R.MI401} - Right Door"),
    LocationRule(L.FLEEP_MAP_REVEAL_16, CanFleepTreasureSpot(I.MAP_16)),
    EntranceRule(fr=R.MI402, to=R.MI401, name=f"{R.MI402} - Left Door"),
    EntranceRule(fr=R.MI402, to=R.MI404, name=f"{R.MI402} - Right Door"),
    EntranceRule(fr=R.MI403, to=R.MI401, name=f"{R.MI403} - Bottom Left Door"),
    EntranceRule(fr=R.MI403, to=R.MI404, name=f"{R.MI403} - Bottom Right Door"),
    EntranceRule(fr=R.MI403, to=R.MI405, name=f"{R.MI403} - Top Right Door"),
    EntranceRule(fr=R.MI404, to=R.MI406, name=f"{R.MI404} - Top Left Door"),
    EntranceRule(fr=R.MI404, to=R.MI402, name=f"{R.MI404} - Middle Floating Door"),
    EntranceRule(fr=R.MI404, to=R.MI403, name=f"{R.MI404} - Bottom Right Door"),
    EntranceRule(fr=R.MI405, to=R.MI403, name=f"{R.MI405} - Left Door"),
    EntranceRule(fr=R.MI405, to=R.MI406, name=f"{R.MI405} - Right Door"),
    EntranceRule(fr=R.MI406, to=R.MI409, name=f"{R.MI406} - Top Right Door"),
    EntranceRule(fr=R.MI406, to=R.MI405, name=f"{R.MI406} - Bottom Right Door"),
    EntranceRule(fr=R.MI406, to=R.MI404, name=f"{R.MI406} - Bottom Left Door"),
    EntranceRule(fr=R.MI407, to=R.MI408, name=f"{R.MI407} - Top Left Door"),
    EntranceRule(fr=R.MI407, to=R.MI410, name=f"{R.MI407} - Top Right Door"),
    EntranceRule(fr=R.MI407, to=R.MI409, name=f"{R.MI407} - Bottom Left Door"),
    EntranceRule(fr=R.MI408, to=R.MI410, name=f"{R.MI408} - Top Left Door"),
    EntranceRule(fr=R.MI408, to=R.MI411, name=f"{R.MI408} - Top Right Door"),
    EntranceRule(fr=R.MI408, to=R.MI407, name=f"{R.MI408} - Bottom Left Door"),
    EntranceRule(fr=R.MI408, to=R.MI410, name=f"{R.MI408} - Bottom Right Door"),
    EntranceRule(fr=R.MI409, to=R.MI406, name=f"{R.MI409} - Left Door"),
    EntranceRule(fr=R.MI409, to=R.MI407, name=f"{R.MI409} - Bottom Door"),
    # MI409 Top door can't be entered
    EntranceRule(fr=R.MI410, to=R.MI408, name=f"{R.MI410} - Top Left Door"),
    EntranceRule(fr=R.MI410, to=R.MI411, name=f"{R.MI410} - Top Right Door"),
    EntranceRule(fr=R.MI410, to=R.MI408, name=f"{R.MI410} - Bottom Left Door"),
    EntranceRule(fr=R.MI410, to=R.MI407, name=f"{R.MI410} - Bottom Right Door"),
    LocationRule(
        L.C24_OPEN_ITEM_BEHIND_ROOM_08_SIGN, SPMRules.can_flip & Has(I.PIXL_BOOMER)
    ),
    EntranceRule(fr=R.MI411, to=R.MI415, name=f"{R.MI411} - Top Left Door"),
    # TODO: double-check, i don't think this door can be entered
    # EntranceRule(fr=R.MI411
    # , to=R.MI411
    # , name=f"{R.MI411} - Top Right Door"
    # ),
    EntranceRule(fr=R.MI411, to=R.MI410, name=f"{R.MI411} - Bottom Left Door"),
    EntranceRule(fr=R.MI411, to=R.MI409, name=f"{R.MI411} - Bottom Right Door"),
    EntranceRule(fr=R.MI412, to=R.MI415, name=f"{R.MI412} - Left Door"),
    EntranceRule(fr=R.MI412, to=R.MI413, name=f"{R.MI412} - Men's Bathroom Door"),
    EntranceRule(fr=R.MI412, to=R.MI414, name=f"{R.MI412} - Women's Bathroom Door"),
    EntranceRule(fr=R.MI413, to=R.MI412, name=f"{R.MI413} - Door"),
    EntranceRule(fr=R.MI414, to=R.MI412, name=f"{R.MI414} - Door"),
    # TODO: Add more ways to defeat mimi
    LocationRule(L.C24_YELLOW_PURE_HEART, Has(I.PIXL_THOREAU)),
    LocationRule(L.FLEEP_MAP_REVEAL_17, CanFleepTreasureSpot(I.MAP_17)),
    EntranceRule(fr=R.MI415, to=R.MI411, name=f"{R.MI415} - Bottom Door"),
    EntranceRule(fr=R.MI415, to=R.MI412, name=f"{R.MI415} - Top Door"),
    # endregion
    # region Chapter 3-1
    # doa1_l
    # EntranceRule(fr=R.TA101
    # , to=R.TA102
    # , name=f"{R.TA101} - Door in the sky"
    # ),
    # Entrance has an empty name
    # EntranceRule(fr=R.TA101
    # , to=R.TA103
    # , name=f"{R.TA101} - Fall between Red Pipes"
    # , etype=EntranceType.ONE_WAY
    # ),
    # dokan_m
    # EntranceRule(fr=R.TA101
    # , to=R.MAC02_L_TOWER
    # , name=f"{R.TA101} - Left Red Pipe"
    # , etype=EntranceType.ONE_WAY
    # ),
    # dokan_m2
    # EntranceRule(fr=R.TA101
    # , to=R.MAC02_L_TOWER
    # , name=f"{R.TA101} - Right Red Pipe"
    # , etype=EntranceType.ONE_WAY
    # ),
    # hai_dokan_03
    # EntranceRule(fr=R.TA101
    # , to=R.MAC02_L_TOWER
    # , name=f"{R.TA101} - Right Background Pipe"
    # , etype=EntranceType.ONE_WAY
    # ),
    # endregion
]

ENTRANCE_RULES = [rule for rule in ALL_RULES if isinstance(rule, EntranceRule)]
LOCATION_RULES = [rule for rule in ALL_RULES if isinstance(rule, LocationRule)]
