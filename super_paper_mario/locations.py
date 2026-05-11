from dataclasses import replace
from typing import Callable, TypedDict

from BaseClasses import Location

from . import items
from .names import ELocationName
from .names import EventName as E
from .names import ItemName as I
from .names import LocationName as L
from .names import RegionName as R
from .options import ChapterDoorAccess, FlopsidePitAccess, PitAccess, SuperPaperMarioOptions
from .types import (
    GSW,
    GSWF,
    LocationConfig,
    LocationData,
    LocationSetup,
    SPMLocation,
    SPMWorldBase,
)
from .types import (
    RandomizationType as RT,
)


def get_location_names_with_ids(location_names: list[L]) -> dict[str, int]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


class LocationConfigOverride(TypedDict, total=False):
    setting: RT


TAG_HEART_PILLAR = "hp"
TAG_PURE_HEART = "ph"
TAG_STAR_BLOCK = "star"
TAG_FETCH = "tq"
TAG_FLIPSIDE_PIT = "flippit"
TAG_FLIPSIDE_PIT_ENT = "flippit_entrance"
TAG_FLOPSIDE_PIT = "floppit"
TAG_FLOPSIDE_PIT_ENT = "floppit_entrance"
TAG_FLAMM = "flammspot"
TAG_TREASURE = "treasurespot"


CONFIG_OVERRIDES: dict[str, tuple[Callable[[SuperPaperMarioOptions], bool], LocationConfigOverride]] = {
    # TAG_HEART_PILLAR: (lambda options: options.chapter_door_access == ChapterDoorAccess.option_chapters_closed, {"count": 1}),
    TAG_PURE_HEART: (lambda options: options.shuffle_pure_hearts.value, {"setting": RT.RANDOM}),
    TAG_STAR_BLOCK: (
        lambda options: options.chapter_door_access == ChapterDoorAccess.option_chapters_open,
        {"setting": RT.VANILLA_EVENT},
    ),
    # TAG_SHOP:
    TAG_FETCH: (lambda options: options.trading_quest.value, {"setting": RT.RANDOM}),
    TAG_FLIPSIDE_PIT: (lambda options: options.flipside_pit_access != PitAccess.option_closed, {"setting": RT.RANDOM}),
    TAG_FLOPSIDE_PIT: (lambda options: options.flopside_pit_access != PitAccess.option_closed, {"setting": RT.RANDOM}),
}


def prepare_location_data(world: SPMWorldBase) -> list[LocationSetup]:
    # Construct a dictionary of tag to count/classification to override LocationData defaults
    overrides: dict[str, LocationConfigOverride] = {
        tag: override for tag, (func, override) in CONFIG_OVERRIDES.items() if func(world.options)
    }

    # Apply the overrides from the base loc data
    return [
        (loc_data, replace(loc_config, **overrides[loc_data.tag]))
        if loc_data.tag and overrides.get(loc_data.tag, None) is not None
        else (loc_data, loc_config)
        for loc_data, loc_config in LOCATION_SETUP
    ]


def create_all_locations(world: SPMWorldBase, locations: list[LocationSetup]):
    # This also returns the filler weights
    region_map = world.rm
    for data, config in locations:
        rt = config.setting
        if rt == RT.VANILLA_WORLD:
            loc = SPMLocation(
                world.player,
                data.name.value,
                LOCATION_NAME_TO_ID[data.name.value],
                region_map[data.region.value],
            )
            loc.place_locked_item(world.create_item(data.item.value))
            region_map[data.region].locations.append(loc)
        elif rt == RT.VANILLA_EVENT:
            region_map[data.region].add_event(data.name.value, data.item.value, None, SPMLocation, items.SPMItem)
        elif rt == RT.RANDOM:
            region_map[data.region].locations.append(
                SPMLocation(
                    world.player,
                    data.name.value,
                    LOCATION_NAME_TO_ID[data.name.value],
                    region_map[data.region.value],
                )
            )


def get_location_map(
    world: SPMWorldBase, location_names: list[ELocationName] | None = None
) -> dict[ELocationName, Location]:
    if location_names is None or len(location_names) == 0:
        location_names = [*L, *E]
    return {location.name: location for location in world.get_locations() if location.name in location_names}


# Groups
GROUP_FLIPSIDE_PIT = "Flipside Pit"
GROUP_FLOPSIDE_PIT = "Flopside Pit"
GROUP_PIT = "Pit"
GROUP_SHOP = "Shop"


# Randomization settings
def heart_pillar(opt: SuperPaperMarioOptions) -> RT:
    return RT.DISABLED
    # return RT.RANDOM if opt.chapter_door_access != ChapterDoorAccess.option_open else RT.DISABLED


def pure_heart(opt: SuperPaperMarioOptions) -> RT:
    return RT.RANDOM if opt.shuffle_pure_hearts else RT.VANILLA_WORLD


def star_block(opt: SuperPaperMarioOptions) -> RT:
    return RT.DISABLED if opt.chapter_door_access == ChapterDoorAccess.option_subchapters_open else RT.VANILLA_EVENT


def shop(opt: SuperPaperMarioOptions) -> RT:
    return RT.RANDOM


def fetch(opt: SuperPaperMarioOptions) -> RT:
    return RT.RANDOM if opt.trading_quest else RT.DISABLED


def flipside_pit(opt: SuperPaperMarioOptions) -> RT:
    return RT.DISABLED if opt.flipside_pit_access == PitAccess.option_closed else RT.RANDOM


def flopside_pit(opt: SuperPaperMarioOptions) -> RT:
    return RT.DISABLED if opt.flopside_pit_access == FlopsidePitAccess.option_closed else RT.RANDOM


def flamm(opt: SuperPaperMarioOptions) -> RT:
    return (
        RT.DISABLED
        if opt.treasure_maps.flamm_disabled
        else RT.VANILLA_WORLD
        if opt.treasure_maps.flamm_vanilla
        else RT.RANDOM
    )


def treasure_spot(opt: SuperPaperMarioOptions) -> RT:
    return RT.DISABLED if opt.treasure_maps.treasures_disabled else RT.RANDOM


CFG_RANDOM = LocationConfig(setting=RT.RANDOM)
CFG_DISABLED = LocationConfig(setting=RT.DISABLED)
CFG_EVENT = LocationConfig(setting=RT.VANILLA_EVENT)
CFG_LOCKED = LocationConfig(setting=RT.VANILLA_WORLD)


