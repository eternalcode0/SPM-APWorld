from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from BaseClasses import ItemClassification

from ..names.item_names import ItemName as I
from ..options import ChapterKeysLock, SuperPaperMarioOptions

if TYPE_CHECKING:
    from .. import SuperPaperMarioWorld


@dataclass(frozen=True)
class ItemData:
    name: I
    code: int = field(compare=True, hash=True)
    """A unique id among all other SPM items. Should match the id given to the rom."""
    classification: Callable[[SuperPaperMarioOptions], ItemClassification] | ItemClassification = field(compare=False)
    """What item classification should this be?"""
    amount: Callable[["SuperPaperMarioWorld"], int] | int = field(default=1, compare=False)
    """How many of the item should be in the pool? positive/zero/None only.
    None will handle as if it's a filler item"""
    groups: frozenset[str] = field(compare=False, default=frozenset())
    """What item groups does this belong to"""


# convenience strings bc I hate putting quotes everywhere in dicts
name = "name"
code = "code"
classification = "classification"
amount = "amount"
groups = "groups"


# Groups
GROUP_HEART = "Pure Heart"
GROUP_HERO = "Hero"
GROUP_PIXL = "Pixl"
GROUP_IMPORTANT = "Important"
GROUP_FETCH = "Fetch"
GROUP_ABILITY = "Ability"
GROUP_COOKING_DISC = "Cooking Disc"
GROUP_CONSUMABLE = "Consumable"
GROUP_TOWER_KEY = "Tower Key"
GROUP_CHAPTER_KEY = "Chapter Key"
GROUP_SUBCHAPTER_KEY = "Subchapter Key"


# Amounts
def fetch_amount(world: "SuperPaperMarioWorld") -> int:
    return 1 if world.options.trading_quest else 0


def chapter_key_amount(world: "SuperPaperMarioWorld") -> int:
    return 1 if world.options.chapter_keys_lock.value == ChapterKeysLock.option_chapter_locked else 0


def subchapter_key_amount(world: "SuperPaperMarioWorld") -> int:
    return 1 if world.options.chapter_keys_lock.value == ChapterKeysLock.option_subchapters_locked else 0


def trap_amount(world: "SuperPaperMarioWorld") -> int | None:
    return None if world.options.traps else 0  # None means default to filler/trap fill


def ability_amount(world: "SuperPaperMarioWorld") -> int:
    return 1 if world.options.shuffle_abilities else 0


