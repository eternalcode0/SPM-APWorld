"""Defines the set of game items and item pools"""
from dataclasses import dataclass
import typing

from BaseClasses import ItemClassification

from .constants import SPMItem, SPMLocation, SuperPaperMarioItem
from .options import ChapterKeysLock

if typing.TYPE_CHECKING:
    from . import SuperPaperMarioWorld


@dataclass
class ItemData:
    """Core item data to be used internally within the apworld only, not given to AP's internals"""
    classification: ItemClassification
    """The *default* item classification, this may be overridden by the pool"""
    code: int
    """The in-game item id"""


CHARACTERS = [
    SPMItem.CHARACTER_MARIO,
    SPMItem.CHARACTER_PEACH,
    SPMItem.CHARACTER_BOWSER,
    SPMItem.CHARACTER_LUIGI]
PIXLS = [
    SPMItem.PIXL_TIPPI,
    SPMItem.PIXL_THOREAU,
    SPMItem.PIXL_BOOMER,
    SPMItem.PIXL_SLIM,
    SPMItem.PIXL_THUDLEY,
    SPMItem.PIXL_CARRIE,
    SPMItem.PIXL_FLEEP,
    SPMItem.PIXL_CUDGE,
    SPMItem.PIXL_DOTTIE,
    SPMItem.PIXL_BARRY,
    SPMItem.PIXL_DASHELL,
    SPMItem.PIXL_PICCOLO]
CHAPTER_KEYS = [
    SPMItem.CHAPTER_1_KEY,
    SPMItem.CHAPTER_2_KEY,
    SPMItem.CHAPTER_3_KEY,
    SPMItem.CHAPTER_4_KEY,
    SPMItem.CHAPTER_5_KEY,
    SPMItem.CHAPTER_6_KEY,
    SPMItem.CHAPTER_7_KEY,
    SPMItem.CHAPTER_8_KEY]
SUBCHAPTER_KEYS = [
    SPMItem.CHAPTER_1_1_KEY,
    SPMItem.CHAPTER_1_2_KEY,
    SPMItem.CHAPTER_1_3_KEY,
    SPMItem.CHAPTER_1_4_KEY,
    SPMItem.CHAPTER_2_1_KEY,
    SPMItem.CHAPTER_2_2_KEY,
    SPMItem.CHAPTER_2_3_KEY,
    SPMItem.CHAPTER_2_4_KEY,
    SPMItem.CHAPTER_3_1_KEY,
    SPMItem.CHAPTER_3_2_KEY,
    SPMItem.CHAPTER_3_3_KEY,
    SPMItem.CHAPTER_3_4_KEY,
    SPMItem.CHAPTER_4_1_KEY,
    SPMItem.CHAPTER_4_2_KEY,
    SPMItem.CHAPTER_4_3_KEY,
    SPMItem.CHAPTER_4_4_KEY,
    SPMItem.CHAPTER_5_1_KEY,
    SPMItem.CHAPTER_5_2_KEY,
    SPMItem.CHAPTER_5_3_KEY,
    SPMItem.CHAPTER_5_4_KEY,
    SPMItem.CHAPTER_6_1_KEY,
    SPMItem.CHAPTER_6_2_KEY,
    SPMItem.CHAPTER_6_3_KEY,
    SPMItem.CHAPTER_6_4_KEY,
    SPMItem.CHAPTER_7_1_KEY,
    SPMItem.CHAPTER_7_2_KEY,
    SPMItem.CHAPTER_7_3_KEY,
    SPMItem.CHAPTER_7_4_KEY,
    SPMItem.CHAPTER_8_1_KEY,
    SPMItem.CHAPTER_8_2_KEY,
    SPMItem.CHAPTER_8_3_KEY,
    SPMItem.CHAPTER_8_4_KEY]

