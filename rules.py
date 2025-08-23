""" All things that define logical access between regions and locations """
import typing
from enum import IntEnum

from entrance_rando import Entrance, EntranceType
from worlds.generic.Rules import add_rule, CollectionRule

from .constants import (SuperPaperMarioItem, SuperPaperMarioLocation, SPMEntrance, SPMEvent, SPMItem, SPMLocation,
                        SPMRegion)
from .items import CHARACTERS, PIXLS
from .options import ChapterKeysLock, FlipsidePitAccess, FlopsidePitAccess, PitLogic, SuperPaperMarioOptions

if typing.TYPE_CHECKING:
    from . import SuperPaperMarioWorld


class SPMRuleBuilder:
    """Utility class to more easily build `CollectionRule`s"""
    player: int
    world: "SuperPaperMarioWorld"
    options: SuperPaperMarioOptions

    entrance_rando: list[Entrance]
    """
    The list of entrances that need randomization.
    To be used with Generic ER and SPMRuleBuilder.randomize_entrances
    """

    def __init__(self, world: "SuperPaperMarioWorld"):
        self.world = world
        self.player = world.player
        self.options = world.options
        self.entrance_rando = []

    @staticmethod
    def always():
        """Constant rule to always allow access"""
        return lambda state: True

    @staticmethod
    def never():
        """Constant rule to never allow access"""
        return lambda state: False

    def location(self, location_name: str, rule: CollectionRule = always()):
        """Sets a rule on the location_name"""
        add_rule(self.world.get_location(location_name), rule)

    def event(self, region_name: str, location_name: str, item_name: str | None = None,
              rule: CollectionRule = always(), show_in_spoiler: bool = False):
        """Adds an event location to the world and sets the rule on it's access"""
        region = self.world.get_region(region_name)
        region.add_event(location_name, item_name, rule, SuperPaperMarioLocation, SuperPaperMarioItem, show_in_spoiler)

    def connect(self, name: str, src: str, dest: str, rule: CollectionRule = always(),
                randomization_group: int = 0, randomization_type: EntranceType = EntranceType.TWO_WAY):
        """Connects a region to another given an access rule.
        Keeps tracks of whether the entrance created from this should later be randomized with `randomize_entrances`.

        name -- The entrance name for display in text clients. Use SPMEntrance.
        src -- The region.name to connect from. Use SPMRegion.
        dest -- The region.name to connect to. Use SPMRegion.
        rule -- What restricts going from `src` to `dest`.
        randomization_group -- How can this entrance pair with others? Use EGroup with bitwise or (|) to combine these.
        randomization_type -- Is the entrance one-way or two-way? Only applies if randomization_group is specified.
        """
        src_region = self.world.get_region(src)
        dest_region = self.world.get_region(dest)
        entrance = src_region.connect(dest_region, name, rule)
        if randomization_group > 0:
            entrance.randomization_group = randomization_group
            entrance.randomization_type = randomization_type
            self.entrance_rando.append(entrance)

    # def randomize_entrances(self):
    #     for entrance in self.entrance_rando:
    #         disconnect_entrance_for_randomization(entrance)
    #     randomize_entrances(self.world, True, bake_target_group_lookup(self.world, get_target_groups), True)

    def if_any(self, *rules: CollectionRule) -> CollectionRule:
        """Rule combinator, returns True if all rules given are True"""
        return lambda state: any(rule(state) for rule in rules)

    def if_all(self, *rules: CollectionRule) -> CollectionRule:
        """Rule combinator, returns True if any rule given is True"""
        return lambda state: all(rule(state) for rule in rules)

    def if_opt(self, opt: bool, rule_true: CollectionRule = always(),
               rule_false: CollectionRule = never()) -> CollectionRule:
        """Rule combinator, returns `rule_true` if `opt` is True, else returns `rule_false"""
        return rule_true if opt else rule_false

    def has(self, item: str, count: int = 1) -> CollectionRule:
        """CollectionState helper, returns True if the player has at least `count` of `item`"""
        return lambda state: state.has(item, self.player, count)

    def has_all(self, *items: str) -> CollectionRule:
        """CollectionState helper, returns True if the player has all `items`"""
        return lambda state: state.has_all(items, self.player)

    def has_any(self, *items: str) -> CollectionRule:
        """CollectionState helper, returns True if the player has any `items`"""
        return lambda state: state.has_any(items, self.player)

    def has_all_counts(self, item_counts: dict[str, int]) -> CollectionRule:
        """
        CollectionState helper, returns True if the player has at least the `value` of the `key` of all `item_counts`
        """
        return lambda state: state.has_all_counts(item_counts, self.player)

    def has_any_count(self, item_counts: dict[str, int]) -> CollectionRule:
        """
        CollectionState helper, returns True if the player has at least the `value` of the `key` of any `item_counts`
        """
        return lambda state: state.has_any_count(item_counts, self.player)

    def has_from_list(self, items: list[str], count: int) -> CollectionRule:
        """CollectionState helper, returns True if the player has at least `count` of any `items`"""
        return lambda state: state.has_from_list(items, self.player, count)

    def has_from_list_unique(self, items: list[str], count: int) -> CollectionRule:
        """CollectionState helper, returns True if the player has at least `count` of `item`"""
        return lambda state: state.has_from_list_unique(items, self.player, count)

    def has_group(self, item_name_group: str, count: int = 1) -> CollectionRule:
        """CollectionState helper, returns True if the player has at least `count` of `item`"""
        return lambda state: state.has_group(item_name_group, self.player, count)

    def has_group_unique(self, item_name_group: str, count: int = 1) -> CollectionRule:
        """CollectionState helper, returns True if the player has at least `count` of `item`"""
        return lambda state: state.has_group_unique(item_name_group, self.player, count)

    def chapter_key(self, chapter_key: str, subchapter_key: str) -> CollectionRule:
        opts = {
            ChapterKeysLock.option_open: self.always(),
            ChapterKeysLock.option_chapter_locked: self.has(chapter_key),
            ChapterKeysLock.option_subchapters_locked: self.has(subchapter_key),
        }
        return opts.get(self.options.chapter_keys_lock.value, self.never())

    def can_flip(self) -> CollectionRule:
        return self.has_all(SPMItem.CHARACTER_MARIO, SPMItem.ABILITY_FLIP)

    def can_float(self) -> CollectionRule:
        return self.has_all(SPMItem.CHARACTER_PEACH)  # SPMItem.ABILITY_UMBRELLA

    def can_fire(self) -> CollectionRule:
        return self.has_all(SPMItem.CHARACTER_BOWSER)  # SPMItem.ABILITY_FIRE

    def can_super_jump(self) -> CollectionRule:
        return self.has_all(SPMItem.CHARACTER_LUIGI)  # SPMItem.ABILITY_SUPER_JUMP

    def can_break_hard_blocks(self) -> CollectionRule:
        return self.if_any(self.has_any(SPMItem.PIXL_BOOMER, SPMItem.PIXL_CUDGE, SPMItem.PIXL_THUDLEY),
                           self.can_fire())


def set_rules(r: SPMRuleBuilder) -> None:
    """Assign all of the location/event collection rules as well as the completion condition"""
    flipside_rules(r)
    flopside_rules(r)
    chapter1_rules(r)
    chapter2_rules(r)
    chapter3_rules(r)
    chapter4_rules(r)
    chapter5_rules(r)
    chapter6_rules(r)
    chapter7_rules(r)
    chapter8_rules(r)

    r.world.multiworld.completion_condition[r.world.player] = r.has(SPMEvent.VICTORY)


class EGroup(IntEnum):
    """An Entrance Group for entrance_rando"""
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