ITEM_LIST_DICT: list[dict[str, Any]] = [
    #region Important Things
    # MOD: 3 Ruins keys typically use a GSW(0) sequence
    { name: I.RUINS_KEY
    , code: 16
    , classification: ItemClassification.progression
    , amount: 3
    , groups: {GROUP_IMPORTANT}
    },
    { name: I.DOOR_KEY_21
    , code: 17
    , classification: ItemClassification.progression
    , groups: {GROUP_IMPORTANT}
    },
    { name: I.HOUSE_KEY  # 2-2 Key
    , code: 18
    , classification: ItemClassification.progression
    , groups: {GROUP_IMPORTANT}
    },
    # MOD: There are 3 Fort Keys all with the same name/description but diff ids. Should these be combined or kept unique?
    { name: I.FORT_KEY
    , code: 19
    , classification: ItemClassification.progression
    , amount: 3
    , groups: {GROUP_IMPORTANT}
    },
    # { name: I.FORT_KEY
    # , code: 20
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.FORT_KEY
    # , code: 21
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    { name: I.GOLDFISH_BOWL_FISH
    , code: 22
    , classification: ItemClassification.progression
    , amount: 0
    , groups: {GROUP_IMPORTANT}
    },
    # MOD: Should this just be replaced by the Helmet?
    { name: I.GOLDFISH_BOWL_EMPTY
    , code: 23
    , classification: ItemClassification.progression
    , amount: 0
    , groups: {GROUP_IMPORTANT}
    },
    { name: I.HELMET
    , code: 24
    , classification: ItemClassification.progression
    , amount: 0
    , groups: {GROUP_IMPORTANT}
    },
    { name: I.ANCIENT_CLUE
    , code: 25
    , classification: ItemClassification.progression
    , amount: 0
    , groups: {GROUP_IMPORTANT}
    },
    { name: I.DOOR_KEY_42
    , code: 26
    , classification: ItemClassification.progression
    , amount: 0
    , groups: {GROUP_IMPORTANT}
    },
    # MOD: Same deal as Fort keys, 3 of them but diff ids.
    { name: I.DIMENSION_KEY
    , code: 27
    , classification: ItemClassification.progression
    , amount: 3
    , groups: {GROUP_IMPORTANT}
    },
    # { name: I.DIMENSION_KEY
    # , code: 28
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.DIMENSION_KEY
    # , code: 29
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # Temp commented out just to make a smaller itempool until more locations are reachable through logic
    # { name: I.WATER_TABLET
    # , code: 30
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.STONE_TABLET
    # , code: 31
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.FIRE_TABLET
    # , code: 32
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.CAVE_KEY_53
    # , code: 33
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.CAVE_KEY_54
    # , code: 34
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.CARD_KEY
    # , code: 35
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.FLORO_SPROUT
    # , code: 36
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.DOOR_KEY_71
    # , code: 37
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.DOOR_KEY_72
    # , code: 38
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.DIET_BOOK
    # , code: 39
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.DOOR_KEY_74
    # , code: 40
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.BLUE_ORB
    # , code: 41
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.YELLOW_ORB
    # , code: 42
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    # { name: I.RED_ORB
    # , code: 43
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT}
    # },
    { name: I.OLD_KEY
    , code: 47
    , classification: ItemClassification.progression
    , groups: {GROUP_IMPORTANT}
    },
    { name: I.CRYSTAL_BALL
    , code: 51
    , classification: ItemClassification.progression
    , amount: fetch_amount
    , groups: {GROUP_IMPORTANT, GROUP_FETCH}
    },
    { name: I.TRAINING_MACHINE
    , code: 52
    , classification: ItemClassification.progression
    , amount: fetch_amount
    , groups: {GROUP_IMPORTANT, GROUP_FETCH}
    },
    { name: I.YOU_KNOW_WHAT
    , code: 53
    , classification: ItemClassification.progression
    , amount: fetch_amount
    , groups: {GROUP_IMPORTANT, GROUP_FETCH}
    },
    { name: I.PAPER
    , code: 54
    , classification: ItemClassification.progression
    , amount: fetch_amount
    , groups: {GROUP_IMPORTANT, GROUP_FETCH}
    },
    { name: I.AUTOGRAPH
    , code: 55
    , classification: ItemClassification.progression
    , amount: fetch_amount
    , groups: {GROUP_IMPORTANT, GROUP_FETCH}
    },
    { name: I.RANDOM_HOUSE_KEY
    , code: 56
    , classification: ItemClassification.progression
    , amount: fetch_amount
    , groups: {GROUP_IMPORTANT, GROUP_FETCH}
    },
    { name: I.COOKING_DISK_R
    , code: 57
    , classification: ItemClassification.filler
    , groups: {GROUP_COOKING_DISC}
    , amount: 0
    },
    { name: I.COOKING_DISK_W
    , code: 58
    , classification: ItemClassification.filler
    , groups: {GROUP_COOKING_DISC}
    , amount: 0
    },
    { name: I.COOKING_DISK_Y
    , code: 59
    , classification: ItemClassification.filler
    , groups: {GROUP_COOKING_DISC}
    , amount: 0
    },
    { name: I.COOKING_DISK_B
    , code: 60
    , classification: ItemClassification.filler
    , groups: {GROUP_COOKING_DISC}
    , amount: 0
    },
    { name: I.COOKING_DISK_G
    , code: 61
    , classification: ItemClassification.filler
    , groups: {GROUP_COOKING_DISC}
    , amount: 0
    },
    { name: I.COOKING_DISK_PU
    , code: 62
    , classification: ItemClassification.filler
    , groups: {GROUP_COOKING_DISC}
    , amount: 0
    },
    # { name: I.GOLDEN_CARD
    # , code: 64
    # , classification: ItemClassification.filler
    # },
    #endregion
    #region Consumables
    { name: I.FIRE_BURST
    , code: 65
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ICE_STORM
    , code: 66
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.THUNDER_RAGE
    , code: 67
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHOOTING_STAR
    , code: 68
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POW_BLOCK
    , code: 69
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHELL_SHOCK
    , code: 70
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLD_BAR
    , code: 71
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLD_BAR_X3
    , code: 72
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLOCK_BLOCK
    , code: 73
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.COURAGE_SHELL
    , code: 74
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MIGHTY_TONIC
    , code: 75
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.VOLT_SHROOM
    , code: 76
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GHOST_SHROOM
    , code: 77
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SLEEPY_SHEEP
    , code: 78
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STOP_WATCH
    , code: 79
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_SHAKE
    , code: 80
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SUPER_SHROOM_SHAKE
    , code: 81
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ULTRA_SHROOM_SHAKE
    , code: 82
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DRIED_SHROOM
    , code: 83
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LIFE_SHROOM
    , code: 84
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LONG_LAST_SHAKE
    , code: 85
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MYSTERY_BOX
    , code: 86
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CATCH_CARD
    , code: 87
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CATCH_CARD_SP
    , code: 88
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HP_PLUS
    , code: 89
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POWER_PLUS
    , code: 90
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLUE_APPLE
    , code: 91
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.YELLOW_APPLE
    , code: 92
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.RED_APPLE
    , code: 93
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PINK_APPLE
    , code: 94
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLACK_APPLE
    , code: 95
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STAR_MEDAL
    , code: 96
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLD_MEDAL
    , code: 97
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POISON_SHROOM
    , code: 98
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SLIMY_SHROOM
    , code: 99
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PEACHY_PEACH
    , code: 100
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KEEL_MANGO
    , code: 101
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PRIMORDIAL_FRUIT
    , code: 102
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLDEN_LEAF
    , code: 103
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.TURTLEY_LEAF
    , code: 104
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CAKE_MIX
    , code: 105
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.WHACKA_BUMP
    , code: 106
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HORSETAIL
    , code: 107
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRESH_PASTA_BUNCH
    , code: 108
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HOT_SAUCE
    , code: 109
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.INKY_SAUCE
    , code: 110
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DAYZEE_TEAR
    , code: 111
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SAP_SOUP
    , code: 112
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BONE_IN_CUT
    , code: 113
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRESH_VEGGIE
    , code: 114
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SMELLY_HERB
    , code: 115
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_JAR
    , code: 116
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POWER_STEAK
    , code: 117
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BIG_EGG
    , code: 118
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MILD_COCOA_BEAN
    , code: 119
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SWEET_CHOCO_BAR
    , code: 120
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_CHOCO_BAR
    , code: 121
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLDEN_CHOCO_BAR
    , code: 122
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GRADUAL_SYRUP
    , code: 123
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DAYZEE_SYRUP
    , code: 124
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SLIMY_EXTRACT
    , code: 125
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRIED_SHROOM_PLATE
    , code: 126
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ROAST_SHROOM_DISH
    , code: 127
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_STEAK
    , code: 128
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_SHROOM
    , code: 129
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_SUPER
    , code: 130
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_BROTH
    , code: 131
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MUSHROOM_CREPE
    , code: 132
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_CAKE
    , code: 133
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CHOCOLATE_CAKE
    , code: 134
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HEARTFUL_CAKE
    , code: 135
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MOUSSE
    , code: 136
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PEACH_TART
    , code: 137
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HORSETAIL_TART
    , code: 138
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SWEET_COOKIE_SNACK
    , code: 139
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPA_DUMPLING
    , code: 140
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SAP_MUFFIN
    , code: 141
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.TOWN_SPECIAL
    , code: 142
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MANGO_PUDDING
    , code: 143
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LOVE_PUDDING
    , code: 144
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.COUPLES_CAKE
    , code: 145
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUIT_PARFAIT
    , code: 146
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SNOW_CONE
    , code: 147
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SNOW_BUNNY
    , code: 148
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BERRY_SNOW_BUNNY
    , code: 149
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_CANDY
    , code: 150
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ELECTRO_POP
    , code: 151
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HERB_TEA
    , code: 152
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPA_TEA
    , code: 153
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPAGHETTI_PLATE
    , code: 154
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPICY_PASTA_DISH
    , code: 155
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.INK_PASTA_DISH
    , code: 156
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPASTA_DISH
    , code: 157
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LOVE_NOODLE_DISH
    , code: 158
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRIED_EGG
    , code: 159
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.EGG_BOMB
    , code: 160
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_DYNAMITE
    , code: 161
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPIT_ROAST
    , code: 162
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.METEOR_MEAL
    , code: 163
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.OMELETTE_PLATE
    , code: 164
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPICY_SOUP
    , code: 165
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HOT_DOG
    , code: 166
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HEALTHY_SALAD
    , code: 167
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_DINNER
    , code: 168
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_SPECIAL
    , code: 169
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_DELUXE
    , code: 170
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPACE_FOOD
    , code: 171
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.EMERGENCY_RATION
    , code: 172
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DANGEROUS_DELIGHT
    , code: 173
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.TRIAL_STEW
    , code: 174
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MISTAKE
    , code: 175
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MISTAKE_SLEEPY_SHEEP
    , code: 176
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.WARM_COCOA
    , code: 177
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ODD_DINNER
    , code: 178
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.INKY_SOUP
    , code: 179
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GINGERBREAD_HOUSE
    , code: 180
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.VOLCANO_SHROOM
    , code: 181
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPA_PILAF
    , code: 182
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPICY_DINNER
    , code: 183
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_PUDDING
    , code: 184
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HEAVY_MEAL
    , code: 185
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PRIMORDIAL_DINNER
    , code: 186
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GORGEOUS_STEAK
    , code: 187
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLDEN_MEAL
    , code: 188
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LUXURIOUS_SET
    , code: 189
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ROAST_WHACKA_BUMP
    , code: 190
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_BREAKFAST
    , code: 191
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_LUNCH
    , code: 192
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SKY_JUICE
    , code: 193
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STAMINA_JUICE
    , code: 194
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CHOCO_PASTA_DISH
    , code: 195
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_DELICACY
    , code: 196
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ROAST_HORSETAIL
    , code: 197
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SAP_SYRUP
    , code: 198
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HAMBURGER
    , code: 199
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PEACH_JUICE
    , code: 200
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STANDARD_CHOCOLATE
    , code: 201
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_CAKE
    , code: 202
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_HAMBURGER
    , code: 203
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_PUNCH
    , code: 204
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_SHROOM
    , code: 205
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLOCK_MEAL
    , code: 206
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.VEGGIE_SET
    , code: 207
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.WEIRD_EXTRACT
    , code: 208
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.AWESOME_SNACK
    , code: 209
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MANGO_JUICE
    , code: 210
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MEAT_PASTA_DISH
    , code: 211
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MIXED_SHAKE
    , code: 212
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MIRACLE_DINNER
    , code: 213
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MEGATON_DINNER
    , code: 214
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LOVELY_CHOCOLATE
    , code: 215
    , classification: ItemClassification.filler
    , amount: None
    , groups: {GROUP_CONSUMABLE}
    },
    #endregion
    #region Non-standard Items
    # Things that exist in-game but not as "items"
    { name: I.CHARACTER_MARIO
    , code: 216
    , classification: ItemClassification.progression
    , groups: {GROUP_HERO}
    },
    { name: I.CHARACTER_PEACH
    , code: 217
    , classification: ItemClassification.progression
    , groups: {GROUP_HERO}
    },
    { name: I.CHARACTER_BOWSER
    , code: 218
    , classification: ItemClassification.progression
    , groups: {GROUP_HERO}
    },
    { name: I.CHARACTER_LUIGI
    , code: 219
    , classification: ItemClassification.progression
    , groups: {GROUP_HERO}
    },
    { name: I.PIXL_TIPPI
    , code: 220
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_THOREAU
    , code: 221
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_BOOMER
    , code: 222
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_SLIM
    , code: 223
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_THUDLEY
    , code: 224
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_CARRIE
    , code: 225
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_FLEEP
    , code: 226
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_CUDGE
    , code: 227
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_DOTTIE
    , code: 228
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_PICCOLO
    , code: 229
    , classification: ItemClassification.progression
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_BARRY
    , code: 230
    , classification: ItemClassification.useful
    , groups: {GROUP_PIXL}
    },
    { name: I.PIXL_DASHELL
    , code: 231
    , classification: ItemClassification.useful
    , groups: {GROUP_PIXL}
    },
    { name: I.RED_PURE_HEART
    , code: 232
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    { name: I.ORANGE_PURE_HEART
    , code: 233
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    { name: I.YELLOW_PURE_HEART
    , code: 234
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    { name: I.GREEN_PURE_HEART
    , code: 235
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    { name: I.CYAN_PURE_HEART
    , code: 236
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    { name: I.BLUE_PURE_HEART
    , code: 237
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    { name: I.PURPLE_PURE_HEART
    , code: 238
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    { name: I.WHITE_PURE_HEART
    , code: 239
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    },
    #endregion
    #region AP Items
    # These items don't exist in-game. They're concepts introduced by the rando.
    { name: I.ABILITY_FLIP
    , code: 240
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.ABILITY_UMBRELLA
    , code: 241
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.ABILITY_FIRE
    , code: 242
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.ABILITY_SUPER_JUMP
    , code: 243
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.CHAPTER_1_KEY
    , code: 244
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_2_KEY
    , code: 245
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_3_KEY
    , code: 246
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_4_KEY
    , code: 247
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_5_KEY
    , code: 248
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_6_KEY
    , code: 249
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_7_KEY
    , code: 250
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_8_KEY
    , code: 251
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_1_1_KEY
    , code: 252
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_1_2_KEY
    , code: 253
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_1_3_KEY
    , code: 254
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_1_4_KEY
    , code: 255
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_1_KEY
    , code: 256
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_2_KEY
    , code: 257
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_3_KEY
    , code: 258
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_4_KEY
    , code: 259
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_1_KEY
    , code: 260
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_2_KEY
    , code: 261
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_3_KEY
    , code: 262
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_4_KEY
    , code: 263
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_1_KEY
    , code: 264
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_2_KEY
    , code: 265
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_3_KEY
    , code: 266
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_4_KEY
    , code: 267
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_1_KEY
    , code: 268
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_2_KEY
    , code: 269
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_3_KEY
    , code: 270
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_4_KEY
    , code: 271
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_1_KEY
    , code: 272
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_2_KEY
    , code: 273
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_3_KEY
    , code: 274
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_4_KEY
    , code: 275
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_1_KEY
    , code: 276
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_2_KEY
    , code: 277
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_3_KEY
    , code: 278
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_4_KEY
    , code: 279
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_1_KEY
    , code: 280
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_2_KEY
    , code: 281
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_3_KEY
    , code: 282
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_4_KEY
    , code: 283
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.SLOW_CURSYA_TRAP
    , code: 284
    , classification: ItemClassification.trap
    , amount: None
    },
    { name: I.HEAVY_CURSYA_TRAP
    , code: 285
    , classification: ItemClassification.trap
    , amount: None
    },
    { name: I.REVERSYA_CURSYA_TRAP
    , code: 286
    , classification: ItemClassification.trap
    , amount: None
    },
    { name: I.TECH_CURSYA_TRAP
    , code: 287
    , classification: ItemClassification.trap
    , amount: None
    },
    { name: I.BACK_CURSYA_TRAP
    , code: 288
    , classification: ItemClassification.trap
    , amount: None
    },
    #endregion
]

ITEM_DATA = [ItemData(**data) for data in ITEM_LIST_DICT]
