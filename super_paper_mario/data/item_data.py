from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from BaseClasses import ItemClassification

from ..names.item_names import ItemName as I
from ..options import ChapterDoorAccess, SuperPaperMarioOptions

if TYPE_CHECKING:
    from .. import SuperPaperMarioWorld


@dataclass(frozen=True)
class ItemData:
    name: I
    code: int = field(compare=False, hash=False)
    """A unique id among all other SPM items. Should match the id given to the rom. Short value"""
    classification: Callable[[SuperPaperMarioOptions], ItemClassification] | ItemClassification = field(
        compare=False, default=ItemClassification.filler
    )
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
GROUP_TOWER_KEY = "Tower Key"  # This should only be paired with either chapter / subchapter key
GROUP_CHAPTER_KEY = "Chapter Key"
GROUP_SUBCHAPTER_KEY = "Subchapter Key"
GROUP_CURSYA_TRAP = "Cursya Trap"
GROUP_MAP = "Map"
GROUP_CATCH_CARD = "Catch Cards"
GROUP_CHAPTER_ITEMS = "Chapter Items"  # This should only be paired with a specific chapter item group
GROUP_C1_ITEMS = "Chapter 1 Items"
GROUP_C2_ITEMS = "Chapter 2 Items"
GROUP_C3_ITEMS = "Chapter 3 Items"
GROUP_C4_ITEMS = "Chapter 4 Items"
GROUP_C5_ITEMS = "Chapter 5 Items"
GROUP_C6_ITEMS = "Chapter 6 Items"  # Declared for brevity but there are no chapter 6 items
GROUP_C7_ITEMS = "Chapter 7 Items"
GROUP_C8_ITEMS = "Chapter 8 Items"


# Amounts
def heart_amount(world: "SuperPaperMarioWorld") -> int:
    return 1 if world.options.shuffle_pure_hearts else 0  # else pure hearts are placed via RT.VANILLA_WORLD


def fetch_amount(world: "SuperPaperMarioWorld") -> int:
    return 1 if world.options.trading_quest else 0


def chapter_key_amount(world: "SuperPaperMarioWorld") -> int:
    return 0
    # return 1 if world.options.chapter_door_access.value == ChapterDoorAccess.option_chapter_locked else 0


def subchapter_key_amount(world: "SuperPaperMarioWorld") -> int:
    return 0
    # return 1 if world.options.chapter_door_access.value == ChapterDoorAccess.option_subchapters_locked else 0


def ability_amount(world: "SuperPaperMarioWorld") -> int:
    return 1 if world.options.ability_shuffle else 0


# def maps_amount(world: "SuperPaperMarioWorld") -> int:
#     return 1 if world.options.treasure_maps.map_items_in_pool else 0


