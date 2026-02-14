from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ..flags import GSW, GSWF, ScriptVariable
from ..names.event_names import EventName as E
from ..names.item_names import ItemName as I
from ..names.location_names import LocationName as L
from ..names.region_names import RegionName as R
from ..options import PitAccess, SuperPaperMarioOptions
from . import RandomizationType as RT


@dataclass
class LocationData:
    name: L
    code: int
    """A unique id among all other SPM locations. Gets added to BASE_LOCATION_ID."""
    rom: int
    """Where do we write the randomized item to to change what gets picked up?"""
    var: ScriptVariable
    """Which game variable is set when this location is checked?
    https://github.com/SeekyCt/spm-docs/wiki/GSWF"""
    item: I
    """What item is normally at this location. Mostly just used for events, maybe to be used for multislot setting"""
    region: R
    """What region does this location belong to"""
    setting: Callable[[SuperPaperMarioOptions], RT] | RT = RT.RANDOM
    """How is this location randomized?"""
    groups: frozenset[str] = frozenset()
    """What location groups does this belong to"""

# convenience strings bc I hate putting quotes everywhere in dicts
name = "name"
code = "code"
rom = "rom"
var = "var"
item = "item"
region = "region"
setting = "setting"
groups = "groups"


# Groups
GROUP_FLIPSIDE_PIT = "Flipside Pit"
GROUP_FLOPSIDE_PIT = "Flopside Pit"
GROUP_PIT = "Pit"
GROUP_SHOP = "Shop"

# Randomization settings
def heart_pillar(opt: SuperPaperMarioOptions) -> RT:
    return RT.RANDOM


def pure_heart(opt: SuperPaperMarioOptions) -> RT:
    return RT.RANDOM if opt.shuffle_pure_hearts else RT.VANILLA_WORLD


def shop(opt: SuperPaperMarioOptions) -> RT:
    return RT.RANDOM


def fetch(opt: SuperPaperMarioOptions) -> RT:
    return RT.RANDOM


def flipside_pit(opt: SuperPaperMarioOptions) -> RT:
    return RT.DISABLED if opt.flipside_pit_access == PitAccess.option_closed else RT.RANDOM


def flopside_pit(opt: SuperPaperMarioOptions) -> RT:
    return RT.DISABLED if opt.flopside_pit_access == PitAccess.option_closed else RT.RANDOM