def flipside_rules(r: SPMRuleBuilder):
    # Flipside Tower
    r.connect(SPMEntrance.MAC02_L_FALL, SPMRegion.MAC02_L_TOWER, SPMRegion.MAC01_LAYER1)
    # EGroup.FALL | EGroup.DOWN | EGroup.HUB, EntranceType.ONE_WAY),
    r.connect(SPMEntrance.MAC02_L_TOWER_ELV1, SPMRegion.MAC02_L_TOWER, SPMRegion.MAC02_LAYER1)
    r.connect(SPMEntrance.MAC02_DOA6_I_1, SPMRegion.MAC02_L_TOWER, SPMRegion.HE101,
              r.chapter_key(SPMItem.CHAPTER_1_KEY, SPMItem.CHAPTER_1_1_KEY))
    r.connect(SPMEntrance.MAC02_DOA6_I_2, SPMRegion.MAC02_L_TOWER, SPMRegion.HE201,
              r.chapter_key(SPMItem.CHAPTER_1_KEY, SPMItem.CHAPTER_1_2_KEY))
    r.connect(SPMEntrance.MAC02_DOA6_I_3, SPMRegion.MAC02_L_TOWER, SPMRegion.HE301,
              r.chapter_key(SPMItem.CHAPTER_1_KEY, SPMItem.CHAPTER_1_3_KEY))
    r.connect(SPMEntrance.MAC02_DOA6_I_4, SPMRegion.MAC02_L_TOWER, SPMRegion.HE401,
              r.chapter_key(SPMItem.CHAPTER_1_KEY, SPMItem.CHAPTER_1_4_KEY))
    r.connect(SPMEntrance.MAC02_DOA8_I_1, SPMRegion.MAC02_L_TOWER, SPMRegion.MI101,
              r.chapter_key(SPMItem.CHAPTER_2_KEY, SPMItem.CHAPTER_2_1_KEY))
    r.connect(SPMEntrance.MAC02_DOA8_I_2, SPMRegion.MAC02_L_TOWER, SPMRegion.MI201,
              r.chapter_key(SPMItem.CHAPTER_2_KEY, SPMItem.CHAPTER_2_2_KEY))
    r.connect(SPMEntrance.MAC02_DOA8_I_3, SPMRegion.MAC02_L_TOWER, SPMRegion.MI301,
              r.chapter_key(SPMItem.CHAPTER_2_KEY, SPMItem.CHAPTER_2_3_KEY))
    r.connect(SPMEntrance.MAC02_DOA8_I_4, SPMRegion.MAC02_L_TOWER, SPMRegion.MI401,
              r.chapter_key(SPMItem.CHAPTER_2_KEY, SPMItem.CHAPTER_2_4_KEY))
    r.connect(SPMEntrance.MAC02_DOA9_I_1, SPMRegion.MAC02_L_TOWER, SPMRegion.TA101,
              r.chapter_key(SPMItem.CHAPTER_3_KEY, SPMItem.CHAPTER_3_1_KEY))
    r.connect(SPMEntrance.MAC02_DOA9_I_2, SPMRegion.MAC02_L_TOWER, SPMRegion.TA201,
              r.chapter_key(SPMItem.CHAPTER_3_KEY, SPMItem.CHAPTER_3_2_KEY))
    r.connect(SPMEntrance.MAC02_DOA9_I_3, SPMRegion.MAC02_L_TOWER, SPMRegion.TA301,
              r.chapter_key(SPMItem.CHAPTER_3_KEY, SPMItem.CHAPTER_3_3_KEY))
    r.connect(SPMEntrance.MAC02_DOA9_I_4, SPMRegion.MAC02_L_TOWER, SPMRegion.TA401,
              r.chapter_key(SPMItem.CHAPTER_3_KEY, SPMItem.CHAPTER_3_4_KEY))
    r.connect(SPMEntrance.MAC02_DOA10_I_1, SPMRegion.MAC02_L_TOWER, SPMRegion.SP101,
              r.chapter_key(SPMItem.CHAPTER_4_KEY, SPMItem.CHAPTER_4_1_KEY))
    r.connect(SPMEntrance.MAC02_DOA10_I_2, SPMRegion.MAC02_L_TOWER, SPMRegion.SP201,
              r.chapter_key(SPMItem.CHAPTER_4_KEY, SPMItem.CHAPTER_4_2_KEY))
    r.connect(SPMEntrance.MAC02_DOA10_I_3, SPMRegion.MAC02_L_TOWER, SPMRegion.SP301,
              r.chapter_key(SPMItem.CHAPTER_4_KEY, SPMItem.CHAPTER_4_3_KEY))
    r.connect(SPMEntrance.MAC02_DOA10_I_4, SPMRegion.MAC02_L_TOWER, SPMRegion.SP401,
              r.chapter_key(SPMItem.CHAPTER_4_KEY, SPMItem.CHAPTER_4_4_KEY))
    r.connect(SPMEntrance.MAC02_DOA11_I_1, SPMRegion.MAC02_L_TOWER, SPMRegion.GN101,
              r.chapter_key(SPMItem.CHAPTER_5_KEY, SPMItem.CHAPTER_5_1_KEY))
    r.connect(SPMEntrance.MAC02_DOA11_I_2, SPMRegion.MAC02_L_TOWER, SPMRegion.GN201,
              r.chapter_key(SPMItem.CHAPTER_5_KEY, SPMItem.CHAPTER_5_2_KEY))
    r.connect(SPMEntrance.MAC02_DOA11_I_3, SPMRegion.MAC02_L_TOWER, SPMRegion.GN301,
              r.chapter_key(SPMItem.CHAPTER_5_KEY, SPMItem.CHAPTER_5_3_KEY))
    r.connect(SPMEntrance.MAC02_DOA11_I_4, SPMRegion.MAC02_L_TOWER, SPMRegion.GN401,
              r.chapter_key(SPMItem.CHAPTER_5_KEY, SPMItem.CHAPTER_5_4_KEY))
    r.connect(SPMEntrance.MAC02_DOA12_I_1, SPMRegion.MAC02_L_TOWER, SPMRegion.WA101,
              r.chapter_key(SPMItem.CHAPTER_6_KEY, SPMItem.CHAPTER_6_1_KEY))
    r.connect(SPMEntrance.MAC02_DOA12_I_2, SPMRegion.MAC02_L_TOWER, SPMRegion.WA201,
              r.chapter_key(SPMItem.CHAPTER_6_KEY, SPMItem.CHAPTER_6_2_KEY))
    r.connect(SPMEntrance.MAC02_DOA12_I_3, SPMRegion.MAC02_L_TOWER, SPMRegion.WA301,
              r.chapter_key(SPMItem.CHAPTER_6_KEY, SPMItem.CHAPTER_6_3_KEY))
    r.connect(SPMEntrance.MAC02_DOA12_I_4, SPMRegion.MAC02_L_TOWER, SPMRegion.WA401,
              r.chapter_key(SPMItem.CHAPTER_6_KEY, SPMItem.CHAPTER_6_4_KEY))
    r.connect(SPMEntrance.MAC02_DOA13_I_1, SPMRegion.MAC02_L_TOWER, SPMRegion.AN101,
              r.chapter_key(SPMItem.CHAPTER_7_KEY, SPMItem.CHAPTER_7_1_KEY))
    r.connect(SPMEntrance.MAC02_DOA13_I_2, SPMRegion.MAC02_L_TOWER, SPMRegion.AN201,
              r.chapter_key(SPMItem.CHAPTER_7_KEY, SPMItem.CHAPTER_7_2_KEY))
    r.connect(SPMEntrance.MAC02_DOA13_I_3, SPMRegion.MAC02_L_TOWER, SPMRegion.AN301,
              r.chapter_key(SPMItem.CHAPTER_7_KEY, SPMItem.CHAPTER_7_3_KEY))
    r.connect(SPMEntrance.MAC02_DOA13_I_4, SPMRegion.MAC02_L_TOWER, SPMRegion.AN401,
              r.chapter_key(SPMItem.CHAPTER_7_KEY, SPMItem.CHAPTER_7_4_KEY))

    # Flipside 3F
    r.connect(SPMEntrance.MAC01_ELV1, SPMRegion.MAC01_LAYER1, SPMRegion.MAC02_LAYER1,
              randomization_group=EGroup.ELEVATOR_DOWN | EGroup.HUB)
    r.location(SPMLocation.FLIPSIDE_HEART_PILLAR_RED,
               r.has(SPMItem.RED_PURE_HEART))
    # r.location(SPMLocation.FLIPSIDE_3F_EAT_A_SPICY_SOUP)  # will this require spicy soup in the itempool?
    # r.location(SPMLocation.FLIPSIDE_3F_FISHBOWL)

    r.connect(SPMEntrance.MAC01_DOKAN_1, SPMRegion.MAC01_LAYER2, SPMRegion.MAC02_LAYER2,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.location(SPMLocation.FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS,
               r.has(SPMItem.PIXL_TIPPI))
    r.location(SPMLocation.FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK,
               r.has(SPMItem.PIXL_PICCOLO))

    # Flipside 2F
    r.connect(SPMEntrance.MAC02_L_TOWER_ELV2, SPMRegion.MAC02_LAYER1, SPMRegion.MAC02_L_TOWER)
    r.connect(SPMEntrance.MAC02_ELV1, SPMRegion.MAC02_LAYER1, SPMRegion.MAC09_LAYER3,
              r.always(),  # This elevator doesn't work until GSW(0, 53), after chapter 1-4 cleared, before intermission
              randomization_group=EGroup.ELEVATOR_DOWN | EGroup.HUB)
    r.connect(SPMEntrance.MAC02_ELV2, SPMRegion.MAC02_LAYER1, SPMRegion.MAC01_LAYER1,
              randomization_group=EGroup.ELEVATOR_UP | EGroup.HUB)
    r.connect(SPMEntrance.MAC02_AODOKAN_1, SPMRegion.MAC02_LAYER1, SPMRegion.MAC05_LAYER1,
              r.can_flip())
    r.connect(SPMEntrance.MAC02_AODOKAN_2, SPMRegion.MAC02_LAYER1, SPMRegion.MAC12_LAYER1)
    r.connect(SPMEntrance.MAC02_L_3D_1_2, SPMRegion.MAC02_LAYER1, SPMRegion.MAC02_LAYER2,
              r.if_all(r.can_flip(), r.has(SPMItem.OLD_KEY)))
    r.location(SPMLocation.PICCOLO_FETCH_MERLUVLEE,
               r.has(SPMItem.TRAINING_MACHINE))

    r.connect(SPMEntrance.MAC02_DOKAN_1, SPMRegion.MAC02_LAYER2, SPMRegion.MAC01_LAYER2,
              r.can_break_hard_blocks(),
              EGroup.PIPE | EGroup.HUB)
    # MAC02_L_3D_2_1: you can't go from layer 2 to layer 1 if you haven't opened the door with the Old Key
    r.connect(SPMEntrance.MAC02_L_3D_2_3, SPMRegion.MAC02_LAYER2, SPMRegion.MAC02_LAYER3,
              r.can_flip())

    r.connect(SPMEntrance.MAC02_DOKAN_2, SPMRegion.MAC02_LAYER3, SPMRegion.MAC06_LAYER1,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.connect(SPMEntrance.MAC02_L_3D_3_2, SPMRegion.MAC02_LAYER3, SPMRegion.MAC02_LAYER2,
              r.can_flip())
    r.location(SPMLocation.FLIPSIDE_HEART_PILLAR_GREEN,
               r.has_all(SPMItem.PIXL_THUDLEY, SPMItem.GREEN_PURE_HEART))

    # Flipside/Flopside Mirror Hall
    r.connect(SPMEntrance.MAC03_DOA6_R, SPMRegion.MAC03_LAYER1, SPMRegion.MAC09_LAYER1,
              randomization_group=EGroup.DOOR | EGroup.HUB)
    r.connect(SPMEntrance.MAC03_L_3D_1_2, SPMRegion.MAC03_LAYER1, SPMRegion.MAC03_LAYER2,
              r.can_flip())

    # Flipside B1
    r.connect(SPMEntrance.MAC04_ELV1, SPMRegion.MAC04_LAYER1, SPMRegion.MAC09_LAYER3,
              randomization_group=EGroup.ELEVATOR_UP | EGroup.HUB)
    r.connect(SPMEntrance.MAC04_ELV2, SPMRegion.MAC04_LAYER1, SPMRegion.MAC05_LAYER1,
              randomization_group=EGroup.ELEVATOR_DOWN | EGroup.HUB)
    r.connect(SPMEntrance.MAC04_L_SHRINK, SPMRegion.MAC04_LAYER1, SPMRegion.MAC04_ITTY_BITS,
              r.has(SPMItem.PIXL_DOTTIE))
    r.location(SPMLocation.FLIPSIDE_B1_3D_CHEST,
               r.can_flip())
    # SPMRegion.MAC04_ITTY_BITS,  # Technically this connects back thru MAC04_L_SHRINK but dead-end two-way entrances
    # don't have to be reconnected... I think
    # SPMRegion.MAC04_ARCADE_PIPE,

    # Flipside B2
    r.connect(SPMEntrance.MAC05_ELV1, SPMRegion.MAC05_LAYER1, SPMRegion.MAC04_LAYER1)
    r.connect(SPMEntrance.MAC05_AODOKAN_1, SPMRegion.MAC05_LAYER1, SPMRegion.MAC02_LAYER1,
              r.can_flip())
    r.connect(SPMEntrance.MAC05_DOKAN_1, SPMRegion.MAC05_LAYER1, SPMRegion.L_FLIPSIDE_PIT,
              r.if_all(
                  # Is pit accessible at all?
                  r.if_opt(r.options.flipside_pit_access != FlipsidePitAccess.option_closed,
                           r.has(SPMEvent.SWITCH_FLIPSIDE_PIT_CAGE)),
                  # Have the settings deferred pit in-logic until they have enough chapters?
                  r.if_opt(r.options.flipside_pit_logic.requires_chapters,
                           r.always(),  # TODO chapter 1-7 access logic
                           r.always()),
                  # Have the settings deferred pit in-logic until they have all characters and pixls?
                  r.if_opt(r.options.flipside_pit_logic.requires_characters,
                           r.has_all(*CHARACTERS, *PIXLS),
                           r.always())))
    r.connect(SPMEntrance.MAC05_L_CAGE_JUMP, SPMRegion.MAC05_LAYER1, SPMRegion.L_FLIPSIDE_PIT_ENTRANCE,
              r.if_any(r.can_super_jump(), r.has(SPMEvent.SWITCH_FLIPSIDE_PIT_CAGE)))
    r.connect(SPMEntrance.MAC05_L_3D_1_2, SPMRegion.L_FLIPSIDE_PIT_ENTRANCE, SPMRegion.MAC05_LAYER2,
              r.can_flip())
    r.event(SPMRegion.L_FLIPSIDE_PIT_ENTRANCE, SPMEvent.SWITCH_FLIPSIDE_PIT_CAGE)

    r.connect(SPMEntrance.MAC05_L_3D_2_1, SPMRegion.MAC05_LAYER2, SPMRegion.L_FLIPSIDE_PIT_ENTRANCE,
              r.has_all(SPMItem.CHARACTER_MARIO, SPMItem.PIXL_TIPPI))
    r.connect(SPMEntrance.MAC05_DOKAN_2, SPMRegion.MAC05_LAYER2, SPMRegion.MAC07_LAYER2,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.location(SPMLocation.FLIPSIDE_B2_CHEST_AFTER_PIPE,
               r.has(SPMEvent.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK))

    # Flipside 1F Outskirts
    r.connect(SPMEntrance.MAC06_DOKAN_1, SPMRegion.MAC06_LAYER1, SPMRegion.MAC02_LAYER3,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.connect(SPMEntrance.MAC06_DOKAN_2, SPMRegion.MAC06_LAYER1, SPMRegion.MAC07_LAYER2,
              r.can_break_hard_blocks(),  # Bowser *barely* has enough room to stand to break the blocks
              EGroup.PIPE | EGroup.HUB)
    r.connect(SPMEntrance.MAC06_JUMP, SPMRegion.MAC06_LAYER1, SPMRegion.MAC08)
    r.connect(SPMEntrance.MAC06_L_3D_1_2, SPMRegion.MAC06_LAYER1, SPMRegion.MAC06_LAYER2,
              r.can_flip())

    r.connect(SPMEntrance.MAC06_L_3D_2_1, SPMRegion.MAC06_LAYER2, SPMRegion.MAC06_LAYER1,
              r.can_flip())
    r.location(SPMLocation.FLIPSIDE_HEART_PILLAR_ORANGE,
               r.if_all(
                   # Thoreau place a squig below the pillar to jump off of
                   r.if_any(r.can_float(), r.has(SPMItem.PIXL_THOREAU)),
                   r.has(SPMItem.ORANGE_PURE_HEART)))

    # Flipside B1 Outskirts
    # SPMLocation.FLIPSIDE_B1_OUTSKIRTS_CHEST_BEHIND_PILLAR

    r.connect(SPMEntrance.MAC07_DOKAN_1, SPMRegion.MAC07_LAYER2, SPMRegion.MAC05_LAYER2,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.connect(SPMEntrance.MAC07_DOKAN_2, SPMRegion.MAC07_LAYER2, SPMRegion.MAC06_LAYER1,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.connect(SPMEntrance.MAC07_L_3D_2_1, SPMRegion.MAC07_LAYER2, SPMRegion.MAC07_LAYER1,
              r.if_all(r.can_flip(), r.has(SPMEvent.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK)))
    r.location(SPMLocation.FLIPSIDE_HEART_PILLAR_YELLOW,
               r.if_all(r.can_flip(), r.has_all(SPMItem.YELLOW_PURE_HEART, SPMItem.PIXL_SLIM)))

    # Flipside 1F Outskirts - Chasm
    r.connect(SPMEntrance.MAC08_DEFAULT, SPMRegion.MAC08, SPMRegion.MAC06_LAYER1)
    # SPMLocation.FLIPSIDE_1F_OUTSKIRTS_LEFT_CHEST_IN_HOLE
    # SPMLocation.FLIPSIDE_1F_OUTSKIRTS_RIGHT_CHEST_IN_HOLE

    # Flipside 1F
    r.connect(SPMEntrance.MAC09_DOA6_I, SPMRegion.MAC09_LAYER1, SPMRegion.MAC03_LAYER1)
    r.connect(SPMEntrance.MAC09_L_3D_1_2, SPMRegion.MAC09_LAYER1, SPMRegion.MAC09_LAYER2,
              r.can_flip())  # Standing outside Mirror Hall, you don't need Fleep. You just walk thru the wall

    r.connect(SPMEntrance.MAC09_L_3D_2_1, SPMRegion.MAC09_LAYER2, SPMRegion.MAC09_LAYER1,
              r.if_all(r.has(SPMItem.PIXL_FLEEP), r.can_flip()))
    r.connect(SPMEntrance.MAC09_L_3D_2_3, SPMRegion.MAC09_LAYER2, SPMRegion.MAC09_LAYER3,
              r.if_all(r.has(SPMItem.PIXL_BOOMER), r.can_flip()))

    r.connect(SPMEntrance.MAC09_ELV1, SPMRegion.MAC09_LAYER3, SPMRegion.MAC02_LAYER1,
              randomization_group=EGroup.ELEVATOR_UP | EGroup.HUB)
    r.connect(SPMEntrance.MAC09_ELV2, SPMRegion.MAC09_LAYER3, SPMRegion.MAC04_LAYER1,
              r.always(),  # This elevator only works starting at GSW(0, 73), getting boomer
              randomization_group=EGroup.ELEVATOR_DOWN | EGroup.HUB)
    r.connect(SPMEntrance.MAC09_L_3D_3_2, SPMRegion.MAC09_LAYER3, SPMRegion.MAC09_LAYER2,
              r.if_all(r.has(SPMItem.PIXL_BOOMER), r.can_flip()))

    # Flipside Pit of 100 Trials
    if r.options.flipside_pit_access != FlipsidePitAccess.option_closed:
        r.event(SPMRegion.L_FLIPSIDE_PIT, SPMLocation.FLIPSIDE_PIT_WRACKTAIL, SPMEvent.COMPLETED_FLIPSIDE_PIT,
                show_in_spoiler=True)


def flopside_rules(r: SPMRuleBuilder):
    # Flopside Tower
    r.connect(SPMEntrance.MAC12_L_FALL, SPMRegion.MAC12_L_TOWER, SPMRegion.MAC11_LAYER1,
              randomization_type=EntranceType.ONE_WAY)
    r.connect(SPMEntrance.MAC12_L_TOWER_ELV1, SPMRegion.MAC12_L_TOWER, SPMRegion.MAC12_LAYER1)

    r.connect(SPMEntrance.MAC12_DOA6_I_1, SPMRegion.MAC12_L_TOWER, SPMRegion.LS101,
              r.chapter_key(SPMItem.CHAPTER_8_KEY, SPMItem.CHAPTER_8_1_KEY))
    r.connect(SPMEntrance.MAC12_DOA6_I_2, SPMRegion.MAC12_L_TOWER, SPMRegion.LS201,
              r.chapter_key(SPMItem.CHAPTER_8_KEY, SPMItem.CHAPTER_8_2_KEY))
    r.connect(SPMEntrance.MAC12_DOA6_I_3, SPMRegion.MAC12_L_TOWER, SPMRegion.LS301,
              r.chapter_key(SPMItem.CHAPTER_8_KEY, SPMItem.CHAPTER_8_3_KEY))
    r.connect(SPMEntrance.MAC12_DOA6_I_4, SPMRegion.MAC12_L_TOWER, SPMRegion.LS401,
              r.chapter_key(SPMItem.CHAPTER_8_KEY, SPMItem.CHAPTER_8_4_KEY))

    # Flopside 3F
    r.connect(SPMEntrance.MAC11_ELV1, SPMRegion.MAC11_LAYER1, SPMRegion.MAC12_LAYER1)
    r.location(SPMLocation.FLOPSIDE_HEART_PILLAR_CYAN, r.has(SPMItem.CYAN_PURE_HEART))

    r.connect(SPMEntrance.MAC11_DOKAN_1, SPMRegion.MAC11_LAYER2, SPMRegion.MAC12_LAYER2)
    r.location(SPMLocation.FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK, r.has(SPMItem.PIXL_PICCOLO))
    r.location(SPMLocation.FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS, r.has(SPMItem.PIXL_TIPPI))

    # Flopside 2F
    r.connect(SPMEntrance.MAC12_L_TOWER_ELV2, SPMRegion.MAC12_LAYER1, SPMRegion.MAC12_L_TOWER)
    r.connect(SPMEntrance.MAC12_ELV1, SPMRegion.MAC12_LAYER1, SPMRegion.MAC11_LAYER1,
              randomization_group=EGroup.ELEVATOR_UP | EGroup.HUB)
    r.connect(SPMEntrance.MAC12_ELV2, SPMRegion.MAC12_LAYER1, SPMRegion.MAC19_LAYER3,
              randomization_group=EGroup.ELEVATOR_DOWN | EGroup.HUB)
    r.connect(SPMEntrance.MAC12_AODOKAN_1, SPMRegion.MAC12_LAYER1, SPMRegion.MAC15_LAYER1,
              r.can_flip())
    r.connect(SPMEntrance.MAC12_AODOKAN_2, SPMRegion.MAC12_LAYER1, SPMRegion.MAC02_LAYER1)
    r.connect(SPMEntrance.MAC12_L_3D_1_2, SPMRegion.MAC12_LAYER1, SPMRegion.MAC12_LAYER2,
              r.can_flip())
    r.location(SPMLocation.PICCOLO_FETCH_MERLEE, r.has(SPMItem.CRYSTAL_BALL))

    r.connect(SPMEntrance.MAC12_DOKAN_1, SPMRegion.MAC12_LAYER2, SPMRegion.MAC11_LAYER2,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.connect(SPMEntrance.MAC12_L_3D_2_1, SPMRegion.MAC12_LAYER2, SPMRegion.MAC12_LAYER1,
              r.can_flip())
    r.connect(SPMEntrance.MAC12_L_3D_2_3, SPMRegion.MAC12_LAYER2, SPMRegion.MAC12_LAYER3,
              r.can_flip())

    r.connect(SPMEntrance.MAC12_DOKAN_2, SPMRegion.MAC12_LAYER3, SPMRegion.MAC16_LAYER1,
              randomization_group=EGroup.PIPE | EGroup.HUB)
    r.connect(SPMEntrance.MAC12_L_3D_3_2, SPMRegion.MAC12_LAYER3, SPMRegion.MAC12_LAYER2,
              r.can_flip())
    r.location(SPMLocation.FLOPSIDE_HEART_PILLAR_WHITE, r.has(SPMItem.WHITE_PURE_HEART))

    # Flopside B1
    r.connect(SPMEntrance.MAC14_ELV1, SPMRegion.MAC14_RIGHT, SPMRegion.MAC15_LAYER1)
    r.connect(SPMEntrance.MAC14_ELV2, SPMRegion.MAC14_RIGHT, SPMRegion.MAC19_LAYER3)
    r.connect(SPMEntrance.MAC14_L_FLIP_L, SPMRegion.MAC14_RIGHT, SPMRegion.MAC14_LEFT,
              r.can_flip())
    r.connect(SPMEntrance.MAC14_L_FLIP_B, SPMRegion.MAC14_RIGHT, SPMRegion.MAC14_L_BACK_BEVERAGARIUM,
              r.can_flip())

    r.connect(SPMEntrance.MAC14_L_SHRINK, SPMRegion.MAC14_LEFT, SPMRegion.MAC14_L_ITTY_BITS)
    r.connect(SPMEntrance.MAC14_L_FLIP_R, SPMRegion.MAC14_LEFT, SPMRegion.MAC14_RIGHT,
              r.can_flip())

    # Flopside B2
    r.connect(SPMEntrance.MAC15_DOKAN_1, SPMRegion.MAC15_LAYER1, SPMRegion.L_FLOPSIDE_PIT,
              r.if_all(
                  r.if_opt(r.options.flopside_pit_access == FlopsidePitAccess.option_open,
                           r.always(),
                           r.if_opt(r.options.flopside_pit_access == FlopsidePitAccess.option_normal,
                                    r.has_all(SPMEvent.COMPLETED_FLIPSIDE_PIT, SPMItem.PIXL_FLEEP),
                                    r.never())),  # option_closed
                  r.if_opt(r.options.flopside_pit_logic.requires_chapters,
                           r.always(),  # TODO region access logic
                           r.always()),
                  r.if_opt(r.options.flopside_pit_logic.requires_characters,
                           r.has_all(*CHARACTERS, *PIXLS),
                           r.always())))

    r.connect(SPMEntrance.MAC15_AODOKAN_1, SPMRegion.MAC15_LAYER1, SPMRegion.MAC12_LAYER1)
    r.connect(SPMEntrance.MAC15_ELV1, SPMRegion.MAC15_LAYER1, SPMRegion.MAC14_RIGHT)

    r.connect(SPMEntrance.MAC15_JUMP, SPMRegion.MAC15_LAYER2, SPMRegion.MAC18)
    r.connect(SPMEntrance.MAC15_DOKAN_2, SPMRegion.MAC15_LAYER2, SPMRegion.MAC17_LAYER2)
    r.event(SPMRegion.MAC15_LAYER2, SPMEvent.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK, None,
            r.if_all(r.has(SPMItem.PIXL_CUDGE), r.can_flip()))
    r.location(SPMLocation.FLOPSIDE_B2_CHEST_AFTER_PIPE,
               r.has(SPMEvent.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK))

    # Flopside 1st Floor Outskirts
    r.connect(SPMEntrance.MAC16_DOKAN_1, SPMRegion.MAC16_LAYER1, SPMRegion.MAC12_LAYER3)
    r.connect(SPMEntrance.MAC16_DOKAN_2, SPMRegion.MAC16_LAYER1, SPMRegion.MAC17_LAYER1)
    r.connect(SPMEntrance.MAC16_L_3D_1_2, SPMRegion.MAC16_LAYER1, SPMRegion.MAC16_LAYER2)

    r.connect(SPMEntrance.MAC16_L_3D_2_1, SPMRegion.MAC16_LAYER2, SPMRegion.MAC16_LAYER1)
    r.location(SPMLocation.FLOPSIDE_HEART_PILLAR_BLUE, r.has(SPMItem.BLUE_PURE_HEART))

    # Flopside B1 Outskirts
    r.connect(SPMEntrance.MAC17_DOKAN1, SPMRegion.MAC17_LAYER1, SPMRegion.MAC15_LAYER2)
    r.connect(SPMEntrance.MAC17_DOKAN2, SPMRegion.MAC17_LAYER1, SPMRegion.MAC16_LAYER1)
    # SPMLocation.FLOPSIDE_B1_OUTSKIRT_CHEST_BEHIND_PILLAR

    r.connect(SPMEntrance.MAC17_L_3D_2_1, SPMRegion.MAC17_LAYER2, SPMRegion.MAC17_LAYER1,
              r.if_all(r.has(SPMItem.CHARACTER_LUIGI), r.can_flip()))
    r.location(SPMLocation.FLOPSIDE_HEART_PILLAR_PURPLE,
               r.has_all(SPMItem.PURPLE_PURE_HEART, SPMItem.CHARACTER_LUIGI))  # Luigi can make the jump w/o super jump
    r.event(SPMRegion.MAC17_LAYER2, SPMEvent.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK, None,
            r.has(SPMItem.PIXL_CUDGE))

    r.connect(SPMEntrance.MAC18_DEFAULT, SPMRegion.MAC18, SPMRegion.MAC15_LAYER1)

    # Flopside 1F
    r.connect(SPMEntrance.MAC19_DOA16_R, SPMRegion.MAC19_LAYER1, SPMRegion.MAC03_LAYER2)
    r.connect(SPMEntrance.MAC19_L_3D_1_2, SPMRegion.MAC19_LAYER1, SPMRegion.MAC19_LAYER2)

    r.connect(SPMEntrance.MAC19_L_3D_2_1, SPMRegion.MAC19_LAYER2, SPMRegion.MAC19_LAYER1,
              r.if_all(r.has(SPMItem.PIXL_FLEEP), r.can_flip()))
    r.connect(SPMEntrance.MAC19_L_3D_2_3, SPMRegion.MAC19_LAYER2, SPMRegion.MAC19_LAYER3,
              r.if_all(r.has(SPMItem.PIXL_BOOMER), r.can_flip()))

    r.connect(SPMEntrance.MAC19_ELV1, SPMRegion.MAC19_LAYER3, SPMRegion.MAC12_LAYER1,
              randomization_group=EGroup.ELEVATOR_UP | EGroup.HUB)
    r.connect(SPMEntrance.MAC19_ELV2, SPMRegion.MAC19_LAYER3, SPMRegion.MAC14_RIGHT,
              randomization_group=EGroup.ELEVATOR_DOWN | EGroup.HUB)
    r.connect(SPMEntrance.MAC19_L_3D_3_2, SPMRegion.MAC19_LAYER3, SPMRegion.MAC19_LAYER2)

    # Flopside Mirror Hall
    r.connect(SPMEntrance.MAC03_DOA16_R, SPMRegion.MAC03_LAYER2, SPMRegion.MAC19_LAYER1,
              randomization_group=EGroup.DOOR | EGroup.HUB)
    r.connect(SPMEntrance.MAC03_L_3D_2_1, SPMRegion.MAC03_LAYER2, SPMRegion.MAC03_LAYER1,
              r.can_flip())

    # Flopside Pit of 100 Trials
    if r.options.flopside_pit_access != FlopsidePitAccess.option_closed:
        r.event(SPMRegion.L_FLOPSIDE_PIT, SPMLocation.FLOPSIDE_PIT_SHADOO, SPMEvent.COMPLETED_FLOPSIDE_PIT,
                show_in_spoiler=True)


def chapter1_rules(r: SPMRuleBuilder):
    # Lineland Road (1-1)
    r.connect(SPMEntrance.HE101_IE_DOA_02, SPMRegion.HE101, SPMRegion.HE106,
              r.has(SPMItem.PIXL_TIPPI))
    r.connect(SPMEntrance.HE101_DOKAN_2, SPMRegion.HE101, SPMRegion.HE103)
    r.connect(SPMEntrance.HE101_DOA2_L, SPMRegion.HE101, SPMRegion.HE102,
              r.can_flip())
    r.location(SPMLocation.C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY, r.can_flip())

    r.connect(SPMEntrance.HE102_DOA1_L, SPMRegion.HE102, SPMRegion.HE101)
    r.connect(SPMEntrance.HE102_DOA2_L, SPMRegion.HE102, SPMRegion.HE104,
              r.if_any(r.can_flip(), r.can_float()))
    r.location(SPMLocation.C11_OPEN_ITEM_BEHIND_PIPE, r.can_flip())

    r.connect(SPMEntrance.HE103_DOKAN_2, SPMRegion.HE103, SPMRegion.HE101)

    r.connect(SPMEntrance.HE104_DOA1_L, SPMRegion.HE104, SPMRegion.HE102)
    r.connect(SPMEntrance.HE104_DOA2_L, SPMRegion.HE104, SPMRegion.HE105,
              r.if_any(r.can_flip(), r.can_super_jump()))

    r.connect(SPMEntrance.HE105_DOA1_L, SPMRegion.HE105, SPMRegion.HE104)
    r.location(SPMLocation.C11_CHEST_AFTER_STAR_BLOCK, r.can_flip())

    r.connect(SPMEntrance.HE106_IE_DOA, SPMRegion.HE106, SPMRegion.HE101)
    r.location(SPMLocation.C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM, r.can_flip())
    r.location(SPMLocation.C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM, r.can_flip())
    # r.location(SPMLocation.C11_TALK_TO_BESTOVIUS)  # Should talking to Bestovius require Mario?

    # Mount Lineland (1-2)
    r.connect(SPMEntrance.HE201_DOA1_I, SPMRegion.HE201, SPMRegion.HE202)
    r.connect(SPMEntrance.HE201_DOA2_I, SPMRegion.HE201, SPMRegion.HE202, r.can_flip())
    r.location(SPMLocation.C12_CHEST_IN_SHORTCUT, r.can_flip())

    r.connect(SPMEntrance.HE202_DOA1_I, SPMRegion.HE202, SPMRegion.HE201)
    r.connect(SPMEntrance.HE202_DOA3_I, SPMRegion.HE202, SPMRegion.HE203,
              r.if_any(
                  r.can_flip(),  # Mario flips from either left/middle door to right or...
                  r.if_all(  # You have to face tank 5-7 spiny tromps even with good timing by...
                      r.can_super_jump(),  # Luigi makes the jump from left door to middle
                      r.can_float(),  # Peach & Dashell float from middle hill to Spiny Tromp slope
                      r.has(SPMItem.PIXL_DASHELL))))

    r.connect(SPMEntrance.HE203_DOKAN_2, SPMRegion.HE203, SPMRegion.HE208,
              r.can_flip())  # Mario saves red to build the bridge, flips behind the bricks
    r.connect(SPMEntrance.HE203_DOKAN_3, SPMRegion.HE203, SPMRegion.HE206,
              r.can_flip())  # Flip behind the partitions
    r.connect(SPMEntrance.HE203_DOA1_I, SPMRegion.HE203, SPMRegion.HE202)
    r.connect(SPMEntrance.HE203_BG_IE1_IRIGUCHI, SPMRegion.HE203, SPMRegion.HE204)
    r.connect(SPMEntrance.HE203_BG_IE2_IRIGUCHI, SPMRegion.HE203, SPMRegion.HE205,
              r.if_any(
                  r.can_flip(),  # Mario saves red to build the bridge
                  r.has(SPMItem.PIXL_DASHELL),  # Dashell jump the left gap
                  r.can_float()))  # Float the left gap
    r.location(SPMLocation.C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE,
               r.if_any(
                   r.can_flip(),  # Mario saves red to build the bridge
                   r.has(SPMItem.PIXL_DASHELL),  # Dashell jump the left gap
                   r.can_float()))  # Float the left gap)
    r.location(SPMLocation.C12_STAR_BLOCK,
               r.if_any(
                   # Mario saves red to build left bridge, Watchitt wants to see Thoreau
                   r.if_all(r.can_flip(), r.has(SPMItem.PIXL_THOREAU)),
                   # Dashell jump both bridge gaps
                   r.has(SPMItem.PIXL_DASHELL),
                   # Float both bridge gaps
                   r.can_float()))

    r.connect(SPMEntrance.HE204_DEFAULT, SPMRegion.HE204, SPMRegion.HE203)

    r.connect(SPMEntrance.HE205_DEFAULT, SPMRegion.HE205, SPMRegion.HE203)
    r.location(SPMLocation.C12_OPEN_ITEM_BEHIND_GREENS_BED, r.can_flip())  # Item is in 3D

    r.connect(SPMEntrance.HE206_DOKAN_1, SPMRegion.HE206, SPMRegion.HE203)
    r.connect(SPMEntrance.HE206_DOA1_I, SPMRegion.HE206, SPMRegion.HE209)  # ER might require some face tanking thwomps

    r.connect(SPMEntrance.HE207_DOA1_I, SPMRegion.HE207, SPMRegion.HE209,
              r.has(SPMItem.PIXL_THOREAU))

    r.connect(SPMEntrance.HE208_DOKAN_1, SPMRegion.HE208, SPMRegion.HE203)

    r.connect(SPMEntrance.HE209_DOA1_I, SPMRegion.HE209, SPMRegion.HE206)
    r.connect(SPMEntrance.HE209_DOA2_I, SPMRegion.HE209, SPMRegion.HE207,
              r.has(SPMItem.PIXL_TIPPI))

    # Yold Desert (1-3)
    r.connect(SPMEntrance.HE301_DOA1_I, SPMRegion.HE301, SPMRegion.HE303)
    r.connect(SPMEntrance.HE301_DOA2_I, SPMRegion.HE301, SPMRegion.HE302)
    r.location(SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM,
               r.can_flip())

    r.connect(SPMEntrance.HE302_DOA1_I, SPMRegion.HE302, SPMRegion.HE301)
    r.location(SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM,
               r.can_flip())

    r.connect(SPMEntrance.HE303_DOKAN_1, SPMRegion.HE303, SPMRegion.HE305,
              r.if_any(
                  r.can_flip(),
                  r.can_float(),
                  r.has(SPMItem.PIXL_DASHELL),
                  r.if_all(
                      r.has(SPMItem.PIXL_THOREAU),
                      r.can_super_jump())))
    r.connect(SPMEntrance.HE303_DOA1_I, SPMRegion.HE303, SPMRegion.HE301)
    r.connect(SPMEntrance.HE303_DOA2_I, SPMRegion.HE303, SPMRegion.HE304,
              r.if_any(r.can_flip(), r.can_float(), r.has_any(SPMItem.PIXL_DASHELL, SPMItem.PIXL_THOREAU)))

    r.connect(SPMEntrance.HE304_DOA1_I, SPMRegion.HE304, SPMRegion.HE303)
    r.connect(SPMEntrance.HE304_DOA2_I, SPMRegion.HE304, SPMRegion.HE306)

    r.connect(SPMEntrance.HE305_DOKAN_1, SPMRegion.HE305, SPMRegion.HE303)

    r.connect(SPMEntrance.HE306_DOA1_I, SPMRegion.HE306, SPMRegion.HE307)
    r.connect(SPMEntrance.HE306_DOA2_I, SPMRegion.HE306, SPMRegion.HE304)
    r.connect(SPMEntrance.HE306_DOA3_I, SPMRegion.HE306, SPMRegion.HE308)
    r.location(SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM, r.can_flip())

    r.connect(SPMEntrance.HE307_DOA1_I, SPMRegion.HE307, SPMRegion.HE306)

    r.connect(SPMEntrance.HE308_DOA1_I, SPMRegion.HE308, SPMRegion.HE306)
    # r.location(SPMLocation.C13_STAR_BLOCK)

    # Yold Ruins (1-4)
    r.connect(SPMEntrance.HE401_DOA1_I, SPMRegion.HE401, SPMRegion.HE402)

    r.connect(SPMEntrance.HE402_DOA1_I, SPMRegion.HE402, SPMRegion.HE401)
    r.connect(SPMEntrance.HE402_DOA2_I, SPMRegion.HE402, SPMRegion.HE403)

    r.connect(SPMEntrance.HE403_DOA1_I, SPMRegion.HE403, SPMRegion.HE402)
    r.connect(SPMEntrance.HE403_DOA2_I, SPMRegion.HE403, SPMRegion.HE405,
              r.has(SPMItem.RUINS_KEY, 3))
    r.connect(SPMEntrance.HE403_DOA3_I, SPMRegion.HE403, SPMRegion.HE404,
              r.can_flip())  # Mario hits the 3d turn blocks below the door

    r.connect(SPMEntrance.HE404_DOA1_I, SPMRegion.HE404, SPMRegion.HE403)

    r.connect(SPMEntrance.HE405_DOA1_I, SPMRegion.HE405, SPMRegion.HE403)
    r.connect(SPMEntrance.HE405_DOA2_I, SPMRegion.HE405, SPMRegion.HE406)
    r.connect(SPMEntrance.HE405_DOA3_I, SPMRegion.HE405, SPMRegion.HE412,
              r.has(SPMItem.RUINS_KEY, 3))
    # TODO: THOREAU has to be patched to always be thrown at *Mario's* height!
    # Other characters are too tall and thus throw him too high to reach this and probably a couple other items.
    r.location(SPMLocation.C14_OPEN_KEY_BEHIND_BLOCKS,
               r.has_all(SPMItem.PIXL_THOREAU, SPMEvent.SWITCH_YOLD_RUINS_SQUIG_ROOM))

    r.connect(SPMEntrance.HE406_DOA1_I, SPMRegion.HE406, SPMRegion.HE405)
    r.event(SPMRegion.HE406, SPMEvent.SWITCH_YOLD_RUINS_SQUIG_ROOM, None,
            r.if_any(r.can_super_jump(), r.has(SPMItem.PIXL_THOREAU)))

    r.connect(SPMEntrance.HE407_DOA1_I, SPMRegion.HE407, SPMRegion.HE412)
    r.connect(SPMEntrance.HE407_DOA2_I, SPMRegion.HE407, SPMRegion.HE408,
              r.has(SPMItem.RUINS_KEY, 3))
    r.location(SPMLocation.C14_HIDDEN_CHEST_AFTER_3D_PATH, r.can_flip())
    r.location(SPMLocation.C14_OPEN_KEY_BETWEEN_FIRE_BARS, r.can_flip())

    r.connect(SPMEntrance.HE408_DOA1_I, SPMRegion.HE408, SPMRegion.HE407)
    r.connect(SPMEntrance.HE408_DOA2_I, SPMRegion.HE408, SPMRegion.HE409, r.can_flip())

    r.connect(SPMEntrance.HE409_DOKAN_1, SPMRegion.HE409, SPMRegion.HE410)
    r.connect(SPMEntrance.HE409_DOA1_I, SPMRegion.HE409, SPMRegion.HE408)

    r.connect(SPMEntrance.HE410_DOA1_I, SPMRegion.HE410, SPMRegion.HE411)

    r.connect(SPMEntrance.HE411_DOA1_I, SPMRegion.HE411, SPMRegion.HE410)

    r.connect(SPMEntrance.HE412_DOA1_I, SPMRegion.HE412, SPMRegion.HE405)
    r.connect(SPMEntrance.HE412_DOA2_I, SPMRegion.HE412, SPMRegion.HE407,
              r.has(SPMItem.PIXL_TIPPI))


def chapter2_rules(r: SPMRuleBuilder):
    # Gloam Valley (2-1)
    mi110_doors = r.if_any(
        r.if_all(
            r.can_super_jump(),
            r.has_any(SPMItem.PIXL_BOOMER, SPMItem.PIXL_CUDGE),
            r.can_fire(), r.has_any(SPMItem.CHARACTER_MARIO, SPMItem.CHARACTER_PEACH)))

    # Gloam Valley (2-1)
    r.connect(SPMEntrance.MI101_DOKAN_1, SPMRegion.MI101, SPMRegion.MI105,
              r.if_all(
                  r.can_flip(),
                  r.if_any(r.can_float(), r.has(SPMItem.PIXL_DASHELL))))
    r.connect(SPMEntrance.MI101_DOA1_I, SPMRegion.MI101, SPMRegion.MI108,
              r.if_all(
                  r.has(SPMItem.DOOR_KEY_21),
                  r.if_any(r.can_float(), r.has(SPMItem.PIXL_DASHELL))))

    r.connect(SPMEntrance.MI102_DOA1_I, SPMRegion.MI102, SPMRegion.MI110)
    # r.connect(SPMEntrance.MI102_DOA2_I, SPMRegion.MI102, SPMRegion.MI110) Unnecessary until ER
    r.event(SPMRegion.MI102, SPMEvent.SWITCH_GLOAM_VALLEY_UNDERGROUND, None,
            r.if_all(r.can_flip(), r.has(SPMItem.PIXL_BOOMER)))

    r.connect(SPMEntrance.MI103_DOA1_I, SPMRegion.MI103, SPMRegion.MI110)
    # r.connect(SPMEntrance.MI103_DOA2_I, SPMRegion.MI103, SPMRegion.MI110) Unnecessary until ER

    r.connect(SPMEntrance.MI104_DOA1_I, SPMRegion.MI104, SPMRegion.MI110)
    r.location(SPMLocation.C21_LEFT_CHEST_BEFORE_STAR_BLOCK,
               r.can_flip())
    r.location(SPMLocation.C21_RIGHT_CHEST_BEFORE_STAR_BLOCK,
               r.can_flip())

    r.connect(SPMEntrance.MI105_DOKAN_1, SPMRegion.MI105, SPMRegion.MI101)

    r.connect(SPMEntrance.MI106_DOKAN_1, SPMRegion.MI106, SPMRegion.MI110)
    r.connect(SPMEntrance.MI106_DOKAN_2, SPMRegion.MI106, SPMRegion.MI107)

    r.connect(SPMEntrance.MI107_DOKAN_1, SPMRegion.MI107, SPMRegion.MI106)
    # r.location(SPMLocation.C21_BOOMER_CHEST)
    r.location(SPMLocation.C21_CHEST_BEHIND_BOOMER_CHEST,
               r.if_all(r.can_flip(), r.has(SPMItem.PIXL_BOOMER)))

    r.connect(SPMEntrance.MI108_DOA1_I, SPMRegion.MI108, SPMRegion.MI101)
    r.connect(SPMEntrance.MI108_DOA2_I, SPMRegion.MI108, SPMRegion.MI109)
    r.connect(SPMEntrance.MI108_DOA3_I, SPMRegion.MI108, SPMRegion.MI111,
              r.has(SPMEvent.SWITCH_GLOAM_VALLEY_BACKGROUND))
    r.event(SPMRegion.MI108, SPMEvent.SWITCH_GLOAM_VALLEY_BACKGROUND, None,
            r.if_any(r.can_float(), r.has(SPMItem.PIXL_DASHELL)))

    r.connect(SPMEntrance.MI109_DOA1_I, SPMRegion.MI109, SPMRegion.MI108)

    r.connect(SPMEntrance.MI110_DOKAN_1, SPMRegion.MI110, SPMRegion.MI106,
              mi110_doors)
    r.connect(SPMEntrance.MI110_DOA1_I, SPMRegion.MI110, SPMRegion.MI111,
              mi110_doors)
    r.connect(SPMEntrance.MI110_DOA2_I, SPMRegion.MI110, SPMRegion.MI104,
              r.if_all(mi110_doors, r.has(SPMEvent.SWITCH_GLOAM_VALLEY_UNDERGROUND)))
    r.connect(SPMEntrance.MI110_DOA3_I, SPMRegion.MI110, SPMRegion.MI102,
              mi110_doors)
    r.connect(SPMEntrance.MI110_DOA4_I, SPMRegion.MI110, SPMRegion.MI103,
              mi110_doors)
    # r.connect(SPMEntrance.MI110_DOA5_I, SPMRegion.MI110, SPMRegion.MI103)
    # r.connect(SPMEntrance.MI110_DOA6_I, SPMRegion.MI110, SPMRegion.MI102)

    r.connect(SPMEntrance.MI111_DOA1_I, SPMRegion.MI111, SPMRegion.MI108)
    r.connect(SPMEntrance.MI111_DOA2_I, SPMRegion.MI111, SPMRegion.MI110)

    # Merlee's Mansion (2-2)
    r.connect(SPMEntrance.MI201_DOA_L, SPMRegion.MI201, SPMRegion.MI202)
    r.location(SPMLocation.C22_CHEST_ON_ROOF, r.can_flip())
    # r.location(SPMLocation.C22_CHEST_ABOVE_ENTRANCE)

    r.connect(SPMEntrance.MI202_DOA_L, SPMRegion.MI202, SPMRegion.MI201)
    r.connect(SPMEntrance.MI202_DOA_02_L, SPMRegion.MI202, SPMRegion.MI203,
              r.can_flip())

    r.connect(SPMEntrance.MI203_DOA1_L, SPMRegion.MI203, SPMRegion.MI202)
    r.connect(SPMEntrance.MI203_DOA2_L, SPMRegion.MI203, SPMRegion.MI207)
    r.connect(SPMEntrance.MI203_DOA3_L, SPMRegion.MI203, SPMRegion.MI204)
    r.connect(SPMEntrance.MI203_DOA4_L, SPMRegion.MI203, SPMRegion.MI205)
    r.connect(SPMEntrance.MI203_DOA5_L, SPMRegion.MI203, SPMRegion.MI206)
    r.connect(SPMEntrance.MI203_DOA6_L, SPMRegion.MI203, SPMRegion.MI208,
              r.has(SPMItem.HOUSE_KEY))

    r.connect(SPMEntrance.MI204_DOA2_L, SPMRegion.MI204, SPMRegion.MI203)
    r.connect(SPMEntrance.MI204_FALL, SPMRegion.MI204, SPMRegion.MI209)

    r.connect(SPMEntrance.MI205_DOA2_L, SPMRegion.MI205, SPMRegion.MI203)
    r.connect(SPMEntrance.MI205_FALL, SPMRegion.MI205, SPMRegion.MI210)

    r.connect(SPMEntrance.MI206_DOA2_L, SPMRegion.MI206, SPMRegion.MI203)
    r.location(SPMLocation.C22_CHEST_ABOVE_SPIKE_ROOF,
               r.if_all(
                   r.can_flip(),
                   r.has_any(SPMItem.PIXL_BOOMER, SPMItem.PIXL_CUDGE, SPMItem.CHARACTER_BOWSER)))

    r.connect(SPMEntrance.MI207_DOA2_L, SPMRegion.MI207, SPMRegion.MI203)
    r.connect(SPMEntrance.MI207_FALL, SPMRegion.MI207, SPMRegion.MI211)

    r.connect(SPMEntrance.MI208_DOA2_L, SPMRegion.MI208, SPMRegion.MI203)
    # r.location(SPMLocation.C22_STAR_BLOCK)

    r.connect(SPMEntrance.MI209_DOKAN_1, SPMRegion.MI209, SPMRegion.MI204,
              r.has(SPMItem.PIXL_BOOMER))  # Need boomer to defeat the shlurp

    r.connect(SPMEntrance.MI210_DOKAN_1, SPMRegion.MI210, SPMRegion.MI205,
              r.if_any(
                  # Just barely enough to fire breath the switch and ride carrie out
                  r.if_all(r.can_fire(), r.has(SPMItem.PIXL_CARRIE)),
                  # Dashell can be used to speed into the pipe faster than it disappears
                  r.has_any(SPMItem.PIXL_BOOMER, SPMItem.PIXL_DASHELL)))

    r.connect(SPMEntrance.MI211_DOKAN_1, SPMRegion.MI211, SPMRegion.MI207,
              r.if_any(
                  # Just barely enough to fire breath the switch and ride carrie out
                  r.if_all(r.can_fire(), r.has(SPMItem.PIXL_CARRIE)),
                  # Dashell can be used to speed into the pipe faster than it disappears
                  r.has_any(SPMItem.PIXL_BOOMER, SPMItem.PIXL_DASHELL)))

    # Merlee's Mansion (2-3)

    # Merlee's Basement (2-4)


def chapter3_rules(r: SPMRuleBuilder):
    pass


def chapter4_rules(r: SPMRuleBuilder):
    pass


def chapter5_rules(r: SPMRuleBuilder):
    pass


def chapter6_rules(r: SPMRuleBuilder):
    pass


def chapter7_rules(r: SPMRuleBuilder):
    pass


def chapter8_rules(r: SPMRuleBuilder):
    # Replace with LS411 when Chapter 8 connections are done
    r.event(SPMRegion.LS401, SPMLocation.CHAPTER_8_4_END, SPMEvent.VICTORY,
            r.if_all(r.has_group_unique("Hearts", r.options.pure_hearts_required),
                     r.has_group_unique("Heroes", 4)))