item_table = {
    # # Important Things
    # There are 3 Ruins Keys but unlike other keys, only one item id, instead these are use the sequence value
    SPMItem.RUINS_KEY: ItemData(ItemClassification.progression, 16),
    # SPMItem.DOOR_KEY_21: ItemData(ItemClassification.progression, 17),
    # SPMItem.HOUSE_KEY: ItemData(ItemClassification.progression, 18),
    # There are 3 Fort Keys all with the same name/description but diff ids. Can these be combined?
    SPMItem.FORT_KEY: ItemData(ItemClassification.progression, 19),
    # SPMItem.FORT_KEY: ItemData(ItemClassification.progression, 20),
    # SPMItem.FORT_KEY: ItemData(ItemClassification.progression, 21),
    # SPMItem.GOLDFISH_BOWL_FISH: ItemData(ItemClassification.progression, 22),
    # SPMItem.GOLDFISH_BOWL_EMPTY: ItemData(ItemClassification.progression, 23),
    # SPMItem.HELMET: ItemData(ItemClassification.progression, 24),
    # SPMItem.ANCIENT_CLUE: ItemData(ItemClassification.progression, 25),
    # SPMItem.DOOR_KEY_42: ItemData(ItemClassification.progression, 26),
    # Same deal as For Keys, 3 of them but diff ids.
    SPMItem.DIMENSION_KEY: ItemData(ItemClassification.progression, 27),
    # SPMItem.DIMENSION_KEY: ItemData(ItemClassification.progression, 28),
    # SPMItem.DIMENSION_KEY: ItemData(ItemClassification.progression, 29),
    # SPMItem.WATER_TABLET: ItemData(ItemClassification.progression, 30),
    # SPMItem.STONE_TABLET: ItemData(ItemClassification.progression, 31),
    # SPMItem.FIRE_TABLET: ItemData(ItemClassification.progression, 32),
    # SPMItem.CAVE_KEY_53: ItemData(ItemClassification.progression, 33),
    # SPMItem.CAVE_KEY_54: ItemData(ItemClassification.progression, 34),
    # SPMItem.CARD_KEY: ItemData(ItemClassification.progression, 35),
    # SPMItem.FLORO_SPROUT: ItemData(ItemClassification.progression, 36),
    # SPMItem.DOOR_KEY_71: ItemData(ItemClassification.progression, 37),
    # SPMItem.DOOR_KEY_72: ItemData(ItemClassification.progression, 38),
    # SPMItem.DIET_BOOK: ItemData(ItemClassification.progression, 39),
    # SPMItem.DOOR_KEY_74: ItemData(ItemClassification.progression, 40),
    # SPMItem.BLUE_ORB: ItemData(ItemClassification.progression, 41),
    # SPMItem.YELLOW_ORB: ItemData(ItemClassification.progression, 42),
    # SPMItem.RED_ORB: ItemData(ItemClassification.progression, 43),
    # # (ItemClassification.progression, 44),  # Pit Key
    # # (ItemClassification.progression, 45),  # Unavailable Item (Peach sprite)
    # # (ItemClassification.progression, 46),  # Castle Bleck Key
    SPMItem.OLD_KEY: ItemData(ItemClassification.progression, 47),
    # # (ItemClassification.progression, 48),  # Pit Key
    # # (ItemClassification.progression, 49),  # Door Key
    # # (ItemClassification.progression, 50),  # Return Pipe
    SPMItem.CRYSTAL_BALL: ItemData(ItemClassification.progression, 51),
    SPMItem.TRAINING_MACHINE: ItemData(ItemClassification.progression, 52),
    SPMItem.YOU_KNOW_WHAT: ItemData(ItemClassification.progression, 53),
    SPMItem.PAPER: ItemData(ItemClassification.progression, 54),
    SPMItem.AUTOGRAPH: ItemData(ItemClassification.progression, 55),
    SPMItem.RANDOM_HOUSE_KEY: ItemData(ItemClassification.progression, 56),
    # SPMItem.COOKING_DISK_R: ItemData(ItemClassification.filler, 57),
    # SPMItem.COOKING_DISK_W: ItemData(ItemClassification.filler, 58),
    # SPMItem.COOKING_DISK_Y: ItemData(ItemClassification.filler, 59),
    # SPMItem.COOKING_DISK_B: ItemData(ItemClassification.filler, 60),
    # SPMItem.COOKING_DISK_G: ItemData(ItemClassification.filler, 61),
    # SPMItem.COOKING_DISK_PU: ItemData(ItemClassification.filler, 62),
    # # (ItemClassification.progression, 63),  # Cooking Disk PI
    # SPMItem.GOLDEN_CARD: ItemData(ItemClassification.filler, 64),

    # Usable Items
    SPMItem.FIRE_BURST: ItemData(ItemClassification.filler, 65),
    SPMItem.ICE_STORM: ItemData(ItemClassification.filler, 66),
    SPMItem.THUNDER_RAGE: ItemData(ItemClassification.filler, 67),
    SPMItem.SHOOTING_STAR: ItemData(ItemClassification.filler, 68),
    SPMItem.POW_BLOCK: ItemData(ItemClassification.filler, 69),
    SPMItem.SHELL_SHOCK: ItemData(ItemClassification.filler, 70),
    SPMItem.GOLD_BAR: ItemData(ItemClassification.filler, 71),
    SPMItem.GOLD_BAR_X3: ItemData(ItemClassification.filler, 72),
    SPMItem.BLOCK_BLOCK: ItemData(ItemClassification.filler, 73),
    SPMItem.COURAGE_SHELL: ItemData(ItemClassification.filler, 74),
    SPMItem.MIGHTY_TONIC: ItemData(ItemClassification.filler, 75),
    SPMItem.VOLT_SHROOM: ItemData(ItemClassification.filler, 76),
    SPMItem.GHOST_SHROOM: ItemData(ItemClassification.filler, 77),
    SPMItem.SLEEPY_SHEEP: ItemData(ItemClassification.filler, 78),
    SPMItem.STOP_WATCH: ItemData(ItemClassification.filler, 79),
    SPMItem.SHROOM_SHAKE: ItemData(ItemClassification.filler, 80),
    SPMItem.SUPER_SHROOM_SHAKE: ItemData(ItemClassification.filler, 81),
    SPMItem.ULTRA_SHROOM_SHAKE: ItemData(ItemClassification.filler, 82),
    SPMItem.DRIED_SHROOM: ItemData(ItemClassification.filler, 83),
    SPMItem.LIFE_SHROOM: ItemData(ItemClassification.filler, 84),
    SPMItem.LONG_LAST_SHAKE: ItemData(ItemClassification.filler, 85),
    SPMItem.MYSTERY_BOX: ItemData(ItemClassification.filler, 86),
    SPMItem.CATCH_CARD: ItemData(ItemClassification.filler, 87),
    SPMItem.CATCH_CARD_SP: ItemData(ItemClassification.filler, 88),
    SPMItem.HP_PLUS: ItemData(ItemClassification.filler, 89),
    SPMItem.POWER_PLUS: ItemData(ItemClassification.filler, 90),
    SPMItem.BLUE_APPLE: ItemData(ItemClassification.filler, 91),
    SPMItem.YELLOW_APPLE: ItemData(ItemClassification.filler, 92),
    SPMItem.RED_APPLE: ItemData(ItemClassification.filler, 93),
    SPMItem.PINK_APPLE: ItemData(ItemClassification.filler, 94),
    SPMItem.BLACK_APPLE: ItemData(ItemClassification.filler, 95),
    SPMItem.STAR_MEDAL: ItemData(ItemClassification.filler, 96),
    SPMItem.GOLD_MEDAL: ItemData(ItemClassification.filler, 97),
    SPMItem.POISON_SHROOM: ItemData(ItemClassification.filler, 98),
    SPMItem.SLIMY_SHROOM: ItemData(ItemClassification.filler, 99),
    SPMItem.PEACHY_PEACH: ItemData(ItemClassification.filler, 100),
    SPMItem.KEEL_MANGO: ItemData(ItemClassification.filler, 101),
    SPMItem.PRIMORDIAL_FRUIT: ItemData(ItemClassification.filler, 102),
    SPMItem.GOLDEN_LEAF: ItemData(ItemClassification.filler, 103),
    SPMItem.TURTLEY_LEAF: ItemData(ItemClassification.filler, 104),
    SPMItem.CAKE_MIX: ItemData(ItemClassification.filler, 105),
    SPMItem.WHACKA_BUMP: ItemData(ItemClassification.filler, 106),
    SPMItem.HORSETAIL: ItemData(ItemClassification.filler, 107),
    SPMItem.FRESH_PASTA_BUNCH: ItemData(ItemClassification.filler, 108),
    SPMItem.HOT_SAUCE: ItemData(ItemClassification.filler, 109),
    SPMItem.INKY_SAUCE: ItemData(ItemClassification.filler, 110),
    SPMItem.DAYZEE_TEAR: ItemData(ItemClassification.filler, 111),
    SPMItem.SAP_SOUP: ItemData(ItemClassification.filler, 112),
    SPMItem.BONE_IN_CUT: ItemData(ItemClassification.filler, 113),
    SPMItem.FRESH_VEGGIE: ItemData(ItemClassification.filler, 114),
    SPMItem.SMELLY_HERB: ItemData(ItemClassification.filler, 115),
    SPMItem.HONEY_JAR: ItemData(ItemClassification.filler, 116),
    SPMItem.POWER_STEAK: ItemData(ItemClassification.filler, 117),
    SPMItem.BIG_EGG: ItemData(ItemClassification.filler, 118),
    SPMItem.MILD_COCOA_BEAN: ItemData(ItemClassification.filler, 119),
    SPMItem.SWEET_CHOCO_BAR: ItemData(ItemClassification.filler, 120),
    SPMItem.SHROOM_CHOCO_BAR: ItemData(ItemClassification.filler, 121),
    SPMItem.GOLDEN_CHOCO_BAR: ItemData(ItemClassification.filler, 122),
    SPMItem.GRADUAL_SYRUP: ItemData(ItemClassification.filler, 123),
    SPMItem.DAYZEE_SYRUP: ItemData(ItemClassification.filler, 124),
    SPMItem.SLIMY_EXTRACT: ItemData(ItemClassification.filler, 125),
    SPMItem.FRIED_SHROOM_PLATE: ItemData(ItemClassification.filler, 126),
    SPMItem.ROAST_SHROOM_DISH: ItemData(ItemClassification.filler, 127),
    SPMItem.SHROOM_STEAK: ItemData(ItemClassification.filler, 128),
    SPMItem.HONEY_SHROOM: ItemData(ItemClassification.filler, 129),
    SPMItem.HONEY_SUPER: ItemData(ItemClassification.filler, 130),
    SPMItem.SHROOM_BROTH: ItemData(ItemClassification.filler, 131),
    SPMItem.MUSHROOM_CREPE: ItemData(ItemClassification.filler, 132),
    SPMItem.SHROOM_CAKE: ItemData(ItemClassification.filler, 133),
    SPMItem.CHOCOLATE_CAKE: ItemData(ItemClassification.filler, 134),
    SPMItem.HEARTFUL_CAKE: ItemData(ItemClassification.filler, 135),
    SPMItem.MOUSSE: ItemData(ItemClassification.filler, 136),
    SPMItem.PEACH_TART: ItemData(ItemClassification.filler, 137),
    SPMItem.HORSETAIL_TART: ItemData(ItemClassification.filler, 138),
    SPMItem.SWEET_COOKIE_SNACK: ItemData(ItemClassification.filler, 139),
    SPMItem.KOOPA_DUMPLING: ItemData(ItemClassification.filler, 140),
    SPMItem.SAP_MUFFIN: ItemData(ItemClassification.filler, 141),
    SPMItem.TOWN_SPECIAL: ItemData(ItemClassification.filler, 142),
    SPMItem.MANGO_PUDDING: ItemData(ItemClassification.filler, 143),
    SPMItem.LOVE_PUDDING: ItemData(ItemClassification.filler, 144),
    SPMItem.COUPLES_CAKE: ItemData(ItemClassification.filler, 145),
    SPMItem.FRUIT_PARFAIT: ItemData(ItemClassification.filler, 146),
    SPMItem.SNOW_CONE: ItemData(ItemClassification.filler, 147),
    SPMItem.SNOW_BUNNY: ItemData(ItemClassification.filler, 148),
    SPMItem.BERRY_SNOW_BUNNY: ItemData(ItemClassification.filler, 149),
    SPMItem.HONEY_CANDY: ItemData(ItemClassification.filler, 150),
    SPMItem.ELECTRO_POP: ItemData(ItemClassification.filler, 151),
    SPMItem.HERB_TEA: ItemData(ItemClassification.filler, 152),
    SPMItem.KOOPA_TEA: ItemData(ItemClassification.filler, 153),
    SPMItem.SPAGHETTI_PLATE: ItemData(ItemClassification.filler, 154),
    SPMItem.SPICY_PASTA_DISH: ItemData(ItemClassification.filler, 155),
    SPMItem.INK_PASTA_DISH: ItemData(ItemClassification.filler, 156),
    SPMItem.KOOPASTA_DISH: ItemData(ItemClassification.filler, 157),
    SPMItem.LOVE_NOODLE_DISH: ItemData(ItemClassification.filler, 158),
    SPMItem.FRIED_EGG: ItemData(ItemClassification.filler, 159),
    SPMItem.EGG_BOMB: ItemData(ItemClassification.filler, 160),
    SPMItem.DYLLIS_DYNAMITE: ItemData(ItemClassification.filler, 161),
    SPMItem.SPIT_ROAST: ItemData(ItemClassification.filler, 162),
    SPMItem.METEOR_MEAL: ItemData(ItemClassification.filler, 163),
    SPMItem.OMELETTE_PLATE: ItemData(ItemClassification.filler, 164),
    SPMItem.SPICY_SOUP: ItemData(ItemClassification.filler, 165),
    SPMItem.HOT_DOG: ItemData(ItemClassification.filler, 166),
    SPMItem.HEALTHY_SALAD: ItemData(ItemClassification.filler, 167),
    SPMItem.DYLLIS_DINNER: ItemData(ItemClassification.filler, 168),
    SPMItem.DYLLIS_SPECIAL: ItemData(ItemClassification.filler, 169),
    SPMItem.DYLLIS_DELUXE: ItemData(ItemClassification.filler, 170),
    SPMItem.SPACE_FOOD: ItemData(ItemClassification.filler, 171),
    SPMItem.EMERGENCY_RATION: ItemData(ItemClassification.filler, 172),
    SPMItem.DANGEROUS_DELIGHT: ItemData(ItemClassification.filler, 173),
    SPMItem.TRIAL_STEW: ItemData(ItemClassification.filler, 174),
    SPMItem.MISTAKE: ItemData(ItemClassification.filler, 175),
    SPMItem.MISTAKE_SLEEPY_SHEEP: ItemData(ItemClassification.filler, 176),
    SPMItem.WARM_COCOA: ItemData(ItemClassification.filler, 177),
    SPMItem.ODD_DINNER: ItemData(ItemClassification.filler, 178),
    SPMItem.INKY_SOUP: ItemData(ItemClassification.filler, 179),
    SPMItem.GINGERBREAD_HOUSE: ItemData(ItemClassification.filler, 180),
    SPMItem.VOLCANO_SHROOM: ItemData(ItemClassification.filler, 181),
    SPMItem.KOOPA_PILAF: ItemData(ItemClassification.filler, 182),
    SPMItem.SPICY_DINNER: ItemData(ItemClassification.filler, 183),
    SPMItem.SHROOM_PUDDING: ItemData(ItemClassification.filler, 184),
    SPMItem.HEAVY_MEAL: ItemData(ItemClassification.filler, 185),
    SPMItem.PRIMORDIAL_DINNER: ItemData(ItemClassification.filler, 186),
    SPMItem.GORGEOUS_STEAK: ItemData(ItemClassification.filler, 187),
    SPMItem.GOLDEN_MEAL: ItemData(ItemClassification.filler, 188),
    SPMItem.LUXURIOUS_SET: ItemData(ItemClassification.filler, 189),
    SPMItem.ROAST_WHACKA_BUMP: ItemData(ItemClassification.filler, 190),
    SPMItem.DYLLIS_BREAKFAST: ItemData(ItemClassification.filler, 191),
    SPMItem.DYLLIS_LUNCH: ItemData(ItemClassification.filler, 192),
    SPMItem.SKY_JUICE: ItemData(ItemClassification.filler, 193),
    SPMItem.STAMINA_JUICE: ItemData(ItemClassification.filler, 194),
    SPMItem.CHOCO_PASTA_DISH: ItemData(ItemClassification.filler, 195),
    SPMItem.SHROOM_DELICACY: ItemData(ItemClassification.filler, 196),
    SPMItem.ROAST_HORSETAIL: ItemData(ItemClassification.filler, 197),
    SPMItem.SAP_SYRUP: ItemData(ItemClassification.filler, 198),
    SPMItem.HAMBURGER: ItemData(ItemClassification.filler, 199),
    SPMItem.PEACH_JUICE: ItemData(ItemClassification.filler, 200),
    SPMItem.STANDARD_CHOCOLATE: ItemData(ItemClassification.filler, 201),
    SPMItem.FRUITY_CAKE: ItemData(ItemClassification.filler, 202),
    SPMItem.FRUITY_HAMBURGER: ItemData(ItemClassification.filler, 203),
    SPMItem.FRUITY_PUNCH: ItemData(ItemClassification.filler, 204),
    SPMItem.FRUITY_SHROOM: ItemData(ItemClassification.filler, 205),
    SPMItem.BLOCK_MEAL: ItemData(ItemClassification.filler, 206),
    SPMItem.VEGGIE_SET: ItemData(ItemClassification.filler, 207),
    SPMItem.WEIRD_EXTRACT: ItemData(ItemClassification.filler, 208),
    SPMItem.AWESOME_SNACK: ItemData(ItemClassification.filler, 209),
    SPMItem.MANGO_JUICE: ItemData(ItemClassification.filler, 210),
    SPMItem.MEAT_PASTA_DISH: ItemData(ItemClassification.filler, 211),
    SPMItem.MIXED_SHAKE: ItemData(ItemClassification.filler, 212),
    SPMItem.MIRACLE_DINNER: ItemData(ItemClassification.filler, 213),
    SPMItem.MEGATON_DINNER: ItemData(ItemClassification.filler, 214),
    SPMItem.LOVELY_CHOCOLATE: ItemData(ItemClassification.filler, 215),

    SPMItem.CHARACTER_MARIO: ItemData(ItemClassification.progression, 216),
    SPMItem.CHARACTER_PEACH: ItemData(ItemClassification.progression, 217),
    SPMItem.CHARACTER_BOWSER: ItemData(ItemClassification.progression, 218),
    SPMItem.CHARACTER_LUIGI: ItemData(ItemClassification.progression, 219),

    SPMItem.PIXL_TIPPI: ItemData(ItemClassification.progression, 220),
    SPMItem.PIXL_THOREAU: ItemData(ItemClassification.progression, 221),
    SPMItem.PIXL_BOOMER: ItemData(ItemClassification.progression, 222),
    SPMItem.PIXL_SLIM: ItemData(ItemClassification.progression, 223),
    SPMItem.PIXL_THUDLEY: ItemData(ItemClassification.progression, 224),
    SPMItem.PIXL_CARRIE: ItemData(ItemClassification.progression, 225),
    SPMItem.PIXL_FLEEP: ItemData(ItemClassification.progression, 226),
    SPMItem.PIXL_CUDGE: ItemData(ItemClassification.progression, 227),
    SPMItem.PIXL_DOTTIE: ItemData(ItemClassification.progression, 228),
    SPMItem.PIXL_PICCOLO: ItemData(ItemClassification.progression, 229),
    SPMItem.PIXL_BARRY: ItemData(ItemClassification.useful, 230),
    SPMItem.PIXL_DASHELL: ItemData(ItemClassification.useful, 231),

    # AP Items, these use made up item ids since they don't exist in-game
    SPMItem.RED_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 232),
    SPMItem.ORANGE_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 233),
    SPMItem.YELLOW_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 234),
    SPMItem.GREEN_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 235),
    SPMItem.CYAN_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 236),
    SPMItem.BLUE_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 237),
    SPMItem.PURPLE_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 238),
    SPMItem.WHITE_PURE_HEART: ItemData(ItemClassification.progression_skip_balancing, 239),
    SPMItem.ABILITY_FLIP: ItemData(ItemClassification.progression, 240),
    # SPMItem.ABILITY_UMBRELLA: ItemData(ItemClassification.progression, 241),
    # SPMItem.ABILITY_FIRE: ItemData(ItemClassification.progression, 242),
    # SPMItem.ABILITY_SUPER_JUMP: ItemData(ItemClassification.progression, 243),

    SPMItem.CHAPTER_1_KEY: ItemData(ItemClassification.progression, 244),
    SPMItem.CHAPTER_2_KEY: ItemData(ItemClassification.progression, 245),
    SPMItem.CHAPTER_3_KEY: ItemData(ItemClassification.progression, 246),
    SPMItem.CHAPTER_4_KEY: ItemData(ItemClassification.progression, 247),
    SPMItem.CHAPTER_5_KEY: ItemData(ItemClassification.progression, 248),
    SPMItem.CHAPTER_6_KEY: ItemData(ItemClassification.progression, 249),
    SPMItem.CHAPTER_7_KEY: ItemData(ItemClassification.progression, 250),
    SPMItem.CHAPTER_8_KEY: ItemData(ItemClassification.progression, 251),

    SPMItem.CHAPTER_1_1_KEY: ItemData(ItemClassification.progression, 252),
    SPMItem.CHAPTER_1_2_KEY: ItemData(ItemClassification.progression, 253),
    SPMItem.CHAPTER_1_3_KEY: ItemData(ItemClassification.progression, 254),
    SPMItem.CHAPTER_1_4_KEY: ItemData(ItemClassification.progression, 255),
    # hopefully the item ids aren't a single byte
    SPMItem.CHAPTER_2_1_KEY: ItemData(ItemClassification.progression, 256),
    SPMItem.CHAPTER_2_2_KEY: ItemData(ItemClassification.progression, 257),
    SPMItem.CHAPTER_2_3_KEY: ItemData(ItemClassification.progression, 258),
    SPMItem.CHAPTER_2_4_KEY: ItemData(ItemClassification.progression, 259),
    SPMItem.CHAPTER_3_1_KEY: ItemData(ItemClassification.progression, 260),
    SPMItem.CHAPTER_3_2_KEY: ItemData(ItemClassification.progression, 261),
    SPMItem.CHAPTER_3_3_KEY: ItemData(ItemClassification.progression, 262),
    SPMItem.CHAPTER_3_4_KEY: ItemData(ItemClassification.progression, 263),
    SPMItem.CHAPTER_4_1_KEY: ItemData(ItemClassification.progression, 264),
    SPMItem.CHAPTER_4_2_KEY: ItemData(ItemClassification.progression, 265),
    SPMItem.CHAPTER_4_3_KEY: ItemData(ItemClassification.progression, 266),
    SPMItem.CHAPTER_4_4_KEY: ItemData(ItemClassification.progression, 267),
    SPMItem.CHAPTER_5_1_KEY: ItemData(ItemClassification.progression, 268),
    SPMItem.CHAPTER_5_2_KEY: ItemData(ItemClassification.progression, 269),
    SPMItem.CHAPTER_5_3_KEY: ItemData(ItemClassification.progression, 270),
    SPMItem.CHAPTER_5_4_KEY: ItemData(ItemClassification.progression, 271),
    SPMItem.CHAPTER_6_1_KEY: ItemData(ItemClassification.progression, 272),
    SPMItem.CHAPTER_6_2_KEY: ItemData(ItemClassification.progression, 273),
    SPMItem.CHAPTER_6_3_KEY: ItemData(ItemClassification.progression, 274),
    SPMItem.CHAPTER_6_4_KEY: ItemData(ItemClassification.progression, 275),
    SPMItem.CHAPTER_7_1_KEY: ItemData(ItemClassification.progression, 276),
    SPMItem.CHAPTER_7_2_KEY: ItemData(ItemClassification.progression, 277),
    SPMItem.CHAPTER_7_3_KEY: ItemData(ItemClassification.progression, 278),
    SPMItem.CHAPTER_7_4_KEY: ItemData(ItemClassification.progression, 279),
    SPMItem.CHAPTER_8_1_KEY: ItemData(ItemClassification.progression, 280),
    SPMItem.CHAPTER_8_2_KEY: ItemData(ItemClassification.progression, 281),
    SPMItem.CHAPTER_8_3_KEY: ItemData(ItemClassification.progression, 282),
    SPMItem.CHAPTER_8_4_KEY: ItemData(ItemClassification.progression, 283),

    SPMItem.SLOW_CURSYA_TRAP: ItemData(ItemClassification.trap, 284),
    SPMItem.HEAVY_CURSYA_TRAP: ItemData(ItemClassification.trap, 285),
    SPMItem.REVERSYA_CURSYA_TRAP: ItemData(ItemClassification.trap, 286),
    SPMItem.TECH_CURSYA_TRAP: ItemData(ItemClassification.trap, 287),
    SPMItem.BACK_CURSYA_TRAP: ItemData(ItemClassification.trap, 288),
}