###
# WARNING: ALL LOCATION IDS STILL SUBJECT TO CHANGE, DO NOT REFERENCE THESE
###
LOCATION_SETUP: list[LocationSetup] = [
    # region Heart Pillars
    (
        LocationData(
            name=L.FLIPSIDE_HEART_PILLAR_RED,
            code=1,
            rom=0,
            var=GSW(0, 8),
            item=I.CHAPTER_1_1_KEY,
            region=R.MAC01_LAYER1,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HEART_PILLAR_ORANGE,
            code=2,
            rom=0,
            var=GSW(0, 65),
            item=I.CHAPTER_2_1_KEY,
            region=R.MAC06_LAYER2,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HEART_PILLAR_YELLOW,
            code=3,
            rom=0,
            var=GSW(0, 100),
            item=I.CHAPTER_3_1_KEY,
            region=R.MAC07_LAYER2,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HEART_PILLAR_GREEN,
            code=4,
            rom=0,
            var=GSW(0, 128),
            item=I.CHAPTER_4_1_KEY,
            region=R.MAC02_LAYER3,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_HEART_PILLAR_CYAN,
            code=5,
            rom=0,
            var=GSW(0, 177),
            item=I.CHAPTER_5_1_KEY,
            region=R.MAC11_LAYER1,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_HEART_PILLAR_BLUE,
            code=6,
            rom=0,
            var=GSW(0, 224),
            item=I.CHAPTER_6_1_KEY,
            region=R.MAC16_LAYER2,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_HEART_PILLAR_PURPLE,
            code=7,
            rom=0,
            var=GSW(0, 303),
            item=I.CHAPTER_7_1_KEY,
            region=R.MAC17_LAYER2,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_HEART_PILLAR_WHITE,
            code=8,
            rom=0,
            var=GSW(0, 356),
            item=I.CHAPTER_8_1_KEY,
            region=R.MAC12_LAYER3,
            tag="hp",
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region Shop Locations
    # I don't know if the vanilla items are listed in the correct order
    # MOD: What script variable or otherwise can be used to keep track of shop purcheses?
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_1,
            code=9,
            rom=0,
            var=None,
            item=I.SHROOM_SHAKE,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_2,
            code=10,
            rom=0,
            var=None,
            item=I.LONG_LAST_SHAKE,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_3,
            code=11,
            rom=0,
            var=None,
            item=I.LIFE_SHROOM,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_4,
            code=12,
            rom=0,
            var=None,
            item=I.FIRE_BURST,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_5,
            code=13,
            rom=0,
            var=None,
            item=I.ICE_STORM,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_6,
            code=14,
            rom=0,
            var=None,
            item=I.SLEEPY_SHEEP,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_7,
            code=15,
            rom=0,
            var=None,
            item=I.COURAGE_SHELL,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_8,
            code=16,
            rom=0,
            var=None,
            item=I.SHELL_SHOCK,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_9,
            code=17,
            rom=0,
            var=None,
            item=I.STAR_MEDAL,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_HOWZITS_10,
            code=18,
            rom=0,
            var=None,
            item=I.GOLD_BAR,
            region=R.MAC02_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_ITTY_BITS_1,
            code=19,
            rom=0,
            var=None,
            item=I.HONEY_JAR,
            region=R.MAC04_ITTY_BITS,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_ITTY_BITS_2,
            code=20,
            rom=0,
            var=None,
            item=I.BIG_EGG,
            region=R.MAC04_ITTY_BITS,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_ITTY_BITS_3,
            code=21,
            rom=0,
            var=None,
            item=I.CAKE_MIX,
            region=R.MAC04_ITTY_BITS,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_1,
            code=22,
            rom=0,
            var=None,
            item=I.VOLT_SHROOM,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_2,
            code=23,
            rom=0,
            var=None,
            item=I.BLOCK_BLOCK,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_3,
            code=24,
            rom=0,
            var=None,
            item=I.STOP_WATCH,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_4,
            code=25,
            rom=0,
            var=None,
            item=I.MIGHTY_TONIC,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_5,
            code=26,
            rom=0,
            var=None,
            item=I.SUPER_SHROOM_SHAKE,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_6,
            code=27,
            rom=0,
            var=None,
            item=I.THUNDER_RAGE,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_7,
            code=28,
            rom=0,
            var=None,
            item=I.GHOST_SHROOM,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_8,
            code=29,
            rom=0,
            var=None,
            item=I.ULTRA_SHROOM_SHAKE,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_9,
            code=30,
            rom=0,
            var=None,
            item=I.GOLD_BAR_X3,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_NOTSOS_10,
            code=31,
            rom=0,
            var=None,
            item=I.GOLD_MEDAL,
            region=R.MAC12_LAYER1,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_ITTY_BITS_1,
            code=32,
            rom=0,
            var=None,
            item=I.FRESH_PASTA_BUNCH,
            region=R.MAC14_L_ITTY_BITS,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_ITTY_BITS_2,
            code=33,
            rom=0,
            var=None,
            item=I.POWER_STEAK,
            region=R.MAC14_L_ITTY_BITS,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_ITTY_BITS_3,
            code=34,
            rom=0,
            var=None,
            item=I.SMELLY_HERB,
            region=R.MAC14_L_ITTY_BITS,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_1, code=35, rom=0, var=None, item=I.FIRE_BURST, region=R.HE203, groups={GROUP_SHOP}
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_2, code=36, rom=0, var=None, item=I.POW_BLOCK, region=R.HE203, groups={GROUP_SHOP}
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_3,
            code=37,
            rom=0,
            var=None,
            item=I.SHROOM_SHAKE,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_4,
            code=38,
            rom=0,
            var=None,
            item=I.LONG_LAST_SHAKE,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_5,
            code=39,
            rom=0,
            var=None,
            item=I.LIFE_SHROOM,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_6,
            code=40,
            rom=0,
            var=None,
            item=I.SLEEPY_SHEEP,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_7,
            code=41,
            rom=0,
            var=None,
            item=I.SHELL_SHOCK,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_8,
            code=42,
            rom=0,
            var=None,
            item=I.MIGHTY_TONIC,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_9,
            code=43,
            rom=0,
            var=None,
            item=I.COURAGE_SHELL,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.YOLD_TOWN_HOWZITS_10,
            code=44,
            rom=0,
            var=None,
            item=I.VOLT_SHROOM,
            region=R.HE203,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.DOTWOOD_TREE_ITTY_BITS_1,
            code=45,
            rom=0,
            var=None,
            item=I.PEACHY_PEACH,
            region=R.TA301_DOTWOOD_SHOP,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.DOTWOOD_TREE_ITTY_BITS_2,
            code=46,
            rom=0,
            var=None,
            item=I.FRESH_VEGGIE,
            region=R.TA301_DOTWOOD_SHOP,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.DOTWOOD_TREE_ITTY_BITS_3,
            code=47,
            rom=0,
            var=None,
            item=I.HORSETAIL,
            region=R.TA301_DOTWOOD_SHOP,
            groups={GROUP_SHOP},
        ),
        CFG_RANDOM,
    ),
    # TODO: Need regions on these
    # (
    #     LocationData(
    #         name=L.OUTER_LIMITS_HOWZITS_TWINKLE_MART_1,
    #         code=48,
    #         rom=0,
    #         var=None,
    #         item=I.GOLDEN_CHOCO_BAR,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.OUTER_LIMITS_HOWZITS_TWINKLE_MART_2,
    #         code=49,
    #         rom=0,
    #         var=None,
    #         item=I.SHROOM_CHOCO_BAR,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.OUTER_LIMITS_HOWZITS_TWINKLE_MART_3,
    #         code=50,
    #         rom=0,
    #         var=None,
    #         item=I.SWEET_CHOCO_BAR,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_1,
    #         code=51,
    #         rom=0,
    #         var=None,
    #         item=I.COURAGE_SHELL,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_2,
    #         code=52,
    #         rom=0,
    #         var=None,
    #         item=I.FIRE_BURST,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_3, code=53, rom=0, var=None, item=I.ICE_STORM, region=None, groups={GROUP_SHOP}
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_4,
    #         code=54,
    #         rom=0,
    #         var=None,
    #         item=I.LIFE_SHROOM,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_5,
    #         code=55,
    #         rom=0,
    #         var=None,
    #         item=I.MYSTERY_BOX,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_6, code=56, rom=0, var=None, item=I.POW_BLOCK, region=None, groups={GROUP_SHOP}
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_7,
    #         code=57,
    #         rom=0,
    #         var=None,
    #         item=I.PRIMORDIAL_FRUIT,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_8,
    #         code=58,
    #         rom=0,
    #         var=None,
    #         item=I.SHROOM_SHAKE,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_9,
    #         code=59,
    #         rom=0,
    #         var=None,
    #         item=I.SLEEPY_SHEEP,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_HOWZITS_10,
    #         code=60,
    #         rom=0,
    #         var=None,
    #         item=I.SUPER_SHROOM_SHAKE,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_ITTY_BITS_1,
    #         code=61,
    #         rom=0,
    #         var=None,
    #         item=I.KEEL_MANGO,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.DOWNTOWN_CRAG_ITTY_BITS_2,
    #         code=62,
    #         rom=0,
    #         var=None,
    #         item=I.MILD_COCOA_BEAN,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.THE_OVERTHERE_ITTY_BITS_1, code=63, rom=0, var=None, item=I.HOT_DOG, region=None, groups={GROUP_SHOP}
    #     ),
    #     CFG_RANDOM,
    # ),
    # (
    #     LocationData(
    #         name=L.THE_OVERTHERE_ITTY_BITS_2,
    #         code=64,
    #         rom=0,
    #         var=None,
    #         item=I.HOT_SAUCE,
    #         region=None,
    #         groups={GROUP_SHOP},
    #     ),
    #     CFG_RANDOM,
    # ),
    # endregion
    # region Flipside
    # These 2 locations are only here to reserve the ids in case we rework how
    # the starting items work similar to TTYD.
    # (LocationData(name=L.FLIPSIDE_STARTING_CHARACTER
    # , code=65
    # , rom=None
    # , var=None
    # , item=I.CHARACTER_MARIO
    # , region=None
    # , setting=RT.VANILLA_EVENT
    # ), CFG_RANDOM),
    # (LocationData(name=L.FLIPSIDE_STARTING_PIXL
    # , code=66
    # , rom=None
    # , var=None
    # , item=I.PIXL_TIPPI
    # , region=None
    # , setting=RT.VANILLA_EVENT
    # ), CFG_RANDOM),
    (
        LocationData(
            name=L.FLIPSIDE_MERLONS_GIFT,
            code=67,
            rom=None,
            var=None,
            item=I.RED_PURE_HEART,
            region=R.MAC02_L_TOWER,
            tag="ph",
        ),
        CFG_LOCKED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK,
            code=68,
            rom=0,
            var=GSWF(527),
            item=I.CATCH_CARD_MERLEE,
            region=R.MAC01_LAYER2,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS,
            code=69,
            rom=0,
            var=GSWF(580),
            item=I.COOKING_DISK_R,
            region=R.MAC01_LAYER2,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_3F_EAT_A_SPICY_SOUP,
            code=70,
            rom=0,
            var=GSW(0, 63),
            item=I.CHARACTER_PEACH,
            region=R.MAC01_LAYER1,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_3F_FISHBOWL,
            code=71,
            rom=0,
            var=GSW(0, 133),
            item=I.GOLDFISH_BOWL_FISH,
            region=R.MAC01_LAYER1,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_1F_OUTSKIRTS_LEFT_CHEST_IN_HOLE,
            code=72,
            rom=0,
            var=GSWF(523),
            item=I.CATCH_CARD_MERLON,
            region=R.MAC08,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_1F_OUTSKIRTS_RIGHT_CHEST_IN_HOLE,
            code=73,
            rom=0,
            var=GSWF(522),
            item=I.CATCH_CARD_MERLUVLEE,
            region=R.MAC08,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_B1_3D_CHEST,
            code=74,
            rom=0,
            var=GSWF(520),
            item=I.CATCH_CARD_THE_INTER_NED,
            region=R.MAC04_LAYER1,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_B1_OUTSKIRTS_CHEST_BEHIND_PILLAR,
            code=75,
            rom=0,
            var=GSWF(521),
            item=I.CATCH_CARD_THE_INTER_CHET,
            region=R.MAC07_LAYER1,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_B1_FREE_FISH,
            code=76,
            rom=0,
            var=GSW(0, 134),
            item=I.GOLDFISH_BOWL_EMPTY,
            region=R.MAC04_LAYER1,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_B2_CHEST_AFTER_PIPE, code=77, rom=0, var=GSWF(503), item=I.HP_PLUS, region=R.MAC05_LAYER2
        ),
        CFG_RANDOM,
    ),
    # endregion
    # region Flopside
    (
        LocationData(
            name=L.FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK,
            code=78,
            rom=0,
            var=GSWF(529),
            item=I.CATCH_CARD_NOLREM,
            region=R.MAC11_LAYER2,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS,
            code=79,
            rom=0,
            var=GSWF(581),
            item=I.COOKING_DISK_W,
            region=R.MAC11_LAYER2,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK,
            code=80,
            rom=0,
            var=None,
            item=E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK,
            region=R.MAC15_LAYER2,
        ),
        CFG_EVENT,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_B2_CHEST_AFTER_PIPE, code=81, rom=0, var=GSWF(506), item=I.POWER_PLUS, region=R.MAC15_LAYER2
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=E.FLEEP_FLOPSIDE_PIT_CAGE,
            code=82,
            rom=None,
            var=None,
            item=E.FLEEP_FLOPSIDE_PIT_CAGE,
            region=R.L_FLOPSIDE_PIT_TOP,
        ),
        CFG_EVENT,
    ),
    (
        LocationData(
            name=E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK,
            code=83,
            rom=None,
            var=None,
            item=E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK,
            region=R.MAC17_LAYER2,
        ),
        CFG_EVENT,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_B2_CHASM_CHEST, code=84, rom=0, var=GSWF(525), item=I.CATCH_CARD_BARRY, region=R.MAC18
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_B1_BEVERAGARIUM_CHEST1,
            code=85,
            rom=0,
            var=GSWF(537),
            item=I.GOLDEN_CARD,
            region=R.MAC14_L_BACK_BEVERAGARIUM,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_B1_BEVERAGARIUM_CHEST2,
            code=86,
            rom=0,
            var=GSWF(583),
            item=I.COOKING_DISK_B,
            region=R.MAC14_L_BACK_BEVERAGARIUM,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_B1_OUTSKIRT_CHEST_BEHIND_PILLAR,
            code=87,
            rom=0,
            var=GSWF(524),
            item=I.CATCH_CARD_PICCOLO,
            region=R.MAC17_LAYER1,
        ),
        CFG_RANDOM,
    ),
    # endregion
    # region Piccolo's Fetch Quest
    (
        LocationData(
            name=L.PICCOLO_FETCH_WATCHITT_1, code=88, rom=0, var=GSWF(413), item=I.PAPER, region=R.HE203, tag="tq"
        ),
        CFG_DISABLED,
    ),
    # TODO: I don't remember where you find her during the quest? HE411? HE203?
    # (
    #     LocationData(
    #         name=L.PICCOLO_FETCH_MERLUMINA, code=89, rom=0, var=GSWF(414), item=I.AUTOGRAPH, region=None, tag="tq"
    #     ),
    #     CFG_DISABLED,
    # ),
    (
        LocationData(
            name=L.PICCOLO_FETCH_WATCHITT_2,
            code=90,
            rom=0,
            var=GSWF(415),
            item=I.YOU_KNOW_WHAT,
            region=R.HE203,
            tag="tq",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.PICCOLO_FETCH_BESTOVIUS,
            code=91,
            rom=0,
            var=GSWF(416),
            item=I.TRAINING_MACHINE,
            region=R.HE101,
            tag="tq",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.PICCOLO_FETCH_MERLUVLEE,
            code=92,
            rom=0,
            var=GSWF(417),
            item=I.CRYSTAL_BALL,
            region=R.MAC02_LAYER1,
            tag="tq",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.PICCOLO_FETCH_MERLEE,
            code=93,
            rom=0,
            var=GSWF(418),
            item=I.RANDOM_HOUSE_KEY,
            region=R.MAC12_LAYER1,
            tag="tq",
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.PICCOLO_FETCH_END,
            code=94,
            rom=0,
            var=GSWF(517),
            item=I.PIXL_PICCOLO,
            region=R.MAC19_LAYER1,
            tag="tq",
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region Flipside Pit
    (
        LocationData(
            name=E.SWITCH_FLIPSIDE_PIT_CAGE,
            code=95,
            rom=0,
            var=GSWF(501),
            item=E.SWITCH_FLIPSIDE_PIT_CAGE,
            region=R.L_FLIPSIDE_PIT_TOP,
        ),
        CFG_EVENT,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_10,
            code=96,
            rom=0,
            var=GSWF(433),
            item=I.CATCH_CARD_TIPPI,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_20,
            code=97,
            rom=0,
            var=GSWF(434),
            item=I.CATCH_CARD_THOREAU,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_30,
            code=98,
            rom=0,
            var=GSWF(435),
            item=I.CATCH_CARD_BOOMER,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_40,
            code=99,
            rom=0,
            var=GSWF(436),
            item=I.CATCH_CARD_SLIM,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_50,
            code=100,
            rom=0,
            var=GSWF(437),
            item=I.CATCH_CARD_THUDLEY,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_60,
            code=101,
            rom=0,
            var=GSWF(438),
            item=I.CATCH_CARD_CARRIE,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_70,
            code=102,
            rom=0,
            var=GSWF(439),
            item=I.CATCH_CARD_FLEEP,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_80,
            code=103,
            rom=0,
            var=GSWF(440),
            item=I.CATCH_CARD_CUDGE,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_90,
            code=104,
            rom=0,
            var=GSWF(441),
            item=I.CATCH_CARD_DOTTIE,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_100,
            code=105,
            rom=0,
            var=GSWF(389),  # 2 flags for wracktail? 389/409
            item=I.PIXL_DASHELL,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLIPSIDE_PIT_WRACKTAIL,
            code=106,
            rom=0,
            var=GSWF(408),
            item=E.COMPLETED_FLIPSIDE_PIT,
            region=R.L_FLIPSIDE_PIT,
            tag="flippit_entrance",
            groups={GROUP_FLIPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region Flopside Pit
    (
        LocationData(
            name=L.FLOPSIDE_PIT_10,
            code=107,
            rom=0,
            var=GSWF(442),
            item=I.CATCH_CARD_DASHELL,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_20,
            code=108,
            rom=0,
            var=GSWF(443),
            item=I.CATCH_CARD_GOOMBARIO,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_30,
            code=109,
            rom=0,
            var=GSWF(444),
            item=I.CATCH_CARD_KOOPER,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_40,
            code=110,
            rom=0,
            var=GSWF(445),
            item=I.CATCH_CARD_BOMBETTE,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_50,
            code=111,
            rom=0,
            var=GSWF(446),
            item=I.CATCH_CARD_PARAKARRY,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_60,
            code=112,
            rom=0,
            var=GSWF(447),
            item=I.CATCH_CARD_BOW,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_70,
            code=113,
            rom=0,
            var=GSWF(448),
            item=I.CATCH_CARD_WATT,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_80,
            code=114,
            rom=0,
            var=GSWF(449),
            item=I.CATCH_CARD_SUSHIE,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_90,
            code=115,
            rom=0,
            var=GSWF(450),
            item=I.CATCH_CARD_LAKILESTER,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_1,
            code=116,
            rom=0,
            var=None,
            item=I.CATCH_CARD_MARIO,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_2,
            code=117,
            rom=0,
            var=None,
            item=I.CATCH_CARD_DARK_MARIO,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_3,
            code=118,
            rom=0,
            var=None,
            item=I.CATCH_CARD_PEACH_1,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_4,
            code=119,
            rom=0,
            var=None,
            item=I.CATCH_CARD_DARK_PEACH,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_5,
            code=120,
            rom=0,
            var=None,
            item=I.CATCH_CARD_BOWSER_1,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_6,
            code=121,
            rom=0,
            var=None,
            item=I.CATCH_CARD_DARK_BOWSER,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_7,
            code=122,
            rom=0,
            var=None,
            item=I.CATCH_CARD_LUIGI,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_100_8,
            code=123,
            rom=0,
            var=None,
            item=I.CATCH_CARD_DARK_LUIGI,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLOPSIDE_PIT_SHADOO,
            code=124,
            rom=0,
            var=None,
            item=E.COMPLETED_FLOPSIDE_PIT,
            region=R.L_FLOPSIDE_PIT,
            tag="floppit_entrance",
            groups={GROUP_FLOPSIDE_PIT, GROUP_PIT},
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 1-1
    (
        LocationData(
            name=L.C11_OPEN_ITEM_BEHIND_PIPE, code=125, rom=0, var=GSWF(603), item=I.CATCH_CARD_GOOMBA, region=R.HE102
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_CHEST_AFTER_STAR_BLOCK,
            code=126,
            rom=0,
            var=GSWF(604),
            item=I.CATCH_CARD_KOOPA_TROOPA,
            region=R.HE105,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_OPEN_ITEM_ABOVE_BESTOVIUS_HOUSE,
            code=127,
            rom=0,
            var=GSWF(611),
            item=I.CATCH_CARD_SQUIGLET,
            region=R.HE101,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_CHEST_INSIDE_FIRST_PIPE, code=128, rom=0, var=GSWF(612), item=I.SHROOM_SHAKE, region=R.HE103
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM,
            code=129,
            rom=0,
            var=GSWF(614),
            item=I.SHELL_SHOCK,
            region=R.HE106,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY,
            code=130,
            rom=0,
            var=GSWF(615),
            item=I.FIRE_BURST,
            region=R.HE101,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_TALK_TO_BESTOVIUS, code=131, rom=0, var=GSW(0, 16), item=I.ABILITY_FLIP, region=R.HE106
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM,
            code=132,
            rom=0,
            var=GSWF(616),
            item=I.SHROOM_SHAKE,
            region=R.HE106,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C11_STAR_BLOCK,
            code=133,
            rom=0,
            var=GSW(0, 17),
            item=I.CHAPTER_1_2_KEY,
            region=R.HE105,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 1-2
    (
        LocationData(name=L.C12_THOREAU_CHEST, code=134, rom=0, var=GSW(0, 25), item=I.PIXL_THOREAU, region=R.HE207),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C12_CHEST_IN_SHORTCUT, code=135, rom=0, var=GSWF(605), item=I.CATCH_CARD_PARATROOPA, region=R.HE201
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE,
            code=136,
            rom=0,
            var=GSWF(610),
            item=I.CATCH_CARD_BOOMBOXER,
            region=R.HE203,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C12_OPEN_ITEM_BEHIND_GREENS_BED,
            code=137,
            rom=0,
            var=GSWF(618),
            item=I.CATCH_CARD_RED_GREEN,
            region=R.HE205,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C12_STAR_BLOCK,
            code=138,
            rom=0,
            var=GSW(0, 28),
            item=I.CHAPTER_1_3_KEY,
            region=R.HE203,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 1-3
    (
        LocationData(
            name=L.C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM,
            code=139,
            rom=0,
            var=GSWF(606),
            item=I.CATCH_CARD_SQUIG,
            region=R.HE301,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM,
            code=140,
            rom=0,
            var=GSWF(607),
            item=I.COURAGE_SHELL,
            region=R.HE302,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM,
            code=141,
            rom=0,
            var=GSWF(608),
            item=I.GHOST_SHROOM,
            region=R.HE306,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C13_STAR_BLOCK,
            code=142,
            rom=0,
            var=GSW(0, 38),
            item=I.CHAPTER_1_4_KEY,
            region=R.HE308,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 1-4
    (
        LocationData(
            name=L.C14_CHEST_IN_SECOND_ROOM, code=143, rom=0, var=GSWF(609), item=I.LIFE_SHROOM, region=R.HE402
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C14_CHEST_IN_SMALL_SPIKY_TROMP_ROOM,
            code=144,
            rom=0,
            var=GSW(0, 40),
            item=I.RUINS_KEY,
            region=R.HE404,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C14_OPEN_KEY_BEHIND_BLOCKS, code=145, rom=0, var=GSW(0, 43), item=I.RUINS_KEY, region=R.HE405
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=E.SWITCH_YOLD_RUINS_SQUIG_ROOM,
            code=146,
            rom=0,
            var=GSW(0, 42),
            item=E.SWITCH_YOLD_RUINS_SQUIG_ROOM,
            region=R.HE406,
        ),
        CFG_EVENT,
    ),
    (
        LocationData(
            name=L.C14_HIDDEN_CHEST_AFTER_3D_PATH,
            code=147,
            rom=0,
            var=GSWF(613),
            item=I.CATCH_CARD_BUZZY_BEETLE,
            region=R.HE407,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C14_OPEN_KEY_BETWEEN_FIRE_BARS, code=148, rom=0, var=GSW(0, 46), item=I.RUINS_KEY, region=R.HE407
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C14_ORANGE_PURE_HEART,
            code=149,
            rom=0,
            var=GSW(0, 53),
            item=I.ORANGE_PURE_HEART,
            region=R.HE411,
            tag="ph",
        ),
        CFG_LOCKED,
    ),
    # endregion
    # region 2-1
    (
        LocationData(
            name=E.SWITCH_GLOAM_VALLEY_UNDERGROUND,
            code=150,
            rom=None,
            var=None,
            item=E.SWITCH_GLOAM_VALLEY_UNDERGROUND,
            region=R.MI102,
        ),
        CFG_EVENT,
    ),
    (
        LocationData(
            name=E.SWITCH_GLOAM_VALLEY_BACKGROUND,
            code=151,
            rom=None,
            var=None,
            item=E.SWITCH_GLOAM_VALLEY_BACKGROUND,
            region=R.MI108,
        ),
        CFG_EVENT,
    ),
    (
        LocationData(name=L.C21_CHEST_AFTER_SQUIGS, code=152, rom=0, var=GSWF(735), item=I.DOOR_KEY_21, region=R.MI105),
        CFG_RANDOM,
    ),
    (
        LocationData(name=L.C21_BOOMER_CHEST, code=153, rom=0, var=GSW(0, 73), item=I.PIXL_BOOMER, region=R.MI107),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C21_CHEST_BEHIND_BOOMER_CHEST,
            code=154,
            rom=0,
            var=GSWF(738),
            item=I.CATCH_CARD_OLD_MAN_WATCHITT,
            region=R.MI107,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C21_LEFT_CHEST_BEFORE_STAR_BLOCK,
            code=155,
            rom=0,
            var=GSWF(732),
            item=I.CATCH_CARD_SHLURP,
            region=R.MI104,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C21_RIGHT_CHEST_BEFORE_STAR_BLOCK,
            code=156,
            rom=0,
            var=GSWF(733),
            item=I.CATCH_CARD_SWOOPER,
            region=R.MI104,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C21_STAR_BLOCK,
            code=157,
            rom=0,
            var=GSW(0, 76),
            item=I.CHAPTER_2_2_KEY,
            region=R.MI104,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # TODO=verify remaining script variables & items
    # region 2-2
    (
        LocationData(name=L.C22_CHEST_ON_ROOF, code=158, rom=0, var=GSWF(729), item=I.STOP_WATCH, region=R.MI201),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C22_CHEST_ABOVE_ENTRANCE, code=159, rom=0, var=GSWF(730), item=I.CATCH_CARD_CURSYA, region=R.MI201
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C22_OPEN_ITEM_DRAGGED_BY_ROPE, code=160, rom=None, var=None, item=I.MUSHROOM, region=R.MI207
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(name=L.C22_OPEN_ITEM_HUNG_BY_ROPE, code=161, rom=None, var=None, item=I.MUSHROOM, region=R.MI204),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C22_CHEST_ABOVE_SPIKE_ROOF, code=162, rom=0, var=GSW(0, 79), item=I.HOUSE_KEY, region=R.MI206
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C22_STAR_BLOCK,
            code=163,
            rom=0,
            var=GSW(0, 82),
            item=I.CHAPTER_2_3_KEY,
            region=R.MI208,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 2-3
    (
        LocationData(
            name=E.OPEN_THE_RUBEE_VAULT, code=164, rom=None, var=None, item=E.OPEN_THE_RUBEE_VAULT, region=R.MI301
        ),
        CFG_EVENT,
    ),
    (
        LocationData(
            name=L.C23_CHEST_BEHIND_BLOCKS, code=165, rom=None, var=None, item=I.CATCH_CARD_BOO, region=R.MI301
        ),
        CFG_RANDOM,
    ),
    (LocationData(name=L.C23_SLIM_CHEST, code=166, rom=None, var=None, item=I.PIXL_SLIM, region=R.MI301), CFG_RANDOM),
    (
        LocationData(
            name=L.C23_STAR_BLOCK,
            code=167,
            rom=None,
            var=None,
            item=I.CHAPTER_2_4_KEY,
            region=R.MI306,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 2-4
    (
        LocationData(
            name=L.C24_OPEN_ITEM_BEHIND_ROOM_08_SIGN, code=168, rom=None, var=None, item=I.SHROOM_SHAKE, region=R.MI410
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C24_YELLOW_PURE_HEART,
            code=169,
            rom=None,
            var=None,
            item=I.YELLOW_PURE_HEART,
            region=R.MI414,
            tag="ph",
        ),
        CFG_LOCKED,
    ),
    # endregion
    # region 3-1
    # TODO: Double check all locations, I couldn't find some of them initially.
    (
        LocationData(
            name=L.C31_TALK_TO_BARRY_AFTER_DEFEATING_FRANCIS,
            code=170,
            rom=None,
            var=GSWF(818),
            item=I.PIXL_BARRY,
            region=R.TA101_L_FOREGROUND,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C31_CHEST_IN_WARP_ZONE_RIGHT_PIPE,
            code=171,
            rom=None,
            var=GSWF(826),
            item=I.CATCH_CARD_MAGIKOOPA,
            region=R.TA107,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C31_OPEN_ITEM_IN_BACKGROUND,
            code=172,
            rom=None,
            var=GSWF(821),
            item=I.CATCH_CARD_SP,
            region=R.TA102_L_BACKGROUND,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C31_CHEST_IN_BACKGROUND_PIPE, code=173, rom=None, var=GSWF(832), item=I.THUNDER_RAGE, region=R.TA105
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C31_CHEST_ABOVE_COLORFUL_PERSONS,
            code=174,
            rom=None,
            var=GSWF(820),
            item=I.CATCH_CARD_PIRANHA_PLANT,
            region=R.TA101_L_FOREGROUND,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C31_OPEN_ITEM_IN_BACKGROUND_2,
            code=175,
            rom=None,
            var=GSWF(822),
            item=I.CATCH_CARD_SP,
            region=R.TA106,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C31_BOWSER,
            code=176,
            rom=None,
            var=GSW(0, 104),
            item=I.CHARACTER_BOWSER,
            region=R.TA104,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C31_STAR_BLOCK,
            code=177,
            rom=None,
            var=GSW(0, 105),
            item=I.CHAPTER_3_2_KEY,
            region=R.TA104,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 3-2
    (
        LocationData(
            name=L.C32_HIDDEN_CHEST_NEAR_PIPE, code=178, rom=None, var=GSWF(823), item=I.GOLD_BAR, region=R.TA202
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C32_THUDLEY_CHEST, code=179, rom=None, var=None, item=I.PIXL_THUDLEY, region=R.TA204
        ),  # MOD: TODO: This doesn't have an associated script var? closest is GSW(108) unlocking the cage *with* thudley
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C32_STAR_BLOCK,
            code=180,
            rom=None,
            var=GSW(0, 112),
            item=I.CHAPTER_3_3_KEY,
            region=R.TA206,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 3-3
    (
        LocationData(
            name=L.C33_CHOMPS_CHEST, code=181, rom=None, var=GSWF(828), item=I.CATCH_CARD_PEACH_2, region=R.TA307
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C33_STAR_BLOCK,
            code=182,
            rom=None,
            var=GSW(0, 117),
            item=I.CHAPTER_3_4_KEY,
            region=R.TA304,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 3-4
    (
        LocationData(
            name=L.C34_CHEST_IN_PIPE_OUTSIDE_OF_CASTLE,
            code=183,
            rom=None,
            var=GSW(0, 121),
            item=I.FORT_KEY,
            region=R.TA402,
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(name=L.C34_FREE_CARRIE, code=184, rom=None, var=GSW(0, 123), item=I.PIXL_CARRIE, region=R.TA412),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C34_RIGHT_FRANCIS_CHAMBER_CHEST, code=185, rom=None, var=GSWF(812), item=I.FORT_KEY, region=R.TA411
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C34_LEFT_FRANCIS_CHAMBER_CHEST, code=186, rom=None, var=GSWF(811), item=I.FORT_KEY, region=R.TA410
        ),
        CFG_RANDOM,
    ),
    (
        LocationData(
            name=L.C34_GREEN_PURE_HEART,
            code=187,
            rom=None,
            var=GSW(0, 125),
            item=I.GREEN_PURE_HEART,
            region=R.TA413,
            tag="ph",
        ),
        CFG_LOCKED,
    ),
    # endregion
    # region 4-1
    # (LocationData(name=L.C41_SQUIRPS
    # , code=188
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C41_OPEN_ITEM_BEHIND_ASTEROID_1
    # , code=189
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C41_OPEN_ITEM_BEHIND_ASTEROID_2
    # , code=190
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C41_STAR_BLOCK
    # , code=191
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 4-2
    # (LocationData(name=L.C42_FLIP_THE_DIMENSIONAL_RIFT
    # , code=192
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C42_OPEN_ITEM_IN_CHASM_3_D
    # , code=193
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C42_OPEN_ITEM_BEHIND_PIPE_NEAR_BLAPPYS_HOUSE
    # , code=194
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C42_TALK_TO_BLAPPY
    # , code=195
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C42_FLEEP
    # , code=196
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C42_STAR_BLOCK
    # , code=197
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 4-3
    # (LocationData(name=L.C43_OPEN_ITEM_BEHIND_FIRST_BLOCKS
    # , code=198
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C43_OPEN_ITEM_BEHIND_BLOCKS_IN_MANY_WORMHOLE_ROOM
    # , code=199
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C43_VISIBLE_OPEN_ITEM_IN_BLOCKS
    # , code=200
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C43_STAR_BLOCK
    # , code=201
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 4-4
    # (LocationData(name=L.C44_CHEST_NEAR_BARRIBAD
    # , code=202
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C44_CHEST_ABOVE_LOCKED_DOOR
    # , code=203
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C44_CHEST_IN_3_BLOCK_ROOM
    # , code=204
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C44_CYAN_PURE_HEART
    # , code=205
    # , rom=None
    # , var=None
    # , item=I.CYAN_PURE_HEART
    # , region=None
    # , tag="ph"
    # ), CFG_RANDOM),
    # endregion
    # region 5-1
    # (LocationData(name=L.C51_CHEST_NEAR_WHACKA
    # , code=206
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C51_CHEST_AFTER_SHLORPS
    # , code=207
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C51_CHEST_IN_CHASM_3_D
    # , code=208
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C51_STAR_BLOCK
    # , code=209
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 5-2
    # (LocationData(name=L.C52_FIRE_TABLET
    # , code=210
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C52_OPEN_ITEM_IN_BACKGROUND
    # , code=211
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C52_OPEN_ITEM_IN_FRONT_OF_PIPE
    # , code=212
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C52_STONE_TABLET
    # , code=213
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C52_WATER_TABLET
    # , code=214
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C52_CUDGE
    # , code=215
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C52_CHEST_NEAR_STAR_BLOCK
    # , code=216
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # (LocationData(name=L.C52_STAR_BLOCK
    # , code=217
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 5-3
    # (LocationData(name=L.C53_OPEN_ITEM_IN_CAVE
    # , code=218
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C53_SAVE_CRAGLEY_S_CREW
    # , code=219
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C53_STAR_BLOCK
    # , code=220
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 5-4
    # (LocationData(name=L.C54_DOTTIE
    # , code=221
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C54_OPEN_ITEM_NEAR_PROCESSING_CENTER
    # , code=222
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C54_OPEN_ITEM_BEHIND_PIPE
    # , code=223
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C54_FLIP_THE_SKULL
    # , code=224
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C54_DEFEAT_FLORO_CHUNKS
    # , code=225
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C54_BLUE_PURE_HEART
    # , code=226
    # , rom=None
    # , var=None
    # , item=I.PURPLE_PURE_HEART
    # , region=None
    # , tag="ph"
    # ), CFG_RANDOM),
    # endregion
    # region 6-1
    # (LocationData(name=L.C61_PETRIFIED_PURE_HEART
    # , code=227
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C61_STAR_BLOCK
    # , code=228
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 6-2
    # (LocationData(name=L.C62_STAR_BLOCK
    # , code=229
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 6-3
    # (LocationData(name=L.C63_STAR_BLOCK
    # , code=230
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 6-4
    # (LocationData(name=L.C64_SAMMER_KING_REWARD_1
    # , code=231
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C64_SAMMER_KING_REWARD_2
    # , code=232
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C64_SAMMER_KING_REWARD_3
    # , code=233
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C64_SAMMER_KING_REWARD_4
    # , code=234
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C64_SAMMER_KING_REWARD_5
    # , code=235
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C64_SAMMER_KING_REWARD_6
    # , code=236
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C64_SAMMER_KING_REWARD_7
    # , code=237
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C64_STAR_BLOCK
    # , code=238
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 7-1
    # (LocationData(name=L.C71_CHEST_AFTER_GIGABYTE
    # , code=239
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C71_OPEN_ITEM_ABOVE_PIPE
    # , code=240
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C71_GIVE_THE_PETRIFIED_PURE_HEART_TO_JAYDES
    # , code=241
    # , rom=None
    # , var=None
    # , item=I.PURPLE_PURE_HEART
    # , region=None
    # , tag="ph"
    # ), CFG_RANDOM),
    # (LocationData(name=L.C71_LUIGI
    # , code=242
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C71_HIDDEN_OPEN_ITEM_NEAR_LUIGI
    # , code=243
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C71_HIDDEN_CHEST_IN_LUIGI_S_ROOM
    # , code=244
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C71_STAR_BLOCK
    # , code=245
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 7-2
    # (LocationData(name=L.C72_CHEST_IN_FIRST_DARK_ROOM
    # , code=246
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C72_DEFEAT_BOWSER
    # , code=247
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C72_TALK_TO_HAGRA_AND_GET_THE_BOOK_FROM_THE_D_MAN
    # , code=248
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C72_BRING_THE_DIET_BOOK_TO_HAGRA
    # , code=249
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C72_STAR_BLOCK
    # , code=250
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 7-3
    # (LocationData(name=L.C73_CHEST_RIGHT_OF_25
    # , code=251
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_CHEST_AT_34
    # , code=252
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_CHEST_LEFT_OF_47
    # , code=253
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_WAKE_PEACH_UP
    # , code=254
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_CHEST_AT_68
    # , code=255
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_CHEST_RIGHT_OF_69
    # , code=256
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_CHEST_RIGHT_OF_CYRRUS
    # , code=257
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_CHEST_ATOP_BUILDING_AT_80
    # , code=258
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C73_CHEST_BEHIND_STAR_BLOCK
    # , code=259
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # (LocationData(name=L.C73_STAR_BLOCK
    # , code=260
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # , tag=TAG_STAR_BLOCK
    # ), CFG_DISABLED),
    # endregion
    # region 7-4
    # (LocationData(name=L.C74_SAVE_SUNBI
    # , code=261
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_CHEST_AFTER_GIGABYTE
    # , code=262
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_FREE_WHIBBI
    # , code=263
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_TALK_TO_YEBBI
    # , code=264
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_OPEN_ITEM_ABOVE_TWO_DOORS
    # , code=265
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_TALK_TO_REBBI
    # , code=266
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_BIG_CHEST_BELOW_REBBI
    # , code=267
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_TALK_TO_BLUBI_AFTER_WHIBBI
    # , code=268
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_CHEST_BEHIND_STAIRS
    # , code=269
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_CHEST_FAR_RIGHT_OF_MELEE
    # , code=270
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C74_WHITE_PURE_HEART
    # , code=271
    # , rom=None
    # , var=None
    # , item=I.WHITE_PURE_HEART
    # , region=None
    # , tag="ph"
    # ), CFG_RANDOM),
    # endregion
    # region 8-1
    # (LocationData(name=L.C81_RIGHT_CHEST_ABOVE_PEACH_CUTSCENE_START
    # , code=272
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C81_LEFT_CHEST_ABOVE_PEACH_CUTSCENE_START
    # , code=273
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C81_CHEST_IN_SOOPA_STRIKER_HALLWAY
    # , code=274
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    (
        LocationData(
            name=L.CHAPTER_8_1_END,
            code=275,
            rom=None,
            var=None,
            item=I.CHAPTER_8_2_KEY,
            region=R.LS101,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 8-2
    # (LocationData(name=L.C82_LEFT_CHEST_ABOVE_MERLON_ROOM
    # , code=276
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_MIDDLE_CHEST_ABOVE_MERLON_ROOM
    # , code=277
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_RIGHT_CHEST_ABOVE_MERLON_ROOM
    # , code=278
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_OPEN_ITEM_BEHIND_5TH_PIPE
    # , code=279
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_CHEST_IN_CURSYA_ROOM
    # , code=280
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_FIRST_HUNG_ITEM
    # , code=281
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_SECOND_HUNG_ITEM
    # , code=282
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_THIRD_HUNG_ITEM
    # , code=283
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_DEFEAT_THE_CHROMEBA
    # , code=284
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C82_MERLEES_THUNDER_RAGE
    # , code=285
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    (
        LocationData(
            name=L.CHAPTER_8_2_END,
            code=286,
            rom=None,
            var=None,
            item=I.CHAPTER_8_3_KEY,
            region=R.LS201,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 8-3
    # (LocationData(name=L.C83_RIGHT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS
    # , code=287
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C83_LEFT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS
    # , code=288
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C83_CHEST_AFTER_BLOCK_PUZZLE
    # , code=289
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C83_RIGHT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS
    # , code=290
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C83_LEFT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS
    # , code=291
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    (
        LocationData(
            name=L.CHAPTER_8_3_END,
            code=292,
            rom=None,
            var=None,
            item=I.CHAPTER_8_4_KEY,
            region=R.LS301,
            tag=TAG_STAR_BLOCK,
        ),
        CFG_DISABLED,
    ),
    # endregion
    # region 8-4
    # (LocationData(name=L.C84_CHEST_AFTER_TINY_PASSAGE
    # , code=293
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C84_CHEST_IN_FIRST_3_D_HALLWAYS
    # , code=294
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C84_CHEST_IN_SECOND_3_D_HALLWAYS
    # , code=295
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    # (LocationData(name=L.C84_CHEST_IN_THIRD_3_D_HALLWAYS
    # , code=296
    # , rom=None
    # , var=None
    # , item=None
    # , region=None
    # ), CFG_RANDOM),
    (
        LocationData(name=L.CHAPTER_8_4_END, code=297, rom=None, var=GSW(0, 416), item=E.VICTORY, region=R.LS401),
        CFG_EVENT,
    ),
    # endregion
    # region Flamm / Treasure Maps
    # MOD=Consider changing Flamm's shop to sell all items for x number of coins, 20?
    (
        LocationData(
            name=L.FLAMM_ITEM_1, code=298, rom=None, var=None, item=I.MAP_1, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_2, code=299, rom=None, var=None, item=I.MAP_2, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_3, code=300, rom=None, var=None, item=I.MAP_3, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_4, code=301, rom=None, var=None, item=I.MAP_4, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_5, code=302, rom=None, var=None, item=I.MAP_5, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_6, code=303, rom=None, var=None, item=I.MAP_6, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_7, code=304, rom=None, var=None, item=I.MAP_7, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_8, code=305, rom=None, var=None, item=I.MAP_8, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_9, code=306, rom=None, var=None, item=I.MAP_9, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_10, code=307, rom=None, var=None, item=I.MAP_10, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_11, code=308, rom=None, var=None, item=I.MAP_11, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_12, code=309, rom=None, var=None, item=I.MAP_12, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_13, code=310, rom=None, var=None, item=I.MAP_13, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_14, code=311, rom=None, var=None, item=I.MAP_14, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_15, code=312, rom=None, var=None, item=I.MAP_15, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_16, code=313, rom=None, var=None, item=I.MAP_16, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLAMM_ITEM_17, code=314, rom=None, var=None, item=I.MAP_17, region=R.MAC14_LEFT, tag=TAG_FLAMM
        ),
        CFG_DISABLED,
    ),
    # (LocationData(name=L.FLAMM_ITEM_18
    # , code=315
    # , rom=None
    # , var=None
    # , item=I.MAP_18
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_19
    # , code=316
    # , rom=None
    # , var=None
    # , item=I.MAP_19
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_20
    # , code=317
    # , rom=None
    # , var=None
    # , item=I.MAP_20
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_21
    # , code=318
    # , rom=None
    # , var=None
    # , item=I.MAP_21
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_22
    # , code=319
    # , rom=None
    # , var=None
    # , item=I.MAP_22
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_23
    # , code=320
    # , rom=None
    # , var=None
    # , item=I.MAP_23
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_24
    # , code=321
    # , rom=None
    # , var=None
    # , item=I.MAP_24
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_25
    # , code=322
    # , rom=None
    # , var=None
    # , item=I.MAP_25
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_26
    # , code=323
    # , rom=None
    # , var=None
    # , item=I.MAP_26
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_27
    # , code=324
    # , rom=None
    # , var=None
    # , item=I.MAP_27
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_28
    # , code=325
    # , rom=None
    # , var=None
    # , item=I.MAP_28
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_29
    # , code=326
    # , rom=None
    # , var=None
    # , item=I.MAP_29
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_30
    # , code=327
    # , rom=None
    # , var=None
    # , item=I.MAP_30
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_31
    # , code=328
    # , rom=None
    # , var=None
    # , item=I.MAP_31
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_32
    # , code=329
    # , rom=None
    # , var=None
    # , item=I.MAP_32
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_33
    # , code=330
    # , rom=None
    # , var=None
    # , item=I.MAP_33
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_34
    # , code=331
    # , rom=None
    # , var=None
    # , item=I.MAP_34
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_35
    # , code=332
    # , rom=None
    # , var=None
    # , item=I.MAP_35
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_36
    # , code=333
    # , rom=None
    # , var=None
    # , item=I.MAP_36
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_37
    # , code=334
    # , rom=None
    # , var=None
    # , item=I.MAP_37
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_38
    # , code=335
    # , rom=None
    # , var=None
    # , item=I.MAP_38
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_39
    # , code=336
    # , rom=None
    # , var=None
    # , item=I.MAP_39
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_40
    # , code=337
    # , rom=None
    # , var=None
    # , item=I.MAP_40
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_41
    # , code=338
    # , rom=None
    # , var=None
    # , item=I.MAP_41
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_42
    # , code=339
    # , rom=None
    # , var=None
    # , item=I.MAP_42
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_43
    # , code=340
    # , rom=None
    # , var=None
    # , item=I.MAP_43
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_44
    # , code=341
    # , rom=None
    # , var=None
    # , item=I.MAP_44
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_45
    # , code=342
    # , rom=None
    # , var=None
    # , item=I.MAP_45
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_46
    # , code=343
    # , rom=None
    # , var=None
    # , item=I.MAP_46
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_47
    # , code=344
    # , rom=None
    # , var=None
    # , item=I.MAP_47
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLAMM_ITEM_48
    # , code=345
    # , rom=None
    # , var=None
    # , item=I.MAP_48
    # , region=R.MAC14_LEFT
    # , tag=TAG_FLAMM
    # ), CFG_DISABLED),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_01,
            code=346,
            rom=None,
            var=None,
            item=I.GOLD_BAR,
            region=R.MAC01_LAYER1,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_02,
            code=347,
            rom=None,
            var=None,
            item=I.CATCH_CARD_WELDERBERG,
            region=R.MAC03_LAYER1,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_03,
            code=348,
            rom=None,
            var=None,
            item=I.ULTRA_SHROOM_SHAKE,
            region=R.MAC04_LAYER1,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_04,
            code=349,
            rom=None,
            var=None,
            item=I.CATCH_CARD_KING_SAMMER,
            region=R.MAC30,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_05,
            code=350,
            rom=None,
            var=None,
            item=I.CATCH_CARD_O_CHUNKS,
            region=R.MAC11_LAYER1,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_06,
            code=351,
            rom=None,
            var=None,
            item=I.CATCH_CARD_BESTOVIUS,
            region=R.HE101,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_07,
            code=352,
            rom=None,
            var=None,
            item=I.GOLDEN_LEAF,
            region=R.HE201,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_08,
            code=353,
            rom=None,
            var=None,
            item=I.CATCH_CARD_BROBOT_L_TYPE,
            region=R.HE205,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_09,
            code=354,
            rom=None,
            var=None,
            item=I.GOLD_BAR_X3,
            region=R.HE302,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_10,
            code=355,
            rom=None,
            var=None,
            item=I.CATCH_CARD_FRACKTAIL,
            region=R.HE307,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_11,
            code=356,
            rom=None,
            var=None,
            item=I.CATCH_CARD_MERLUMINA,
            region=R.HE411,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_12,
            code=357,
            rom=None,
            var=None,
            item=I.SHOOTING_STAR,
            region=R.MI104,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_13,
            code=358,
            rom=None,
            var=None,
            item=I.CATCH_CARD_SP,
            region=R.MI201,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_14,
            code=359,
            rom=None,
            var=None,
            item=I.CATCH_CARD_GNIP,
            region=R.MI203,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_15,
            code=360,
            rom=None,
            var=None,
            item=I.CATCH_CARD_MIMI,
            region=R.MI306,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_16,
            code=361,
            rom=None,
            var=None,
            item=I.GOLD_BAR_X3,
            region=R.MI401,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    (
        LocationData(
            name=L.FLEEP_MAP_REVEAL_17,
            code=362,
            rom=None,
            var=None,
            item=I.DRIED_SHROOM,
            region=R.MI414,
            tag=TAG_TREASURE,
        ),
        CFG_DISABLED,
    ),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_18
    # , code=363
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_BACK_CURSYA
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_19
    # , code=364
    # , rom=None
    # , var=None
    # , item=I.ULTRA_SHROOM_SHAKE
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_20
    # , code=365
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_BIG_BLOOPER
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_21
    # , code=366
    # , rom=None
    # , var=None
    # , item=I.POWER_PLUS
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_22
    # , code=367
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_DIMENTIO
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_23
    # , code=368
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_TIPTRON
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_24
    # , code=369
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_FRANCIS
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_25
    # , code=370
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_SQUIRPS
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_26
    # , code=371
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_HOOLIGON
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_27
    # , code=372
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_MR_L
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_28
    # , code=373
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_BROBOT
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_29
    # , code=374
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_MUTH
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_30
    # , code=375
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_FLINT_CRAGLEY
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_31
    # , code=376
    # , rom=None
    # , var=None
    # , item=I.FIRE_BURST
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_32
    # , code=377
    # , rom=None
    # , var=None
    # , item=I.FIRE_BURST
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_33
    # , code=378
    # , rom=None
    # , var=None
    # , item=I.ULTRA_SHROOM_SHAKE
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_34
    # , code=379
    # , rom=None
    # , var=None
    # , item=I.SHOOTING_STAR
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_35
    # , code=380
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_HORNFELS_MONZO
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_36
    # , code=381
    # , rom=None
    # , var=None
    # , item=I.POISON_SHROOM
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_37
    # , code=382
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_KING_CROACUS
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_38
    # , code=383
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_JAYDES
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_39
    # , code=384
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_UNDERHAND
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_40
    # , code=385
    # , rom=None
    # , var=None
    # , item=I.TRIAL_STEW
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_41
    # , code=386
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_THE_UNDERCHOMP
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_42
    # , code=387
    # , rom=None
    # , var=None
    # , item=I.GOLD_BAR_X3
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_43
    # , code=388
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_GRAMBI
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_44
    # , code=389
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_LUVBI
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_45
    # , code=390
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_BONECHILL
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_46
    # , code=391
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_NASTASIA
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_47
    # , code=392
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_SUPER_DIMENTIO
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # (LocationData(name=L.FLEEP_MAP_REVEAL_48
    # , code=393
    # , rom=None
    # , var=None
    # , item=I.CATCH_CARD_COUNT_BLECK
    # , region=None
    # , tag=TAG_TREASURE
    # ), CFG_DISABLED),
    # endregion
]


BASE_LOCATION_ID = 4_998_000

LOCATION_ENUM_TO_SETUP = {
    data.name: data for (data, _) in LOCATION_SETUP if data.code is not None and data.region is not None
}
LOCATION_NAME_TO_ID = {name.value: data.code + BASE_LOCATION_ID for name, data in LOCATION_ENUM_TO_SETUP.items()}
LOCATION_GROUPS = {group for (loc, _) in LOCATION_SETUP for group in loc.groups}
LOCATION_GROUP_MAP = {
    group: {loc.name.value for (loc, _) in LOCATION_SETUP if group in loc.groups and loc.region is not None}
    for group in LOCATION_GROUPS
}