ITEM_LIST_DICT: list[dict[str, Any]] = [
    #region Important Things
    # MOD: 3 Ruins keys typically use a GSW(0) sequence
    { name: I.RUINS_KEY
    , code: 16
    , classification: ItemClassification.progression
    , amount: 3
    , groups: {GROUP_IMPORTANT, GROUP_C1_ITEMS, GROUP_CHAPTER_ITEMS}
    },
    { name: I.DOOR_KEY_21
    , code: 17
    , classification: ItemClassification.progression
    , groups: {GROUP_IMPORTANT, GROUP_C2_ITEMS, GROUP_CHAPTER_ITEMS}
    },
    { name: I.HOUSE_KEY  # 2-2 Key
    , code: 18
    , classification: ItemClassification.progression
    , groups: {GROUP_IMPORTANT, GROUP_C2_ITEMS, GROUP_CHAPTER_ITEMS}
    },
    # MOD: There are 3 Fort Keys all with the same name/description but diff ids. Should these be combined or kept unique?
    { name: I.FORT_KEY
    , code: 19
    , classification: ItemClassification.progression
    , amount: 3
    , groups: {GROUP_IMPORTANT, GROUP_C3_ITEMS, GROUP_CHAPTER_ITEMS}
    },
    # { name: I.FORT_KEY
    # , code: 20
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT, GROUP_C3_ITEMS, GROUP_CHAPTER_ITEMS}
    # },
    # { name: I.FORT_KEY
    # , code: 21
    # , classification: ItemClassification.progression
    # , groups: {GROUP_IMPORTANT, GROUP_C3_ITEMS, GROUP_CHAPTER_ITEMS}
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
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ICE_STORM
    , code: 66
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.THUNDER_RAGE
    , code: 67
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHOOTING_STAR
    , code: 68
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POW_BLOCK
    , code: 69
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHELL_SHOCK
    , code: 70
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLD_BAR
    , code: 71
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLD_BAR_X3
    , code: 72
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLOCK_BLOCK
    , code: 73
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.COURAGE_SHELL
    , code: 74
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MIGHTY_TONIC
    , code: 75
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.VOLT_SHROOM
    , code: 76
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GHOST_SHROOM
    , code: 77
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SLEEPY_SHEEP
    , code: 78
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STOP_WATCH
    , code: 79
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_SHAKE
    , code: 80
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SUPER_SHROOM_SHAKE
    , code: 81
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ULTRA_SHROOM_SHAKE
    , code: 82
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DRIED_SHROOM
    , code: 83
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LIFE_SHROOM
    , code: 84
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LONG_LAST_SHAKE
    , code: 85
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MYSTERY_BOX
    , code: 86
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CATCH_CARD
    , code: 87
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CATCH_CARD_SP
    , code: 88
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HP_PLUS
    , code: 89
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POWER_PLUS
    , code: 90
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLUE_APPLE
    , code: 91
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.YELLOW_APPLE
    , code: 92
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.RED_APPLE
    , code: 93
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PINK_APPLE
    , code: 94
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLACK_APPLE
    , code: 95
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STAR_MEDAL
    , code: 96
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLD_MEDAL
    , code: 97
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POISON_SHROOM
    , code: 98
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SLIMY_SHROOM
    , code: 99
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PEACHY_PEACH
    , code: 100
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KEEL_MANGO
    , code: 101
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PRIMORDIAL_FRUIT
    , code: 102
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLDEN_LEAF
    , code: 103
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.TURTLEY_LEAF
    , code: 104
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CAKE_MIX
    , code: 105
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.WHACKA_BUMP
    , code: 106
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HORSETAIL
    , code: 107
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRESH_PASTA_BUNCH
    , code: 108
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HOT_SAUCE
    , code: 109
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.INKY_SAUCE
    , code: 110
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DAYZEE_TEAR
    , code: 111
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SAP_SOUP
    , code: 112
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BONE_IN_CUT
    , code: 113
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRESH_VEGGIE
    , code: 114
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SMELLY_HERB
    , code: 115
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_JAR
    , code: 116
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.POWER_STEAK
    , code: 117
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BIG_EGG
    , code: 118
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MILD_COCOA_BEAN
    , code: 119
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SWEET_CHOCO_BAR
    , code: 120
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_CHOCO_BAR
    , code: 121
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLDEN_CHOCO_BAR
    , code: 122
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GRADUAL_SYRUP
    , code: 123
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DAYZEE_SYRUP
    , code: 124
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SLIMY_EXTRACT
    , code: 125
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRIED_SHROOM_PLATE
    , code: 126
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ROAST_SHROOM_DISH
    , code: 127
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_STEAK
    , code: 128
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_SHROOM
    , code: 129
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_SUPER
    , code: 130
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_BROTH
    , code: 131
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MUSHROOM_CREPE
    , code: 132
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_CAKE
    , code: 133
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CHOCOLATE_CAKE
    , code: 134
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HEARTFUL_CAKE
    , code: 135
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MOUSSE
    , code: 136
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PEACH_TART
    , code: 137
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HORSETAIL_TART
    , code: 138
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SWEET_COOKIE_SNACK
    , code: 139
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPA_DUMPLING
    , code: 140
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SAP_MUFFIN
    , code: 141
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.TOWN_SPECIAL
    , code: 142
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MANGO_PUDDING
    , code: 143
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LOVE_PUDDING
    , code: 144
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.COUPLES_CAKE
    , code: 145
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUIT_PARFAIT
    , code: 146
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SNOW_CONE
    , code: 147
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SNOW_BUNNY
    , code: 148
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BERRY_SNOW_BUNNY
    , code: 149
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HONEY_CANDY
    , code: 150
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ELECTRO_POP
    , code: 151
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HERB_TEA
    , code: 152
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPA_TEA
    , code: 153
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPAGHETTI_PLATE
    , code: 154
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPICY_PASTA_DISH
    , code: 155
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.INK_PASTA_DISH
    , code: 156
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPASTA_DISH
    , code: 157
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LOVE_NOODLE_DISH
    , code: 158
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRIED_EGG
    , code: 159
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.EGG_BOMB
    , code: 160
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_DYNAMITE
    , code: 161
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPIT_ROAST
    , code: 162
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.METEOR_MEAL
    , code: 163
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.OMELETTE_PLATE
    , code: 164
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPICY_SOUP
    , code: 165
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HOT_DOG
    , code: 166
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HEALTHY_SALAD
    , code: 167
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_DINNER
    , code: 168
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_SPECIAL
    , code: 169
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_DELUXE
    , code: 170
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPACE_FOOD
    , code: 171
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.EMERGENCY_RATION
    , code: 172
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DANGEROUS_DELIGHT
    , code: 173
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.TRIAL_STEW
    , code: 174
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MISTAKE
    , code: 175
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MISTAKE_SLEEPY_SHEEP
    , code: 176
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.WARM_COCOA
    , code: 177
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ODD_DINNER
    , code: 178
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.INKY_SOUP
    , code: 179
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GINGERBREAD_HOUSE
    , code: 180
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.VOLCANO_SHROOM
    , code: 181
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.KOOPA_PILAF
    , code: 182
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SPICY_DINNER
    , code: 183
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_PUDDING
    , code: 184
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HEAVY_MEAL
    , code: 185
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PRIMORDIAL_DINNER
    , code: 186
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GORGEOUS_STEAK
    , code: 187
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.GOLDEN_MEAL
    , code: 188
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LUXURIOUS_SET
    , code: 189
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ROAST_WHACKA_BUMP
    , code: 190
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_BREAKFAST
    , code: 191
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.DYLLIS_LUNCH
    , code: 192
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SKY_JUICE
    , code: 193
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STAMINA_JUICE
    , code: 194
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.CHOCO_PASTA_DISH
    , code: 195
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SHROOM_DELICACY
    , code: 196
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.ROAST_HORSETAIL
    , code: 197
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.SAP_SYRUP
    , code: 198
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.HAMBURGER
    , code: 199
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.PEACH_JUICE
    , code: 200
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.STANDARD_CHOCOLATE
    , code: 201
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_CAKE
    , code: 202
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_HAMBURGER
    , code: 203
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_PUNCH
    , code: 204
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.FRUITY_SHROOM
    , code: 205
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.BLOCK_MEAL
    , code: 206
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.VEGGIE_SET
    , code: 207
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.WEIRD_EXTRACT
    , code: 208
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.AWESOME_SNACK
    , code: 209
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MANGO_JUICE
    , code: 210
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MEAT_PASTA_DISH
    , code: 211
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MIXED_SHAKE
    , code: 212
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MIRACLE_DINNER
    , code: 213
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.MEGATON_DINNER
    , code: 214
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    { name: I.LOVELY_CHOCOLATE
    , code: 215
    , classification: ItemClassification.filler
    , groups: {GROUP_CONSUMABLE}
    },
    #endregion
    #region Special Items
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
    #endregion
    #region Unused items
    # { name: "Pointer Finger", code: 232 },
    # { name: "Card Bag", code: 233 },
    #endreion
    #region Fleep Maps
    # { name: I.MAP_1
    # , code: 234
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_2
    # , code: 235
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_3
    # , code: 236
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_4
    # , code: 237
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_5
    # , code: 238
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_6
    # , code: 239
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_7
    # , code: 240
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_8
    # , code: 241
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_9
    # , code: 242
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_10
    # , code: 243
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_11
    # , code: 244
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_12
    # , code: 245
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_13
    # , code: 246
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_14
    # , code: 247
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_15
    # , code: 248
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_16
    # , code: 249
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_17
    # , code: 250
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_18
    # , code: 251
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_19
    # , code: 252
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_20
    # , code: 253
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_21
    # , code: 254
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_22
    # , code: 255
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_23
    # , code: 256
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_24
    # , code: 257
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_25
    # , code: 258
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_26
    # , code: 259
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_27
    # , code: 260
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_28
    # , code: 261
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_29
    # , code: 262
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_30
    # , code: 263
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_31
    # , code: 264
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_32
    # , code: 265
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_33
    # , code: 266
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_34
    # , code: 267
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_35
    # , code: 268
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_36
    # , code: 269
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_37
    # , code: 270
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_38
    # , code: 271
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_39
    # , code: 272
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_40
    # , code: 273
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_41
    # , code: 274
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_42
    # , code: 275
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_43
    # , code: 276
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_44
    # , code: 277
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_45
    # , code: 278
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_46
    # , code: 279
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_47
    # , code: 280
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    # { name: I.MAP_48
    # , code: 281
    # , classification: ItemClassification.progression
    # , amount: maps_amount
    # , groups: {GROUP_MAP}
    # },
    #endregion
    #region Card Items
    { name: I.CATCH_CARD_GOOMBA
    , code: 282
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_GOOMBA
    , code: 283
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPIKED_GOOMBA
    , code: 284
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SPIKED_GOOMBA
    , code: 285
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PARAGOOMBA
    , code: 286
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_PARAGOOMBA
    , code: 287
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GLOOMBA
    , code: 288
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_HEADBONK_GOOMBA
    , code: 289
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_HEADBONK_GOOMBA
    , code: 290
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_KOOPA_TROOPA
    , code: 291
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MEGA_KOOPA
    , code: 292
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_KOOPA
    , code: 293
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_KOOPATROL
    , code: 294
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_KOOPATROL
    , code: 295
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PARATROOPA
    , code: 296
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_PARATROOPA
    , code: 297
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BUZZY_BEETLE
    , code: 298
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPIKE_TOP
    , code: 299
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SPIKE_TOP
    , code: 300
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PARABUZZY
    , code: 301
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPIKY_PARABUZZY
    , code: 302
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_STONE_BUZZY
    , code: 303
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_STONE_BUZZY
    , code: 304
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPINY
    , code: 305
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SPINY
    , code: 306
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_LAKITU
    , code: 307
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DULL_BONES
    , code: 308
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_DULL_BONES
    , code: 309
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DRY_BONES
    , code: 310
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_HAMMER_BRO
    , code: 311
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_HAMMER_BRO
    , code: 312
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOOMERANG_BRO
    , code: 313
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_BOOMERANG_BRO
    , code: 314
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FIRE_BRO
    , code: 315
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_FIRE_BRO
    , code: 316
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MAGIKOOPA
    , code: 317
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_MAGIKOOPA
    , code: 318
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_KOOPA_STRIKER
    , code: 319
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TOOPA_STRIKER
    , code: 320
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SOOPA_STRIKER
    , code: 321
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_STRIKER
    , code: 322
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CLUBBA
    , code: 323
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_CLUBBA
    , code: 324
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SQUIGLET
    , code: 325
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SQUIG
    , code: 326
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SQUOG
    , code: 327
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SQUOINKER
    , code: 328
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SQUIGLET
    , code: 329
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPROING_OING
    , code: 330
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOING_OING
    , code: 331
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_ZOING_OING
    , code: 332
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SPROING_OING
    , code: 333
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOOMBOXER
    , code: 334
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BEEPBOXER
    , code: 335
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BLASTBOXER
    , code: 336
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_BOOMBOXER
    , code: 337
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PIRANHA_PLANT
    , code: 338
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PUTRID_PIRANHA
    , code: 339
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FROST_PIRANHA
    , code: 340
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CRAZEE_DAYZEE
    , code: 341
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_AMAZY_DAYZEE
    , code: 342
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_DAYZEE
    , code: 343
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FUZZY
    , code: 344
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PINK_FUZZY
    , code: 345
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_FUZZY
    , code: 346
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_POKEY
    , code: 347
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_POISON_POKEY
    , code: 348
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_POKEY
    , code: 349
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CHEEP_CHEEP
    , code: 350
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BLOOPER
    , code: 351
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BITTACUDA
    , code: 352
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_JAWBUS
    , code: 353
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_RAWBUS
    , code: 354
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_JAWBUS
    , code: 355
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GAWBUS
    , code: 356
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPANIA
    , code: 357
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SPANIA
    , code: 358
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CURSYA
    , code: 359
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BACK_CURSYA
    , code: 360
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TECH_CURSYA
    , code: 361
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_HEAVY_CURSYA
    , code: 362
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_REVERSYA_CURSYA
    , code: 363
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_CURSYA
    , code: 364
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_TECH_CURSYA
    , code: 365
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_HEAVY_CURSYA
    , code: 366
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_REVERSYA_CURSYA
    , code: 367
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SWOOPER
    , code: 368
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CHERBIL
    , code: 369
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_ICE_CHERBIL
    , code: 370
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_POISON_CHERBIL
    , code: 371
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_CHERBIL
    , code: 372
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOO
    , code: 373
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_BOO
    , code: 374
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_DARK_BOO
    , code: 375
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_ATOMIC_BOO
    , code: 376
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GROWMEBA
    , code: 377
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BLOMEBA
    , code: 378
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CHROMEBA
    , code: 379
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_GROWMEBA
    , code: 380
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MISTER_I
    , code: 381
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_RED_I
    , code: 382
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CHAIN_CHOMP
    , code: 383
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_RED_CHOMP
    , code: 384
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_THE_UNDERCHOMP
    , code: 385
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_CHOMP
    , code: 386
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BALD_CLEFT
    , code: 387
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MOON_CLEFT
    , code: 388
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_CLEFT
    , code: 389
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SHLURP
    , code: 390
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SHLORP
    , code: 391
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SHLURP
    , code: 392
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_THWOMP
    , code: 393
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPINY_TROMP
    , code: 394
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPIKY_TROMP
    , code: 395
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BULLET_BILL
    , code: 396
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BILL_BLASTER
    , code: 397
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_RUFF_PUFF
    , code: 398
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_RUFF_PUFF
    , code: 399
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_LAVA_BUBBLE
    , code: 400
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TILEOID_G
    , code: 401
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TILEOID_B
    , code: 402
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TILEOID_R
    , code: 403
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TILEOID_Y
    , code: 404
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_TILEOID
    , code: 405
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MEOWBOMB
    , code: 406
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PATROL_MEOW
    , code: 407
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_AIR_MEOW
    , code: 408
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SURPRISE_MEOW
    , code: 409
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BIG_MEOW
    , code: 410
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MEOWMAID
    , code: 411
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SECURI_MEOW
    , code: 412
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_JELLIEN
    , code: 413
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FOTON
    , code: 414
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_WARPID
    , code: 415
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_EELIGON
    , code: 416
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_HOOLIGON
    , code: 417
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_EELIGON
    , code: 418
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_LONGATOR
    , code: 419
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_LONGADILE
    , code: 420
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_LONGATOR
    , code: 421
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BARRIBAD
    , code: 422
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SOBARRIBAD
    , code: 423
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_BARRIBAD
    , code: 424
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PIGARITHM
    , code: 425
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_HOGARITHM
    , code: 426
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_PIGARITHM
    , code: 427
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CHOPPA
    , code: 428
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_COPTA
    , code: 429
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_CHOPPA
    , code: 430
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MUTH
    , code: 431
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MEGA_MUTH
    , code: 432
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_MUTH
    , code: 433
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FLORO_SAPIEN
    , code: 434
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FLORO_CRAGNIEN
    , code: 435
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_NINJOE
    , code: 436
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_NINJOHN
    , code: 437
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_NINJERRY
    , code: 438
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_NINJOE
    , code: 439
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_UNDERHAND
    , code: 440
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SKELLOBIT
    , code: 441
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPIKY_SKELLOBIT
    , code: 442
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SKELLOBIT
    , code: 443
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_SPIKY_SKELLOBIT
    , code: 444
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SKELLOBOMBER
    , code: 445
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SKELLOBAIT
    , code: 446
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SPIKY_SKELLOBAIT
    , code: 447
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_RED_MAGIBLOT
    , code: 448
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BLUE_MAGIBLOT
    , code: 449
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_YELLOW_MAGIBLOT
    , code: 450
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_MAGIBLOT
    , code: 451
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MEGABITE
    , code: 452
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GIGABITE
    , code: 453
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_MEGABITE
    , code: 454
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_MARIO
    , code: 455
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_LUIGI
    , code: 456
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_PEACH
    , code: 457
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DARK_BOWSER
    , code: 458
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_ZOMBIE_SHROOM
    , code: 459
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GHOUL_SHROOM
    , code: 460
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FRACKTAIL
    , code: 461
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_WRACKTAIL
    , code: 462
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FRACKLE
    , code: 463
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_WRACKLE
    , code: 464
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BIG_BLOOPER
    , code: 465
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FRANCIS
    , code: 466
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_KING_CROACUS
    , code: 467
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BONECHILL
    , code: 468
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_COUNT_BLECK
    , code: 469
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_NASTASIA
    , code: 470
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_O_CHUNKS
    , code: 471
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MIMI
    , code: 472
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MR_L
    , code: 473
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BROBOT
    , code: 474
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BROBOT_L_TYPE
    , code: 475
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DIMENTIO
    , code: 476
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SUPER_DIMENTIO
    , code: 477
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MERLON
    , code: 478
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_NOLREM
    , code: 479
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MERLUVLEE
    , code: 480
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MERLEE
    , code: 481
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BESTOVIUS
    , code: 482
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_OLD_MAN_WATCHITT
    , code: 483
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MERLUMINA
    , code: 484
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_THE_INTER_NED
    , code: 485
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_THE_INTER_CHET
    , code: 486
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_WELDERBERG
    , code: 487
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_RED_GREEN
    , code: 488
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GNIP
    , code: 489
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GNAW
    , code: 490
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SQUIRPS
    , code: 491
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FLINT_CRAGLEY
    , code: 492
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_HORNFELS_MONZO
    , code: 493
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_KING_SAMMER
    , code: 494
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SAMMER_GUY
    , code: 495
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SMALL_SAMMER_GUY
    , code: 496
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BIG_SAMMER_GUY
    , code: 497
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_LUVBI
    , code: 498
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_JAYDES
    , code: 499
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GRAMBI
    , code: 500
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_WHACKA
    , code: 501
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MARIO
    , code: 502
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_LUIGI
    , code: 503
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PEACH_1
    , code: 504
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PEACH_2
    , code: 505
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PEACH_3
    , code: 506
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOWSER_1
    , code: 507
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOWSER_2
    , code: 508
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TIPPI
    , code: 509
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_THOREAU
    , code: 510
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOOMER
    , code: 511
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SLIM
    , code: 512
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_THUDLEY
    , code: 513
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CARRIE
    , code: 514
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_FLEEP
    , code: 515
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_CUDGE
    , code: 516
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DOTTIE
    , code: 517
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BARRY
    , code: 518
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_DASHELL
    , code: 519
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PICCOLO
    , code: 520
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TIPTRON
    , code: 521
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GOOMBARIO
    , code: 522
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_KOOPER
    , code: 523
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOMBETTE
    , code: 524
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_PARAKARRY
    , code: 525
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_BOW
    , code: 526
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_WATT
    , code: 527
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_SUSHIE
    , code: 528
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_LAKILESTER
    , code: 529
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_GOOMBELLA
    , code: 530
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_KOOPS
    , code: 531
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MADAME_FLURRIE
    , code: 532
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_YOSHI
    , code: 533
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_VIVIAN
    , code: 534
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_ADMIRAL_BOBBERY
    , code: 535
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_MS_MOWZ
    , code: 536
    , groups: {GROUP_CATCH_CARD}
    },
    { name: I.CATCH_CARD_TOAD
    , code: 537
    , groups: {GROUP_CATCH_CARD}
    },
    #endregion
    #region AP Items
    # These items don't exist in-game. They're concepts introduced by the rando.
    # Start at 0x300 bc apparently the "Action Command" sprites are after the catch cards, no idea where they stop.
    { name: I.RED_PURE_HEART
    , code: 768
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    , amount: heart_amount
    },
    { name: I.ORANGE_PURE_HEART
    , code: 769
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    , amount: heart_amount
    },
    { name: I.YELLOW_PURE_HEART
    , code: 770
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    , amount: heart_amount
    },
    { name: I.GREEN_PURE_HEART
    , code: 771
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    # , amount: heart_amount  # commented to default to 1 until its chapter logic is finished
    },
    { name: I.CYAN_PURE_HEART
    , code: 772
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    # , amount: heart_amount  # commented to default to 1 until its chapter logic is finished
    },
    { name: I.BLUE_PURE_HEART
    , code: 773
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    # , amount: heart_amount  # commented to default to 1 until its chapter logic is finished
    },
    { name: I.PURPLE_PURE_HEART
    , code: 774
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    # , amount: heart_amount  # commented to default to 1 until its chapter logic is finished
    },
    { name: I.WHITE_PURE_HEART
    , code: 775
    , classification: ItemClassification.progression_skip_balancing
    , groups: {GROUP_HEART}
    # , amount: heart_amount  # commented to default to 1 until its chapter logic is finished
    },
    { name: I.ABILITY_FLIP
    , code: 776
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.ABILITY_UMBRELLA
    , code: 777
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.ABILITY_FIRE
    , code: 778
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.ABILITY_SUPER_JUMP
    , code: 779
    , classification: ItemClassification.progression
    , groups: {GROUP_ABILITY}
    , amount: ability_amount
    },
    { name: I.CHAPTER_1_KEY
    , code: 780
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_2_KEY
    , code: 781
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_3_KEY
    , code: 782
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_4_KEY
    , code: 783
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_5_KEY
    , code: 784
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_6_KEY
    , code: 785
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_7_KEY
    , code: 786
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_8_KEY
    , code: 787
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY,GROUP_CHAPTER_KEY}
    , amount: chapter_key_amount
    },
    { name: I.CHAPTER_1_1_KEY
    , code: 788
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_1_2_KEY
    , code: 789
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_1_3_KEY
    , code: 790
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_1_4_KEY
    , code: 791
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_1_KEY
    , code: 792
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_2_KEY
    , code: 793
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_3_KEY
    , code: 794
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_2_4_KEY
    , code: 795
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_1_KEY
    , code: 796
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_2_KEY
    , code: 797
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_3_KEY
    , code: 798
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_3_4_KEY
    , code: 799
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_1_KEY
    , code: 800
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_2_KEY
    , code: 801
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_3_KEY
    , code: 802
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_4_4_KEY
    , code: 803
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_1_KEY
    , code: 804
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_2_KEY
    , code: 805
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_3_KEY
    , code: 806
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_5_4_KEY
    , code: 807
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_1_KEY
    , code: 808
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_2_KEY
    , code: 809
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_3_KEY
    , code: 810
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_6_4_KEY
    , code: 811
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_1_KEY
    , code: 812
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_2_KEY
    , code: 813
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_3_KEY
    , code: 814
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_7_4_KEY
    , code: 815
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_1_KEY
    , code: 816
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_2_KEY
    , code: 817
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_3_KEY
    , code: 818
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.CHAPTER_8_4_KEY
    , code: 819
    , classification: ItemClassification.progression
    , groups: {GROUP_TOWER_KEY, GROUP_SUBCHAPTER_KEY}
    , amount: subchapter_key_amount
    },
    { name: I.SLOW_CURSYA_TRAP
    , code: 820
    , classification: ItemClassification.trap
    , groups: {GROUP_CURSYA_TRAP}
    },
    { name: I.HEAVY_CURSYA_TRAP
    , code: 821
    , classification: ItemClassification.trap
    , groups: {GROUP_CURSYA_TRAP}
    },
    { name: I.REVERSYA_CURSYA_TRAP
    , code: 822
    , classification: ItemClassification.trap
    , groups: {GROUP_CURSYA_TRAP}
    },
    { name: I.TECH_CURSYA_TRAP
    , code: 823
    , classification: ItemClassification.trap
    , groups: {GROUP_CURSYA_TRAP}
    },
    { name: I.BACK_CURSYA_TRAP
    , code: 824
    , classification: ItemClassification.trap
    , groups: {GROUP_CURSYA_TRAP}
    },
    #endregion
]  # fmt: skip

ITEM_DATA = [ItemData(**data) for data in ITEM_LIST_DICT]