###
# WARNING: ALL LOCATION IDS STILL SUBJECT TO CHANGE, DO NOT REFERENCE THESE
###
LOCATION_LIST_DICT: list[dict[str, Any]] = [
    #region Heart Pillars
    { name: L.FLIPSIDE_HEART_PILLAR_RED
    , code: 1
    , rom: 0
    , var: GSW(0, 8)
    , item: I.CHAPTER_1_1_KEY
    , region: R.MAC01_LAYER1
    , setting: heart_pillar
    },
    { name: L.FLIPSIDE_HEART_PILLAR_ORANGE
    , code: 2
    , rom: 0
    , var: GSW(0, 65)
    , item: I.CHAPTER_2_1_KEY
    , region: R.MAC06_LAYER2
    , setting: heart_pillar
    },
    { name: L.FLIPSIDE_HEART_PILLAR_YELLOW
    , code: 3
    , rom: 0
    , var: GSW(0, 100)
    , item: I.CHAPTER_3_1_KEY
    , region: R.MAC07_LAYER2
    , setting: heart_pillar
    },
    { name: L.FLIPSIDE_HEART_PILLAR_GREEN
    , code: 4
    , rom: 0
    , var: GSW(0, 128)
    , item: I.CHAPTER_4_1_KEY
    , region: R.MAC02_LAYER3
    , setting: heart_pillar
    },
    { name: L.FLOPSIDE_HEART_PILLAR_CYAN
    , code: 5
    , rom: 0
    , var: GSW(0, 177)
    , item: I.CHAPTER_5_1_KEY
    , region: R.MAC11_LAYER1
    , setting: heart_pillar
    },
    { name: L.FLOPSIDE_HEART_PILLAR_BLUE
    , code: 6
    , rom: 0
    , var: GSW(0, 224)
    , item: I.CHAPTER_6_1_KEY
    , region: R.MAC16_LAYER2
    , setting: heart_pillar
    },
    { name: L.FLOPSIDE_HEART_PILLAR_PURPLE
    , code: 7
    , rom: 0
    , var: GSW(0, 303)
    , item: I.CHAPTER_7_1_KEY
    , region: R.MAC17_LAYER2
    , setting: heart_pillar
    },
    { name: L.FLOPSIDE_HEART_PILLAR_WHITE
    , code: 8
    , rom: 0
    , var: GSW(0, 356)
    , item: I.CHAPTER_8_1_KEY
    , region: R.MAC12_LAYER3
    , setting: heart_pillar
    },
    #endregion
    #region Shop Locations
    #I don't know if the vanilla items are listed in the correct order
    # MOD: What script variable or otherwise can be used to keep track of shop purcheses?
    { name: L.FLIPSIDE_HOWZITS_1
    , code: 9
    , rom: 0
    , var: None
    , item: I.SHROOM_SHAKE
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_2
    , code: 10
    , rom: 0
    , var: None
    , item: I.LONG_LAST_SHAKE
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_3
    , code: 11
    , rom: 0
    , var: None
    , item: I.LIFE_SHROOM
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_4
    , code: 12
    , rom: 0
    , var: None
    , item: I.FIRE_BURST
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_5
    , code: 13
    , rom: 0
    , var: None
    , item: I.ICE_STORM
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_6
    , code: 14
    , rom: 0
    , var: None
    , item: I.SLEEPY_SHEEP
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_7
    , code: 15
    , rom: 0
    , var: None
    , item: I.COURAGE_SHELL
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_8
    , code: 16
    , rom: 0
    , var: None
    , item: I.SHELL_SHOCK
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_9
    , code: 17
    , rom: 0
    , var: None
    , item: I.STAR_MEDAL
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_HOWZITS_10
    , code: 18
    , rom: 0
    , var: None
    , item: I.GOLD_BAR
    , region: R.MAC02_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_ITTY_BITS_1
    , code: 19
    , rom: 0
    , var: None
    , item: I.HONEY_JAR
    , region: R.MAC04_ITTY_BITS
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_ITTY_BITS_2
    , code: 20
    , rom: 0
    , var: None
    , item: I.BIG_EGG
    , region: R.MAC04_ITTY_BITS
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLIPSIDE_ITTY_BITS_3
    , code: 21
    , rom: 0
    , var: None
    , item: I.CAKE_MIX
    , region: R.MAC04_ITTY_BITS
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_1
    , code: 22
    , rom: 0
    , var: None
    , item: I.VOLT_SHROOM
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_2
    , code: 23
    , rom: 0
    , var: None
    , item: I.BLOCK_BLOCK
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_3
    , code: 24
    , rom: 0
    , var: None
    , item: I.STOP_WATCH
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_4
    , code: 25
    , rom: 0
    , var: None
    , item: I.MIGHTY_TONIC
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_5
    , code: 26
    , rom: 0
    , var: None
    , item: I.SUPER_SHROOM_SHAKE
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_6
    , code: 27
    , rom: 0
    , var: None
    , item: I.THUNDER_RAGE
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_7
    , code: 28
    , rom: 0
    , var: None
    , item: I.GHOST_SHROOM
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_8
    , code: 29
    , rom: 0
    , var: None
    , item: I.ULTRA_SHROOM_SHAKE
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_9
    , code: 30
    , rom: 0
    , var: None
    , item: I.GOLD_BAR_X3
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_NOTSOS_10
    , code: 31
    , rom: 0
    , var: None
    , item: I.GOLD_MEDAL
    , region: R.MAC12_LAYER1
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_ITTY_BITS_1
    , code: 32
    , rom: 0
    , var: None
    , item: I.FRESH_PASTA_BUNCH
    , region: R.MAC14_L_ITTY_BITS
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_ITTY_BITS_2
    , code: 33
    , rom: 0
    , var: None
    , item: I.POWER_STEAK
    , region: R.MAC14_L_ITTY_BITS
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.FLOPSIDE_ITTY_BITS_3
    , code: 34
    , rom: 0
    , var: None
    , item: I.SMELLY_HERB
    , region: R.MAC14_L_ITTY_BITS
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_1
    , code: 35
    , rom: 0
    , var: None
    , item: I.FIRE_BURST
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_2
    , code: 36
    , rom: 0
    , var: None
    , item: I.POW_BLOCK
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_3
    , code: 37
    , rom: 0
    , var: None
    , item: I.SHROOM_SHAKE
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_4
    , code: 38
    , rom: 0
    , var: None
    , item: I.LONG_LAST_SHAKE
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_5
    , code: 39
    , rom: 0
    , var: None
    , item: I.LIFE_SHROOM
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_6
    , code: 40
    , rom: 0
    , var: None
    , item: I.SLEEPY_SHEEP
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_7
    , code: 41
    , rom: 0
    , var: None
    , item: I.SHELL_SHOCK
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_8
    , code: 42
    , rom: 0
    , var: None
    , item: I.MIGHTY_TONIC
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_9
    , code: 43
    , rom: 0
    , var: None
    , item: I.COURAGE_SHELL
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.YOLD_TOWN_HOWZITS_10
    , code: 44
    , rom: 0
    , var: None
    , item: I.VOLT_SHROOM
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOTWOOD_TREE_ITTY_BITS_1
    , code: 45
    , rom: 0
    , var: None
    , item: I.FRESH_VEGGIE
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOTWOOD_TREE_ITTY_BITS_2
    , code: 46
    , rom: 0
    , var: None
    , item: I.HORSETAIL
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOTWOOD_TREE_ITTY_BITS_3
    , code: 47
    , rom: 0
    , var: None
    , item: I.PEACHY_PEACH
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.OUTER_LIMITS_HOWZITS_TWINKLE_MART_1
    , code: 48
    , rom: 0
    , var: None
    , item: I.GOLDEN_CHOCO_BAR
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.OUTER_LIMITS_HOWZITS_TWINKLE_MART_2
    , code: 49
    , rom: 0
    , var: None
    , item: I.SHROOM_CHOCO_BAR
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.OUTER_LIMITS_HOWZITS_TWINKLE_MART_3
    , code: 50
    , rom: 0
    , var: None
    , item: I.SWEET_CHOCO_BAR
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_1
    , code: 51
    , rom: 0
    , var: None
    , item: I.COURAGE_SHELL
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_2
    , code: 52
    , rom: 0
    , var: None
    , item: I.FIRE_BURST
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_3
    , code: 53
    , rom: 0
    , var: None
    , item: I.ICE_STORM
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_4
    , code: 54
    , rom: 0
    , var: None
    , item: I.LIFE_SHROOM
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_5
    , code: 55
    , rom: 0
    , var: None
    , item: I.MYSTERY_BOX
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_6
    , code: 56
    , rom: 0
    , var: None
    , item: I.POW_BLOCK
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_7
    , code: 57
    , rom: 0
    , var: None
    , item: I.PRIMORDIAL_FRUIT
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_8
    , code: 58
    , rom: 0
    , var: None
    , item: I.SHROOM_SHAKE
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_9
    , code: 59
    , rom: 0
    , var: None
    , item: I.SLEEPY_SHEEP
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_HOWZITS_10
    , code: 60
    , rom: 0
    , var: None
    , item: I.SUPER_SHROOM_SHAKE
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_ITTY_BITS_1
    , code: 61
    , rom: 0
    , var: None
    , item: I.KEEL_MANGO
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.DOWNTOWN_CRAG_ITTY_BITS_2
    , code: 62
    , rom: 0
    , var: None
    , item: I.MILD_COCOA_BEAN
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.THE_OVERTHERE_ITTY_BITS_1
    , code: 63
    , rom: 0
    , var: None
    , item: I.HOT_DOG
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    { name: L.THE_OVERTHERE_ITTY_BITS_2
    , code: 64
    , rom: 0
    , var: None
    , item: I.HOT_SAUCE
    , region: None
    , setting: shop
    , groups: {GROUP_SHOP}
    },
    #endregion
    #region Flipside
    # { name: L.FLIPSIDE_STARTING_CHARACTER
    # , code: 65
    # , rom: None
    # , var: None
    # , item: I.CHARACTER_MARIO
    # , region: None
    # , setting: RT.VANILLA_EVENT
    # },
    # { name: L.FLIPSIDE_STARTING_PIXL
    # , code: 66
    # , rom: None
    # , var: None
    # , item: I.PIXL_TIPPI
    # , region: None
    # , setting: RT.VANILLA_EVENT
    # },
    { name: L.FLIPSIDE_MERLONS_GIFT
    , code: 67
    , rom: None
    , var: None
    , item: I.RED_PURE_HEART
    , region: R.MAC02_L_TOWER
    , setting: pure_heart
    },
    { name: L.FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK
    , code: 68
    , rom: 0
    , var: GSWF(527)
    , item: I.CATCH_CARD_MERLEE
    , region: R.MAC01_LAYER2
    },
    { name: L.FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS
    , code: 69
    , rom: 0
    , var: GSWF(580)
    , item: I.COOKING_DISK_R
    , region: R.MAC01_LAYER2
    },
    { name: L.FLIPSIDE_3F_EAT_A_SPICY_SOUP
    , code: 70
    , rom: 0
    , var: GSW(0, 63)
    , item: I.CHARACTER_PEACH
    , region: R.MAC01_LAYER1
    },
    { name: L.FLIPSIDE_3F_FISHBOWL
    , code: 71
    , rom: 0
    , var: GSW(0, 133)
    , item: I.GOLDFISH_BOWL_FISH
    , region: R.MAC01_LAYER1
    },
    { name: L.FLIPSIDE_1F_OUTSKIRTS_LEFT_CHEST_IN_HOLE
    , code: 72
    , rom: 0
    , var: GSWF(523)
    , item: I.CATCH_CARD_MERLON
    , region: R.MAC08
    },
    { name: L.FLIPSIDE_1F_OUTSKIRTS_RIGHT_CHEST_IN_HOLE
    , code: 73
    , rom: 0
    , var: GSWF(522)
    , item: I.CATCH_CARD_MERLUVLEE
    , region: R.MAC08
    },
    { name: L.FLIPSIDE_B1_3D_CHEST
    , code: 74
    , rom: 0
    , var: GSWF(520)
    , item: I.CATCH_CARD_THE_INTER_NED
    , region: R.MAC04_LAYER1
    },
    { name: L.FLIPSIDE_B1_OUTSKIRTS_CHEST_BEHIND_PILLAR
    , code: 75
    , rom: 0
    , var: GSWF(521)
    , item: I.CATCH_CARD_THE_INTER_CHET
    , region: R.MAC07_LAYER1
    },
    { name: L.FLIPSIDE_B1_FREE_FISH
    , code: 76
    , rom: 0
    , var: GSW(0, 134)
    , item: I.GOLDFISH_BOWL_EMPTY
    , region: None
    },
    { name: L.FLIPSIDE_B2_CHEST_AFTER_PIPE
    , code: 77
    , rom: 0
    , var: GSWF(503)
    , item: I.HP_PLUS
    , region: R.MAC05_LAYER2
    },
    #endregion
    #region Flopside
    { name: L.FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK
    , code: 78
    , rom: 0
    , var: GSWF(529)
    , item: I.CATCH_CARD_NOLREM
    , region: R.MAC11_LAYER2
    },
    { name: L.FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS
    , code: 79
    , rom: 0
    , var: GSWF(581)
    , item: I.COOKING_DISK_W
    , region: R.MAC11_LAYER2
    },
    { name: E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK
    , code: 80
    , rom: 0
    , var: None
    , item: E.SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK
    , region: R.MAC15_LAYER2
    , setting: RT.VANILLA_EVENT
    },
    { name: L.FLOPSIDE_B2_CHEST_AFTER_PIPE
    , code: 80
    , rom: 0
    , var: GSWF(506)
    , item: I.POWER_PLUS
    , region: R.MAC15_LAYER2
    },
    { name: E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK
    , code: 80
    , rom: None
    , var: None
    , item: E.SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK
    , region: R.MAC17_LAYER2
    , setting: RT.VANILLA_EVENT
    },
    { name: L.FLOPSIDE_B2_CHASM_CHEST
    , code: 81
    , rom: 0
    , var: GSWF(525)
    , item: I.CATCH_CARD_BARRY
    , region: R.MAC18
    },
    { name: L.FLOPSIDE_B1_BEVERAGARIUM_CHEST1
    , code: 82
    , rom: 0
    , var: GSWF(537)
    , item: I.GOLDEN_CARD
    , region: None
    },
    { name: L.FLOPSIDE_B1_BEVERAGARIUM_CHEST2
    , code: 83
    , rom: 0
    , var: GSWF(583)
    , item: I.COOKING_DISK_B
    , region: None
    },
    { name: L.FLOPSIDE_B1_OUTSKIRT_CHEST_BEHIND_PILLAR
    , code: 84
    , rom: 0
    , var: GSWF(524)
    , item: I.CATCH_CARD_PICCOLO
    , region: R.MAC17_LAYER1
    },
    #endregion
    #region Piccolo's Fetch Quest
    { name: L.PICCOLO_FETCH_WATCHITT_1
    , code: 85
    , rom: 0
    , var: GSWF(413)
    , item: I.PAPER
    , region: None
    , setting: fetch
    },
    { name: L.PICCOLO_FETCH_MERLUMINA
    , code: 86
    , rom: 0
    , var: GSWF(414)
    , item: I.AUTOGRAPH
    , region: None
    , setting: fetch
    },
    { name: L.PICCOLO_FETCH_WATCHITT_2
    , code: 87
    , rom: 0
    , var: GSWF(415)
    , item: I.YOU_KNOW_WHAT
    , region: None
    , setting: fetch
    },
    { name: L.PICCOLO_FETCH_BESTOVIUS
    , code: 88
    , rom: 0
    , var: GSWF(416)
    , item: I.TRAINING_MACHINE
    , region: None
    , setting: fetch
    },
    { name: L.PICCOLO_FETCH_MERLUVLEE
    , code: 89
    , rom: 0
    , var: GSWF(417)
    , item: I.CRYSTAL_BALL
    , region: R.MAC02_LAYER1
    , setting: fetch
    },
    { name: L.PICCOLO_FETCH_MERLEE
    , code: 90
    , rom: 0
    , var: GSWF(418)
    , item: I.RANDOM_HOUSE_KEY
    , region: R.MAC12_LAYER1
    , setting: fetch
    },
    { name: L.PICCOLO_FETCH_END
    , code: 91
    , rom: 0
    , var: GSWF(517)
    , item: I.PIXL_PICCOLO
    , region: R.MAC19_LAYER1
    , setting: fetch
    },
    #endregion
    #region Flipside Pit
    { name: E.SWITCH_FLIPSIDE_PIT_CAGE
    , code: 92
    , rom: 0
    , var: GSWF(501)
    , item: E.SWITCH_FLIPSIDE_PIT_CAGE
    , region: R.L_FLIPSIDE_PIT_ENTRANCE
    , setting: RT.VANILLA_EVENT
    },
    { name: L.FLIPSIDE_PIT_10
    , code: 92
    , rom: 0
    , var: GSWF(433)
    , item: I.CATCH_CARD_TIPPI
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_20
    , code: 93
    , rom: 0
    , var: GSWF(434)
    , item: I.CATCH_CARD_THOREAU
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_30
    , code: 94
    , rom: 0
    , var: GSWF(435)
    , item: I.CATCH_CARD_BOOMER
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_40
    , code: 95
    , rom: 0
    , var: GSWF(436)
    , item: I.CATCH_CARD_SLIM
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_50
    , code: 96
    , rom: 0
    , var: GSWF(437)
    , item: I.CATCH_CARD_THUDLEY
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_60
    , code: 97
    , rom: 0
    , var: GSWF(438)
    , item: I.CATCH_CARD_CARRIE
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_70
    , code: 98
    , rom: 0
    , var: GSWF(439)
    , item: I.CATCH_CARD_FLEEP
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_80
    , code: 99
    , rom: 0
    , var: GSWF(440)
    , item: I.CATCH_CARD_CUDGE
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_90
    , code: 100
    , rom: 0
    , var: GSWF(441)
    , item: I.CATCH_CARD_DOTTIE
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_100
    , code: 101
    , rom: 0
    , var: GSWF(389) # 2 flags for wracktail? 389/409
    , item: I.PIXL_DASHELL
    , region: R.L_FLIPSIDE_PIT
    , setting: flipside_pit
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLIPSIDE_PIT_WRACKTAIL
    , code: None
    , rom: 0
    , var: GSWF(408)
    , item: E.COMPLETED_FLIPSIDE_PIT
    , region: R.L_FLIPSIDE_PIT
    , setting: RT.VANILLA_EVENT
    , groups: {GROUP_FLIPSIDE_PIT, GROUP_PIT}
    },
    #endregion
    #region Flopside Pit
    { name: L.FLOPSIDE_PIT_10
    , code: 102
    , rom: 0
    , var: GSWF(442)
    , item: I.CATCH_CARD_DASHELL
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_20
    , code: 103
    , rom: 0
    , var: GSWF(443)
    , item: I.CATCH_CARD_GOOMBARIO
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_30
    , code: 104
    , rom: 0
    , var: GSWF(444)
    , item: I.CATCH_CARD_KOOPER
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_40
    , code: 105
    , rom: 0
    , var: GSWF(445)
    , item: I.CATCH_CARD_BOMBETTE
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_50
    , code: 106
    , rom: 0
    , var: GSWF(446)
    , item: I.CATCH_CARD_PARAKARRY
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_60
    , code: 107
    , rom: 0
    , var: GSWF(447)
    , item: I.CATCH_CARD_BOW
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_70
    , code: 108
    , rom: 0
    , var: GSWF(448)
    , item: I.CATCH_CARD_WATT
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_80
    , code: 109
    , rom: 0
    , var: GSWF(449)
    , item: I.CATCH_CARD_SUSHIE
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_90
    , code: 110
    , rom: 0
    , var: GSWF(450)
    , item: I.CATCH_CARD_LAKILESTER
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_1
    , code: 111
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_MARIO
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_2
    , code: 112
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_DARK_MARIO
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_3
    , code: 113
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_PEACH_1
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_4
    , code: 114
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_DARK_PEACH
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_5
    , code: 115
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_BOWSER_1
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_6
    , code: 116
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_DARK_BOWSER
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_7
    , code: 117
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_LUIGI
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_100_8
    , code: 118
    , rom: 0
    , var: None
    , item: I.CATCH_CARD_DARK_LUIGI
    , region: R.L_FLOPSIDE_PIT
    , setting: flopside_pit
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    { name: L.FLOPSIDE_PIT_SHADOO
    , code: None
    , rom: 0
    , var: None
    , item: E.COMPLETED_FLOPSIDE_PIT
    , region: R.L_FLOPSIDE_PIT
    , setting: RT.VANILLA_EVENT
    , groups: {GROUP_FLOPSIDE_PIT, GROUP_PIT}
    },
    #endregion
    #region 1-1
    # { name: L.C11_OPEN_ITEM_BEHIND_PIPE
    # , code: 119
    # , rom: 0
    # , var: GSWF(603)
    # , item: I.CATCH_CARD_GOOMBA
    # , region: R.HE102
    # },
    # { name: L.C11_CHEST_AFTER_STAR_BLOCK
    # , code: 120
    # , rom: 0
    # , var: GSWF(604)
    # , item: I.CATCH_CARD_KOOPA_TROOPA
    # , region: R.HE105
    # },
    # { name: L.C11_OPEN_ITEM_ABOVE_BESTOVIUS_HOUSE
    # , code: 121
    # , rom: 0
    # , var: GSWF(611)
    # , item: I.CATCH_CARD_SQUIGLET
    # , region: R.HE101
    # },
    # { name: L.C11_CHEST_INSIDE_FIRST_PIPE
    # , code: 122
    # , rom: 0
    # , var: GSWF(612)
    # , item: I.SHROOM_SHAKE
    # , region: R.HE103
    # },
    # { name: L.C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM
    # , code: 123
    # , rom: 0
    # , var: GSWF(614)
    # , item: I.SHELL_SHOCK
    # , region: R.HE106
    # },
    # { name: L.C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY
    # , code: 124
    # , rom: 0
    # , var: GSWF(615)
    # , item: I.FIRE_BURST
    # , region: R.HE101
    # },
    # { name: L.C11_TALK_TO_BESTOVIUS
    # , code: 125
    # , rom: 0
    # , var: GSW(0, 16)
    # , item: I.ABILITY_FLIP
    # , region: R.HE106
    # },
    # { name: L.C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM
    # , code: 126
    # , rom: 0
    # , var: GSWF(616)
    # , item: I.SHROOM_SHAKE
    # , region: R.HE106
    # },
    # { name: L.C11_STAR_BLOCK
    # , code: 127
    # , rom: 0
    # , var: GSW(0, 17)
    # , item: I.CHAPTER_1_2_KEY
    # , region: R.HE105
    # },
    # #endregion
    # #region 1-2
    # { name: L.C12_THOREAU_CHEST
    # , code: 128
    # , rom: 0
    # , var: GSW(0, 25)
    # , item: I.PIXL_THOREAU
    # , region: R.HE207
    # },
    # { name: L.C12_CHEST_IN_SHORTCUT
    # , code: 129
    # , rom: 0
    # , var: GSWF(605)
    # , item: I.CATCH_CARD_PARATROOPA
    # , region: R.HE201
    # },
    # { name: L.C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE
    # , code: 130
    # , rom: 0
    # , var: GSWF(610)
    # , item: I.CATCH_CARD_BOOMBOXER
    # , region: R.HE203
    # },
    # { name: L.C12_OPEN_ITEM_BEHIND_GREENS_BED
    # , code: 131
    # , rom: 0
    # , var: GSWF(618)
    # , item: I.CATCH_CARD_RED_GREEN
    # , region: R.HE205
    # },
    # { name: L.C12_STAR_BLOCK
    # , code: 132
    # , rom: 0
    # , var: GSW(0, 28)
    # , item: I.CHAPTER_1_3_KEY
    # , region: R.HE203
    # },
    # #endregion
    # #region 1-3
    # { name: L.C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM
    # , code: 133
    # , rom: 0
    # , var: GSWF(606)
    # , item: I.CATCH_CARD_SQUIG
    # , region: R.HE301
    # },
    # { name: L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM
    # , code: 134
    # , rom: 0
    # , var: GSWF(607)
    # , item: I.COURAGE_SHELL
    # , region: R.HE302
    # },
    # { name: L.C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM
    # , code: 135
    # , rom: 0
    # , var: GSWF(608)
    # , item: I.GHOST_SHROOM
    # , region: R.HE306
    # },
    # { name: L.C13_STAR_BLOCK
    # , code: 136
    # , rom: 0
    # , var: GSW(0, 38)
    # , item: I.CHAPTER_1_4_KEY
    # , region: R.HE308
    # },
    # #endregion
    # #region 1-4
    # { name: L.C14_CHEST_IN_SECOND_ROOM
    # , code: 137
    # , rom: 0
    # , var: GSWF(609)
    # , item: I.LIFE_SHROOM
    # , region: R.HE402
    # },
    # { name: L.C14_CHEST_IN_SMALL_SPIKY_TROMP_ROOM
    # , code: 138
    # , rom: 0
    # , var: GSW(0, 40)
    # , item: I.RUINS_KEY
    # , region: R.HE404
    # },
    # { name: L.C14_OPEN_KEY_BEHIND_BLOCKS
    # , code: 139
    # , rom: 0
    # , var: GSW(0, 43)
    # , item: I.RUINS_KEY
    # , region: R.HE405
    # },
    # { name: L.C14_HIDDEN_CHEST_AFTER_3D_PATH
    # , code: 140
    # , rom: 0
    # , var: GSWF(613)
    # , item: I.CATCH_CARD_BUZZY_BEETLE
    # , region: R.HE407
    # },
    # { name: L.C14_OPEN_KEY_BETWEEN_FIRE_BARS
    # , code: 141
    # , rom: 0
    # , var: GSW(0, 46)
    # , item: I.RUINS_KEY
    # , region: R.HE407
    # },
    # { name: L.C14_ORANGE_PURE_HEART
    # , code: 142
    # , rom: 0
    # , var: GSW(0, 53)
    # , item: I.ORANGE_PURE_HEART
    # , region: R.HE411
    # , setting: pure_heart
    # },
    # #endregion
    # #region 2-1
    # { name: L.C21_CHEST_AFTER_SQUIGS
    # , code: 143
    # , rom: 0
    # , var: GSWF(735)
    # , item: I.DOOR_KEY_21
    # , region: R.MI105
    # },
    # { name: L.C21_BOOMER_CHEST
    # , code: 144
    # , rom: 0
    # , var: GSW(0, 73)
    # , item: I.PIXL_BOOMER
    # , region: R.MI107
    # },
    # { name: L.C21_CHEST_BEHIND_BOOMER_CHEST
    # , code: 145
    # , rom: 0
    # , var: GSWF(738)
    # , item: I.CATCH_CARD_OLD_MAN_WATCHITT
    # , region: R.MI107
    # },
    # { name: L.C21_LEFT_CHEST_BEFORE_STAR_BLOCK
    # , code: 146
    # , rom: 0
    # , var: GSWF(732)
    # , item: I.CATCH_CARD_SHLURP
    # , region: R.MI104
    # },
    # { name: L.C21_RIGHT_CHEST_BEFORE_STAR_BLOCK
    # , code: 147
    # , rom: 0
    # , var: GSWF(733)
    # , item: I.CATCH_CARD_SWOOPER
    # , region: R.MI104
    # },
    # { name: L.C21_STAR_BLOCK
    # , code: 148
    # , rom: 0
    # , var: GSW(0, 76)
    # , item: I.CHAPTER_2_2_KEY
    # , region: R.MI104
    # },
    # #endregion
    # # TODO: verify remaining script variables & items
    # #region 2-2
    # { name: L.C22_CHEST_ON_ROOF
    # , code: 150
    # , rom: 0
    # , var: GSWF(729)
    # , item: I.STOP_WATCH
    # , region: R.MI201
    # },
    # { name: L.C22_CHEST_ABOVE_ENTRANCE
    # , code: 149
    # , rom: 0
    # , var: GSWF(730)
    # , item: I.CATCH_CARD_CURSYA
    # , region: R.MI201
    # },
    # { name: L.C22_OPEN_ITEM_DRAGGED_BY_ROPE
    # , code: 151
    # , rom: None
    # , var: None
    # , item: I.MUSHROOM
    # , region: R.MI207
    # },
    # { name: L.C22_OPEN_ITEM_HUNG_BY_ROPE
    # , code: 152
    # , rom: None
    # , var: None
    # , item: I.MUSHROOM
    # , region: R.MI204
    # },
    # { name: L.C22_CHEST_ABOVE_SPIKE_ROOF
    # , code: 153
    # , rom: 0
    # , var: GSW(0, 79)
    # , item: I.HOUSE_KEY
    # , region: R.MI206
    # },
    # { name: L.C22_STAR_BLOCK
    # , code: 154
    # , rom: 0
    # , var: GSW(0, 82)
    # , item: I.CHAPTER_2_3_KEY
    # , region: R.MI208
    # },
    # #endregion
    # #region 2-3
    # { name: L.C23_CHEST_BEHIND_BLOCKS
    # , code: 155
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C23_SLIM_CHEST
    # , code: 156
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C23_STAR_BLOCK
    # , code: 157
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 2-4
    # { name: L.C24_OPEN_ITEM_BEHIND_ROOM_08_SIGN
    # , code: 158
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C24_YELLOW_PURE_HEART
    # , code: 159
    # , rom: None
    # , var: None
    # , item: I.YELLOW_PURE_HEART
    # , region: None
    # , setting: pure_heart
    # },
    # #endregion
    # #region 3-1
    # { name: L.C31_TALK_TO_BARRY_AFTER_DEFEATING_FRANCIS
    # , code: 160
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C31_CHEST_IN_WARP_ZONE_RIGHT_PIPE
    # , code: 161
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C31_OPEN_ITEM_IN_BACKGROUND
    # , code: 162
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C31_CHEST_IN_BACKGROUND_PIPE
    # , code: 163
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C31_CHEST_ABOVE_COLORFUL_PERSONS
    # , code: 164
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C31_OPEN_ITEM_IN_BACKGROUND_2
    # , code: 165
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C31_BOWSER
    # , code: 166
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C31_STAR_BLOCK
    # , code: 167
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 3-2
    # { name: L.C32_HIDDEN_CHEST_NEAR_PIPE
    # , code: 168
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C32_THUDLEY_CHEST
    # , code: 169
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C32_STAR_BLOCK
    # , code: 170
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 3-3
    # { name: L.C33_CHOMPS_CHEST
    # , code: 171
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C33_STAR_BLOCK
    # , code: 172
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 3-4
    # { name: L.C34_CHEST_IN_PIPE_OUTSIDE_OF_CASTLE
    # , code: 173
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C34_FREE_CARRIE
    # , code: 174
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C34_RIGHT_FRANCIS_CHAMBER_CHEST
    # , code: 175
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C34_LEFT_FRANCIS_CHAMBER_CHEST
    # , code: 176
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C34_GREEN_PURE_HEART
    # , code: 177
    # , rom: None
    # , var: None
    # , item: I.GREEN_PURE_HEART
    # , region: None
    # , setting: pure_heart
    # },
    # #endregion
    # #region 4-1
    # { name: L.C41_SQUIRPS
    # , code: 178
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C41_OPEN_ITEM_BEHIND_ASTEROID_1
    # , code: 179
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C41_OPEN_ITEM_BEHIND_ASTEROID_2
    # , code: 180
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C41_STAR_BLOCK
    # , code: 181
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 4-2
    # { name: L.C42_FLIP_THE_DIMENSIONAL_RIFT
    # , code: 182
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C42_OPEN_ITEM_IN_CHASM_3_D
    # , code: 183
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C42_OPEN_ITEM_BEHIND_PIPE_NEAR_BLAPPYS_HOUSE
    # , code: 184
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C42_TALK_TO_BLAPPY
    # , code: 185
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C42_FLEEP
    # , code: 186
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C42_STAR_BLOCK
    # , code: 187
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 4-3
    # { name: L.C43_OPEN_ITEM_BEHIND_FIRST_BLOCKS
    # , code: 188
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C43_OPEN_ITEM_BEHIND_BLOCKS_IN_MANY_WORMHOLE_ROOM
    # , code: 189
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C43_VISIBLE_OPEN_ITEM_IN_BLOCKS
    # , code: 190
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C43_STAR_BLOCK
    # , code: 191
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 4-4
    # { name: L.C44_CHEST_NEAR_BARRIBAD
    # , code: 192
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C44_CHEST_ABOVE_LOCKED_DOOR
    # , code: 193
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C44_CHEST_IN_3_BLOCK_ROOM
    # , code: 194
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C44_CYAN_PURE_HEART
    # , code: 195
    # , rom: None
    # , var: None
    # , item: I.CYAN_PURE_HEART
    # , region: None
    # , setting: pure_heart
    # },
    # #endregion
    # #region 5-1
    # { name: L.C51_CHEST_NEAR_WHACKA
    # , code: 196
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C51_CHEST_AFTER_SHLORPS
    # , code: 197
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C51_CHEST_IN_CHASM_3_D
    # , code: 198
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C51_STAR_BLOCK
    # , code: 199
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 5-2
    # { name: L.C52_FIRE_TABLET
    # , code: 200
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C52_OPEN_ITEM_IN_BACKGROUND
    # , code: 201
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C52_OPEN_ITEM_IN_FRONT_OF_PIPE
    # , code: 202
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C52_STONE_TABLET
    # , code: 203
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C52_WATER_TABLET
    # , code: 204
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C52_CUDGE
    # , code: 205
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C52_CHEST_NEAR_STAR_BLOCK
    # , code: 206
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C52_STAR_BLOCK
    # , code: 207
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 5-3
    # { name: L.C53_OPEN_ITEM_IN_CAVE
    # , code: 208
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C53_SAVE_CRAGLEY_S_CREW
    # , code: 209
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C53_STAR_BLOCK
    # , code: 210
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 5-4
    # { name: L.C54_DOTTIE
    # , code: 211
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C54_OPEN_ITEM_NEAR_PROCESSING_CENTER
    # , code: 212
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C54_OPEN_ITEM_BEHIND_PIPE
    # , code: 213
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C54_FLIP_THE_SKULL
    # , code: 214
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C54_DEFEAT_FLORO_CHUNKS
    # , code: 215
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C54_BLUE_PURE_HEART
    # , code: 216
    # , rom: None
    # , var: None
    # , item: I.PURPLE_PURE_HEART
    # , region: None
    # , setting: pure_heart
    # },
    # #endregion
    # #region 6-1
    # { name: L.C61_PETRIFIED_PURE_HEART
    # , code: 217
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C61_STAR_BLOCK
    # , code: 218
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 6-2
    # { name: L.C62_STAR_BLOCK
    # , code: 219
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 6-3
    # { name: L.C63_STAR_BLOCK
    # , code: 220
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 6-4
    # { name: L.C64_SAMMER_KING_REWARD_1
    # , code: 221
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C64_SAMMER_KING_REWARD_2
    # , code: 222
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C64_SAMMER_KING_REWARD_3
    # , code: 223
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C64_SAMMER_KING_REWARD_4
    # , code: 224
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C64_SAMMER_KING_REWARD_5
    # , code: 225
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C64_SAMMER_KING_REWARD_6
    # , code: 226
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C64_SAMMER_KING_REWARD_7
    # , code: 227
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C64_STAR_BLOCK
    # , code: 228
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 7-1
    # { name: L.C71_CHEST_AFTER_GIGABYTE
    # , code: 229
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C71_OPEN_ITEM_ABOVE_PIPE
    # , code: 230
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C71_GIVE_THE_PETRIFIED_PURE_HEART_TO_JAYDES
    # , code: 231
    # , rom: None
    # , var: None
    # , item: I.PURPLE_PURE_HEART
    # , region: None
    # , setting: pure_heart
    # },
    # { name: L.C71_LUIGI
    # , code: 232
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C71_HIDDEN_OPEN_ITEM_NEAR_LUIGI
    # , code: 233
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C71_HIDDEN_CHEST_IN_LUIGI_S_ROOM
    # , code: 234
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C71_STAR_BLOCK
    # , code: 235
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 7-2
    # { name: L.C72_CHEST_IN_FIRST_DARK_ROOM
    # , code: 236
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C72_DEFEAT_BOWSER
    # , code: 237
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C72_TALK_TO_HAGRA_AND_GET_THE_BOOK_FROM_THE_D_MAN
    # , code: 238
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C72_BRING_THE_DIET_BOOK_TO_HAGRA
    # , code: 239
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C72_STAR_BLOCK
    # , code: 240
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 7-3
    # { name: L.C73_CHEST_RIGHT_OF_25
    # , code: 241
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_CHEST_AT_34
    # , code: 242
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_CHEST_LEFT_OF_47
    # , code: 243
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_WAKE_PEACH_UP
    # , code: 244
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_CHEST_AT_68
    # , code: 245
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_CHEST_RIGHT_OF_69
    # , code: 246
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_CHEST_RIGHT_OF_CYRRUS
    # , code: 247
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_CHEST_ATOP_BUILDING_AT_80
    # , code: 248
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_CHEST_BEHIND_STAR_BLOCK
    # , code: 249
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C73_STAR_BLOCK
    # , code: 250
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 7-4
    # { name: L.C74_SAVE_SUNBI
    # , code: 251
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_CHEST_AFTER_GIGABYTE
    # , code: 252
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_FREE_WHIBBI
    # , code: 253
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_TALK_TO_YEBBI
    # , code: 254
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_OPEN_ITEM_ABOVE_TWO_DOORS
    # , code: 255
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_TALK_TO_REBBI
    # , code: 256
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_BIG_CHEST_BELOW_REBBI
    # , code: 257
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_TALK_TO_BLUBI_AFTER_WHIBBI
    # , code: 258
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_CHEST_BEHIND_STAIRS
    # , code: 259
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_CHEST_FAR_RIGHT_OF_MELEE
    # , code: 260
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C74_WHITE_PURE_HEART
    # , code: 261
    # , rom: None
    # , var: None
    # , item: I.WHITE_PURE_HEART
    # , region: None
    # , setting: pure_heart
    # },
    # #endregion
    # #region 8-1
    # { name: L.C81_RIGHT_CHEST_ABOVE_PEACH_CUTSCENE_START
    # , code: 262
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C81_LEFT_CHEST_ABOVE_PEACH_CUTSCENE_START
    # , code: 263
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C81_CHEST_IN_SOOPA_STRIKER_HALLWAY
    # , code: 264
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 8-2
    # { name: L.C82_LEFT_CHEST_ABOVE_MERLON_ROOM
    # , code: 265
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_MIDDLE_CHEST_ABOVE_MERLON_ROOM
    # , code: 266
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_RIGHT_CHEST_ABOVE_MERLON_ROOM
    # , code: 267
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_OPEN_ITEM_BEHIND_5TH_PIPE
    # , code: 268
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_CHEST_IN_CURSYA_ROOM
    # , code: 269
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_FIRST_HUNG_ITEM
    # , code: 270
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_SECOND_HUNG_ITEM
    # , code: 271
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_THIRD_HUNG_ITEM
    # , code: 272
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_DEFEAT_THE_CHROMEBA
    # , code: 273
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C82_MERLEES_THUNDER_RAGE
    # , code: 274
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 8-3
    # { name: L.C83_RIGHT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS
    # , code: 275
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C83_LEFT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS
    # , code: 276
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C83_CHEST_AFTER_BLOCK_PUZZLE
    # , code: 277
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C83_RIGHT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS
    # , code: 278
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C83_LEFT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS
    # , code: 279
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # #endregion
    # #region 8-4
    # { name: L.C84_CHEST_AFTER_TINY_PASSAGE
    # , code: 280
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C84_CHEST_IN_FIRST_3_D_HALLWAYS
    # , code: 281
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C84_CHEST_IN_SECOND_3_D_HALLWAYS
    # , code: 282
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    # { name: L.C84_CHEST_IN_THIRD_3_D_HALLWAYS
    # , code: 283
    # , rom: None
    # , var: None
    # , item: None
    # , region: None
    # },
    { name: L.CHAPTER_8_4_END
    , code: 284
    , rom: None
    , var: GSW(0, 416)
    , item: E.VICTORY
    , region: R.LS401
    , setting: RT.VANILLA_EVENT
    },
    #endregion
]

LOCATION_DATA: list[LocationData] = [LocationData(**loc) for loc in LOCATION_LIST_DICT]