def create_items(world: "SuperPaperMarioWorld") -> list[SuperPaperMarioItem]:
    items = []

    items.extend(world.create_item(item_name) for item_name in item_groups["Heroes"])
    items.extend(world.create_item(item_name) for item_name in item_groups["Pixls"])
    items.extend(world.create_item(item_name) for item_name in [SPMItem.ABILITY_FLIP])  # abilities rando'd?

    item_quantity = {
        SPMItem.RUINS_KEY: 3,
        SPMItem.FORT_KEY: 3,
        SPMItem.DIMENSION_KEY: 3,
        SPMItem.OLD_KEY: 1,
    }
    items.extend(world.create_item(item_name)
                 for item_name, quantity in item_quantity.items()
                 for _ in range(0, quantity))

    if world.options.chapter_keys_lock.value == ChapterKeysLock.option_chapter_locked:
        items.extend(world.create_item(item_name) for item_name in CHAPTER_KEYS)
    elif world.options.chapter_keys_lock.value == ChapterKeysLock.option_subchapters_locked:
        items.extend(world.create_item(item_name) for item_name in SUBCHAPTER_KEYS)

    if world.options.shuffle_pure_hearts.value:
        items.extend(world.create_item(item_name) for item_name in item_groups["Hearts"])
    else:
        heart_locations = {
            SPMLocation.FLIPSIDE_MERLONS_GIFT: SPMItem.RED_PURE_HEART,
            SPMLocation.C14_ORANGE_PURE_HEART: SPMItem.ORANGE_PURE_HEART,
            SPMLocation.C24_YELLOW_PURE_HEART: SPMItem.YELLOW_PURE_HEART,
            SPMLocation.C34_GREEN_PURE_HEART: SPMItem.GREEN_PURE_HEART,
            SPMLocation.C44_BLUE_PURE_HEART: SPMItem.CYAN_PURE_HEART,
            SPMLocation.C54_INDIGO_PURE_HEART: SPMItem.BLUE_PURE_HEART,
            SPMLocation.C71_GIVE_THE_PETRIFIED_PURE_HEART_TO_JAYDES: SPMItem.PURPLE_PURE_HEART,
            SPMLocation.C74_WHITE_PURE_HEART: SPMItem.WHITE_PURE_HEART,
        }
        for loc, item in heart_locations.items():
            world.get_location(loc).place_locked_item(world.create_item(item))

    # if world.options.shuffle_piccolo_fetch_quest.value:
    items.extend(world.create_item(item_name) for item_name in item_groups["Fetch"])

    return items


item_groups = {
    "Hearts": {SPMItem.RED_PURE_HEART, SPMItem.ORANGE_PURE_HEART, SPMItem.YELLOW_PURE_HEART, SPMItem.GREEN_PURE_HEART,
               SPMItem.CYAN_PURE_HEART, SPMItem.BLUE_PURE_HEART, SPMItem.PURPLE_PURE_HEART, SPMItem.WHITE_PURE_HEART},
    "Heroes": {SPMItem.CHARACTER_MARIO, SPMItem.CHARACTER_PEACH, SPMItem.CHARACTER_BOWSER, SPMItem.CHARACTER_LUIGI},
    "Pixls": {SPMItem.PIXL_TIPPI, SPMItem.PIXL_THOREAU, SPMItem.PIXL_BOOMER, SPMItem.PIXL_SLIM, SPMItem.PIXL_THUDLEY,
              SPMItem.PIXL_CARRIE, SPMItem.PIXL_FLEEP, SPMItem.PIXL_CUDGE, SPMItem.PIXL_DOTTIE, SPMItem.PIXL_BARRY,
              SPMItem.PIXL_DASHELL, SPMItem.PIXL_PICCOLO},
    "Important": {SPMItem.RUINS_KEY, SPMItem.DOOR_KEY_21, SPMItem.HOUSE_KEY, SPMItem.FORT_KEY,
                  SPMItem.GOLDFISH_BOWL_FISH, SPMItem.GOLDFISH_BOWL_EMPTY, SPMItem.HELMET, SPMItem.ANCIENT_CLUE,
                  SPMItem.DOOR_KEY_42, SPMItem.DIMENSION_KEY, SPMItem.WATER_TABLET, SPMItem.STONE_TABLET,
                  SPMItem.FIRE_TABLET, SPMItem.CAVE_KEY_53, SPMItem.CAVE_KEY_54, SPMItem.CARD_KEY, SPMItem.FLORO_SPROUT,
                  SPMItem.DOOR_KEY_71, SPMItem.DOOR_KEY_72, SPMItem.DIET_BOOK, SPMItem.DOOR_KEY_74, SPMItem.BLUE_ORB,
                  SPMItem.YELLOW_ORB, SPMItem.RED_ORB, SPMItem.CRYSTAL_BALL, SPMItem.TRAINING_MACHINE,
                  SPMItem.YOU_KNOW_WHAT, SPMItem.PAPER, SPMItem.AUTOGRAPH, SPMItem.RANDOM_HOUSE_KEY},
    "Fetch": {SPMItem.CRYSTAL_BALL, SPMItem.TRAINING_MACHINE, SPMItem.YOU_KNOW_WHAT, SPMItem.PAPER, SPMItem.AUTOGRAPH,
              SPMItem.RANDOM_HOUSE_KEY},
    # "Abilities": {SPMItem.ABILITY_FLIP, SPMItem.ABILITY_UMBRELLA, SPMItem.ABILITY_FIRE, SPMItem.ABILITY_SUPER_JUMP}
    "filler": {SPMItem.FIRE_BURST, SPMItem.ICE_STORM, SPMItem.THUNDER_RAGE, SPMItem.SHOOTING_STAR, SPMItem.POW_BLOCK, SPMItem.SHELL_SHOCK, SPMItem.GOLD_BAR, SPMItem.GOLD_BAR_X3, SPMItem.BLOCK_BLOCK, SPMItem.COURAGE_SHELL, SPMItem.MIGHTY_TONIC, SPMItem.VOLT_SHROOM, SPMItem.GHOST_SHROOM, SPMItem.SLEEPY_SHEEP, SPMItem.STOP_WATCH, SPMItem.SHROOM_SHAKE, SPMItem.SUPER_SHROOM_SHAKE, SPMItem.ULTRA_SHROOM_SHAKE, SPMItem.DRIED_SHROOM, SPMItem.LIFE_SHROOM, SPMItem.LONG_LAST_SHAKE, SPMItem.MYSTERY_BOX, SPMItem.CATCH_CARD, SPMItem.CATCH_CARD_SP, SPMItem.HP_PLUS, SPMItem.POWER_PLUS, SPMItem.BLUE_APPLE, SPMItem.YELLOW_APPLE, SPMItem.RED_APPLE, SPMItem.PINK_APPLE, SPMItem.BLACK_APPLE, SPMItem.STAR_MEDAL, SPMItem.GOLD_MEDAL, SPMItem.POISON_SHROOM, SPMItem.SLIMY_SHROOM, SPMItem.PEACHY_PEACH, SPMItem.KEEL_MANGO, SPMItem.PRIMORDIAL_FRUIT, SPMItem.GOLDEN_LEAF, SPMItem.TURTLEY_LEAF, SPMItem.CAKE_MIX, SPMItem.WHACKA_BUMP, SPMItem.HORSETAIL, SPMItem.FRESH_PASTA_BUNCH, SPMItem.HOT_SAUCE, SPMItem.INKY_SAUCE, SPMItem.DAYZEE_TEAR, SPMItem.SAP_SOUP, SPMItem.BONE_IN_CUT, SPMItem.FRESH_VEGGIE, SPMItem.SMELLY_HERB, SPMItem.HONEY_JAR, SPMItem.POWER_STEAK, SPMItem.BIG_EGG, SPMItem.MILD_COCOA_BEAN, SPMItem.SWEET_CHOCO_BAR, SPMItem.SHROOM_CHOCO_BAR, SPMItem.GOLDEN_CHOCO_BAR, SPMItem.GRADUAL_SYRUP, SPMItem.DAYZEE_SYRUP, SPMItem.SLIMY_EXTRACT, SPMItem.FRIED_SHROOM_PLATE, SPMItem.ROAST_SHROOM_DISH, SPMItem.SHROOM_STEAK, SPMItem.HONEY_SHROOM, SPMItem.HONEY_SUPER, SPMItem.SHROOM_BROTH, SPMItem.MUSHROOM_CREPE, SPMItem.SHROOM_CAKE, SPMItem.CHOCOLATE_CAKE, SPMItem.HEARTFUL_CAKE, SPMItem.MOUSSE, SPMItem.PEACH_TART, SPMItem.HORSETAIL_TART, SPMItem.SWEET_COOKIE_SNACK, SPMItem.KOOPA_DUMPLING, SPMItem.SAP_MUFFIN, SPMItem.TOWN_SPECIAL, SPMItem.MANGO_PUDDING, SPMItem.LOVE_PUDDING, SPMItem.COUPLES_CAKE, SPMItem.FRUIT_PARFAIT, SPMItem.SNOW_CONE, SPMItem.SNOW_BUNNY, SPMItem.BERRY_SNOW_BUNNY, SPMItem.HONEY_CANDY, SPMItem.ELECTRO_POP, SPMItem.HERB_TEA, SPMItem.KOOPA_TEA, SPMItem.SPAGHETTI_PLATE, SPMItem.SPICY_PASTA_DISH, SPMItem.INK_PASTA_DISH, SPMItem.KOOPASTA_DISH, SPMItem.LOVE_NOODLE_DISH, SPMItem.FRIED_EGG, SPMItem.EGG_BOMB, SPMItem.DYLLIS_DYNAMITE, SPMItem.SPIT_ROAST, SPMItem.METEOR_MEAL, SPMItem.OMELETTE_PLATE, SPMItem.SPICY_SOUP, SPMItem.HOT_DOG, SPMItem.HEALTHY_SALAD, SPMItem.DYLLIS_DINNER, SPMItem.DYLLIS_SPECIAL, SPMItem.DYLLIS_DELUXE, SPMItem.SPACE_FOOD, SPMItem.EMERGENCY_RATION, SPMItem.DANGEROUS_DELIGHT, SPMItem.TRIAL_STEW, SPMItem.MISTAKE, SPMItem.MISTAKE_SLEEPY_SHEEP, SPMItem.WARM_COCOA, SPMItem.ODD_DINNER, SPMItem.INKY_SOUP, SPMItem.GINGERBREAD_HOUSE, SPMItem.VOLCANO_SHROOM, SPMItem.KOOPA_PILAF, SPMItem.SPICY_DINNER, SPMItem.SHROOM_PUDDING, SPMItem.HEAVY_MEAL, SPMItem.PRIMORDIAL_DINNER, SPMItem.GORGEOUS_STEAK, SPMItem.GOLDEN_MEAL, SPMItem.LUXURIOUS_SET, SPMItem.ROAST_WHACKA_BUMP, SPMItem.DYLLIS_BREAKFAST, SPMItem.DYLLIS_LUNCH, SPMItem.SKY_JUICE, SPMItem.STAMINA_JUICE, SPMItem.CHOCO_PASTA_DISH, SPMItem.SHROOM_DELICACY, SPMItem.ROAST_HORSETAIL, SPMItem.SAP_SYRUP, SPMItem.HAMBURGER, SPMItem.PEACH_JUICE, SPMItem.STANDARD_CHOCOLATE, SPMItem.FRUITY_CAKE, SPMItem.FRUITY_HAMBURGER, SPMItem.FRUITY_PUNCH, SPMItem.FRUITY_SHROOM, SPMItem.BLOCK_MEAL, SPMItem.VEGGIE_SET, SPMItem.WEIRD_EXTRACT, SPMItem.AWESOME_SNACK, SPMItem.MANGO_JUICE, SPMItem.MEAT_PASTA_DISH, SPMItem.MIXED_SHAKE, SPMItem.MIRACLE_DINNER, SPMItem.MEGATON_DINNER, SPMItem.LOVELY_CHOCOLATE},
    "trap": {SPMItem.SLOW_CURSYA_TRAP, SPMItem.HEAVY_CURSYA_TRAP, SPMItem.REVERSYA_CURSYA_TRAP,
             SPMItem.TECH_CURSYA_TRAP, SPMItem.BACK_CURSYA_TRAP},
}
