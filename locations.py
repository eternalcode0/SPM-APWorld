from dataclasses import dataclass

from .constants import SPMEvent, SPMItem, SPMLocation
from .flags import ScriptVariable, GSW, GSWF


BASE_LOCATION_ID = 4_998_000


@dataclass
class LocData:
    code: int
    """A unique id among all other SPM locations. Gets added to BASE_LOCATION_ID."""
    rom: int
    """Where do we write the randomized item to to change what gets picked up?"""
    var: ScriptVariable
    """Which game variable is set when this location is checked?
    https://github.com/SeekyCt/spm-docs/wiki/GSWF"""
    vanilla_item: str
    """What SPMItem is normally at this location"""


###
# WARNING: ALL LOCATION IDS STILL SUBJECT TO CHANGE, DO NOT REFERENCE THESE
###
location_table: dict[str, LocData] = {
    # Heart Pillars
    SPMLocation.FLIPSIDE_HEART_PILLAR_RED: LocData(1, 0, GSW(0, 8), SPMItem.CHAPTER_1_1_KEY),
    SPMLocation.FLIPSIDE_HEART_PILLAR_ORANGE: LocData(2, 0, GSW(0, 65), SPMItem.CHAPTER_2_1_KEY),
    SPMLocation.FLIPSIDE_HEART_PILLAR_YELLOW: LocData(3, 0, GSW(0, 100), SPMItem.CHAPTER_3_1_KEY),
    SPMLocation.FLIPSIDE_HEART_PILLAR_GREEN: LocData(4, 0, GSW(0, 128), SPMItem.CHAPTER_4_1_KEY),
    SPMLocation.FLOPSIDE_HEART_PILLAR_CYAN: LocData(5, 0, GSW(0, 177), SPMItem.CHAPTER_5_1_KEY),
    SPMLocation.FLOPSIDE_HEART_PILLAR_BLUE: LocData(6, 0, GSW(0, 224), SPMItem.CHAPTER_6_1_KEY),
    SPMLocation.FLOPSIDE_HEART_PILLAR_PURPLE: LocData(7, 0, GSW(0, 303), SPMItem.CHAPTER_7_1_KEY),
    SPMLocation.FLOPSIDE_HEART_PILLAR_WHITE: LocData(8, 0, GSW(0, 356), SPMItem.CHAPTER_8_1_KEY),

    # Shop locations, I don't know if the vanilla items are listed in the correct order
    SPMLocation.FLIPSIDE_HOWZITS_1: LocData(9, 0, None, SPMItem.SHROOM_SHAKE),
    SPMLocation.FLIPSIDE_HOWZITS_2: LocData(10, 0, None, SPMItem.LONG_LAST_SHAKE),
    SPMLocation.FLIPSIDE_HOWZITS_3: LocData(11, 0, None, SPMItem.LIFE_SHROOM),
    SPMLocation.FLIPSIDE_HOWZITS_4: LocData(12, 0, None, SPMItem.FIRE_BURST),
    SPMLocation.FLIPSIDE_HOWZITS_5: LocData(13, 0, None, SPMItem.ICE_STORM),
    SPMLocation.FLIPSIDE_HOWZITS_6: LocData(14, 0, None, SPMItem.SLEEPY_SHEEP),
    SPMLocation.FLIPSIDE_HOWZITS_7: LocData(15, 0, None, SPMItem.COURAGE_SHELL),
    SPMLocation.FLIPSIDE_HOWZITS_8: LocData(16, 0, None, SPMItem.SHELL_SHOCK),
    SPMLocation.FLIPSIDE_HOWZITS_9: LocData(17, 0, None, SPMItem.STAR_MEDAL),
    SPMLocation.FLIPSIDE_HOWZITS_10: LocData(18, 0, None, SPMItem.GOLD_BAR),
    SPMLocation.FLIPSIDE_ITTY_BITS_1: LocData(19, 0, None, SPMItem.HONEY_JAR),
    SPMLocation.FLIPSIDE_ITTY_BITS_2: LocData(20, 0, None, SPMItem.BIG_EGG),
    SPMLocation.FLIPSIDE_ITTY_BITS_3: LocData(21, 0, None, SPMItem.CAKE_MIX),
    SPMLocation.FLOPSIDE_NOTSOS_1: LocData(22, 0, None, SPMItem.VOLT_SHROOM),
    SPMLocation.FLOPSIDE_NOTSOS_2: LocData(23, 0, None, SPMItem.BLOCK_BLOCK),
    SPMLocation.FLOPSIDE_NOTSOS_3: LocData(24, 0, None, SPMItem.STOP_WATCH),
    SPMLocation.FLOPSIDE_NOTSOS_4: LocData(25, 0, None, SPMItem.MIGHTY_TONIC),
    SPMLocation.FLOPSIDE_NOTSOS_5: LocData(26, 0, None, SPMItem.SUPER_SHROOM_SHAKE),
    SPMLocation.FLOPSIDE_NOTSOS_6: LocData(27, 0, None, SPMItem.THUNDER_RAGE),
    SPMLocation.FLOPSIDE_NOTSOS_7: LocData(28, 0, None, SPMItem.GHOST_SHROOM),
    SPMLocation.FLOPSIDE_NOTSOS_8: LocData(29, 0, None, SPMItem.ULTRA_SHROOM_SHAKE),
    SPMLocation.FLOPSIDE_NOTSOS_9: LocData(30, 0, None, SPMItem.GOLD_BAR_X3),
    SPMLocation.FLOPSIDE_NOTSOS_10: LocData(31, 0, None, SPMItem.GOLD_MEDAL),
    SPMLocation.FLOPSIDE_ITTY_BITS_1: LocData(32, 0, None, SPMItem.FRESH_PASTA_BUNCH),
    SPMLocation.FLOPSIDE_ITTY_BITS_2: LocData(33, 0, None, SPMItem.POWER_STEAK),
    SPMLocation.FLOPSIDE_ITTY_BITS_3: LocData(34, 0, None, SPMItem.SMELLY_HERB),
    SPMLocation.YOLD_TOWN_HOWZITS_1: LocData(35, 0, None, SPMItem.FIRE_BURST),
    SPMLocation.YOLD_TOWN_HOWZITS_2: LocData(36, 0, None, SPMItem.POW_BLOCK),
    SPMLocation.YOLD_TOWN_HOWZITS_3: LocData(37, 0, None, SPMItem.SHROOM_SHAKE),
    SPMLocation.YOLD_TOWN_HOWZITS_4: LocData(38, 0, None, SPMItem.LONG_LAST_SHAKE),
    SPMLocation.YOLD_TOWN_HOWZITS_5: LocData(39, 0, None, SPMItem.LIFE_SHROOM),
    SPMLocation.YOLD_TOWN_HOWZITS_6: LocData(40, 0, None, SPMItem.SLEEPY_SHEEP),
    SPMLocation.YOLD_TOWN_HOWZITS_7: LocData(41, 0, None, SPMItem.SHELL_SHOCK),
    SPMLocation.YOLD_TOWN_HOWZITS_8: LocData(42, 0, None, SPMItem.MIGHTY_TONIC),
    SPMLocation.YOLD_TOWN_HOWZITS_9: LocData(43, 0, None, SPMItem.COURAGE_SHELL),
    SPMLocation.YOLD_TOWN_HOWZITS_10: LocData(44, 0, None, SPMItem.VOLT_SHROOM),
    SPMLocation.DOTWOOD_TREE_ITTY_BITS_1: LocData(45, 0, None, SPMItem.FRESH_VEGGIE),
    SPMLocation.DOTWOOD_TREE_ITTY_BITS_2: LocData(46, 0, None, SPMItem.HORSETAIL),
    SPMLocation.DOTWOOD_TREE_ITTY_BITS_3: LocData(47, 0, None, SPMItem.PEACHY_PEACH),
    SPMLocation.OUTER_LIMITS_HOWZITS_TWINKLE_MART_1: LocData(48, 0, None, SPMItem.GOLDEN_CHOCO_BAR),
    SPMLocation.OUTER_LIMITS_HOWZITS_TWINKLE_MART_2: LocData(49, 0, None, SPMItem.SHROOM_CHOCO_BAR),
    SPMLocation.OUTER_LIMITS_HOWZITS_TWINKLE_MART_3: LocData(50, 0, None, SPMItem.SWEET_CHOCO_BAR),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_1: LocData(51, 0, None, SPMItem.COURAGE_SHELL),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_2: LocData(52, 0, None, SPMItem.FIRE_BURST),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_3: LocData(53, 0, None, SPMItem.ICE_STORM),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_4: LocData(54, 0, None, SPMItem.LIFE_SHROOM),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_5: LocData(55, 0, None, SPMItem.MYSTERY_BOX),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_6: LocData(56, 0, None, SPMItem.POW_BLOCK),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_7: LocData(57, 0, None, SPMItem.PRIMORDIAL_FRUIT),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_8: LocData(58, 0, None, SPMItem.SHROOM_SHAKE),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_9: LocData(59, 0, None, SPMItem.SLEEPY_SHEEP),
    SPMLocation.DOWNTOWN_CRAG_HOWZITS_10: LocData(60, 0, None, SPMItem.SUPER_SHROOM_SHAKE),
    SPMLocation.DOWNTOWN_CRAG_ITTY_BITS_1: LocData(61, 0, None, SPMItem.KEEL_MANGO),
    SPMLocation.DOWNTOWN_CRAG_ITTY_BITS_2: LocData(62, 0, None, SPMItem.MILD_COCOA_BEAN),
    SPMLocation.THE_OVERTHERE_ITTY_BITS_1: LocData(63, 0, None, SPMItem.HOT_DOG),
    SPMLocation.THE_OVERTHERE_ITTY_BITS_2: LocData(64, 0, None, SPMItem.HOT_SAUCE),

    SPMLocation.FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK: LocData(65, 0, GSWF(527), SPMItem.CATCH_CARD_MERLEE),
    SPMLocation.FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS: LocData(66, 0, GSWF(580), SPMItem.COOKING_DISK_R),
    SPMLocation.FLIPSIDE_B2_CHEST_AFTER_PIPE: LocData(67, 0, GSWF(503), SPMItem.HP_PLUS),
    SPMLocation.FLIPSIDE_1F_OUTSKIRTS_LEFT_CHEST_IN_HOLE: LocData(68, 0, GSWF(523), SPMItem.CATCH_CARD_MERLON),
    SPMLocation.FLIPSIDE_1F_OUTSKIRTS_RIGHT_CHEST_IN_HOLE: LocData(69, 0, GSWF(522), SPMItem.CATCH_CARD_MERLUVLEE),

    SPMLocation.FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK: LocData(70, 0, GSWF(529), SPMItem.CATCH_CARD_NOLREM),
    SPMLocation.FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS: LocData(71, 0, GSWF(581), SPMItem.COOKING_DISK_W),
    SPMLocation.FLOPSIDE_B2_CHEST_AFTER_PIPE: LocData(72, 0, GSWF(506), SPMItem.POWER_PLUS),
    SPMLocation.FLOPSIDE_B2_CHASM_CHEST: LocData(73, 0, GSWF(525), SPMItem.CATCH_CARD_BARRY),
    SPMLocation.FLOPSIDE_B1_BEVERAGARIUM_CHEST1: LocData(74, 0, GSWF(537), SPMItem.GOLDEN_CARD),
    SPMLocation.FLOPSIDE_B1_BEVERAGARIUM_CHEST2: LocData(75, 0, GSWF(583), SPMItem.COOKING_DISK_B),
    SPMLocation.FLOPSIDE_B1_OUTSKIRT_CHEST_BEHIND_PILLAR: LocData(76, 0, GSWF(524), SPMItem.CATCH_CARD_PICCOLO),

    # Piccolo Fetch Quest
    SPMLocation.PICCOLO_FETCH_WATCHITT_1: LocData(77, 0, GSWF(413), SPMItem.PAPER),
    SPMLocation.PICCOLO_FETCH_MERLUMINA: LocData(78, 0, GSWF(414), SPMItem.AUTOGRAPH),
    SPMLocation.PICCOLO_FETCH_WATCHITT_2: LocData(79, 0, GSWF(415), SPMItem.YOU_KNOW_WHAT),
    SPMLocation.PICCOLO_FETCH_BESTOVIUS: LocData(80, 0, GSWF(416), SPMItem.TRAINING_MACHINE),
    SPMLocation.PICCOLO_FETCH_MERLUVLEE: LocData(81, 0, GSWF(417), SPMItem.CRYSTAL_BALL),
    SPMLocation.PICCOLO_FETCH_MERLEE: LocData(82, 0, GSWF(418), SPMItem.RANDOM_HOUSE_KEY),
    SPMLocation.PICCOLO_FETCH_END: LocData(83, 0, GSWF(517), SPMItem.PIXL_PICCOLO),

    # Flipside Pit
    SPMLocation.FLIPSIDE_PIT_10: LocData(84, 0, GSWF(433), SPMItem.CATCH_CARD_TIPPI),
    SPMLocation.FLIPSIDE_PIT_20: LocData(85, 0, GSWF(434), SPMItem.CATCH_CARD_THOREAU),
    SPMLocation.FLIPSIDE_PIT_30: LocData(86, 0, GSWF(435), SPMItem.CATCH_CARD_BOOMER),
    SPMLocation.FLIPSIDE_PIT_40: LocData(87, 0, GSWF(436), SPMItem.CATCH_CARD_SLIM),
    SPMLocation.FLIPSIDE_PIT_50: LocData(88, 0, GSWF(437), SPMItem.CATCH_CARD_THUDLEY),
    SPMLocation.FLIPSIDE_PIT_60: LocData(89, 0, GSWF(438), SPMItem.CATCH_CARD_CARRIE),
    SPMLocation.FLIPSIDE_PIT_70: LocData(90, 0, GSWF(439), SPMItem.CATCH_CARD_FLEEP),
    SPMLocation.FLIPSIDE_PIT_80: LocData(91, 0, GSWF(440), SPMItem.CATCH_CARD_CUDGE),
    SPMLocation.FLIPSIDE_PIT_90: LocData(92, 0, GSWF(441), SPMItem.CATCH_CARD_DOTTIE),
    SPMLocation.FLIPSIDE_PIT_100: LocData(93, 0, GSWF(389), SPMItem.PIXL_DASHELL),  # 2 flags for wracktail? 389/409
    SPMLocation.FLIPSIDE_PIT_WRACKTAIL: LocData(None, 0, GSWF(408), SPMEvent.COMPLETED_FLIPSIDE_PIT),

    # Flopside Pit
    SPMLocation.FLOPSIDE_PIT_10: LocData(94, 0, GSWF(442), SPMItem.CATCH_CARD_DASHELL),
    SPMLocation.FLOPSIDE_PIT_20: LocData(95, 0, GSWF(443), SPMItem.CATCH_CARD_GOOMBARIO),
    SPMLocation.FLOPSIDE_PIT_30: LocData(96, 0, GSWF(444), SPMItem.CATCH_CARD_KOOPER),
    SPMLocation.FLOPSIDE_PIT_40: LocData(97, 0, GSWF(445), SPMItem.CATCH_CARD_BOMBETTE),
    SPMLocation.FLOPSIDE_PIT_50: LocData(98, 0, GSWF(446), SPMItem.CATCH_CARD_PARAKARRY),
    SPMLocation.FLOPSIDE_PIT_60: LocData(99, 0, GSWF(447), SPMItem.CATCH_CARD_BOW),
    SPMLocation.FLOPSIDE_PIT_70: LocData(100, 0, GSWF(448), SPMItem.CATCH_CARD_WATT),
    SPMLocation.FLOPSIDE_PIT_80: LocData(101, 0, GSWF(449), SPMItem.CATCH_CARD_SUSHIE),
    SPMLocation.FLOPSIDE_PIT_90: LocData(102, 0, GSWF(450), SPMItem.CATCH_CARD_LAKILESTER),
    SPMLocation.FLOPSIDE_PIT_100_1: LocData(103, 0, None, SPMItem.CATCH_CARD_MARIO),
    SPMLocation.FLOPSIDE_PIT_100_2: LocData(104, 0, None, SPMItem.CATCH_CARD_DARK_MARIO),
    SPMLocation.FLOPSIDE_PIT_100_3: LocData(105, 0, None, SPMItem.CATCH_CARD_PEACH_1),
    SPMLocation.FLOPSIDE_PIT_100_4: LocData(106, 0, None, SPMItem.CATCH_CARD_DARK_PEACH),
    SPMLocation.FLOPSIDE_PIT_100_5: LocData(107, 0, None, SPMItem.CATCH_CARD_BOWSER_1),
    SPMLocation.FLOPSIDE_PIT_100_6: LocData(108, 0, None, SPMItem.CATCH_CARD_DARK_BOWSER),
    SPMLocation.FLOPSIDE_PIT_100_7: LocData(109, 0, None, SPMItem.CATCH_CARD_LUIGI),
    SPMLocation.FLOPSIDE_PIT_100_8: LocData(110, 0, None, SPMItem.CATCH_CARD_DARK_LUIGI),
    SPMLocation.FLOPSIDE_PIT_SHADOO: LocData(None, 0, None, SPMEvent.COMPLETED_FLOPSIDE_PIT),

    # region Chapter 1
    # 1-1
    SPMLocation.C11_OPEN_ITEM_BEHIND_PIPE: LocData(111, 0, GSWF(603), SPMItem.CATCH_CARD_GOOMBA),
    SPMLocation.C11_CHEST_AFTER_STAR_BLOCK: LocData(112, 0, GSWF(604), SPMItem.CATCH_CARD_KOOPA_TROOPA),
    SPMLocation.C11_OPEN_ITEM_ABOVE_BESTOVIUS_HOUSE: LocData(113, 0, GSWF(611), SPMItem.CATCH_CARD_SQUIGLET),
    SPMLocation.C11_CHEST_INSIDE_FIRST_PIPE: LocData(114, 0, GSWF(612), SPMItem.SHROOM_SHAKE),
    SPMLocation.C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM: LocData(115, 0, GSWF(614), SPMItem.SHELL_SHOCK),
    SPMLocation.C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY: LocData(116, 0, GSWF(615), SPMItem.FIRE_BURST),
    SPMLocation.C11_TALK_TO_BESTOVIUS: LocData(117, 0, GSW(0, 16), SPMItem.ABILITY_FLIP),
    SPMLocation.C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM: LocData(118, 0, GSWF(616), SPMItem.SHROOM_SHAKE),
    SPMLocation.C11_STAR_BLOCK: LocData(119, 0, GSW(0, 17), SPMItem.CHAPTER_1_2_KEY),

    # 1-2
    SPMLocation.C12_THOREAU_CHEST: LocData(120, 0, GSW(0, 25), SPMItem.PIXL_THOREAU),
    SPMLocation.C12_CHEST_IN_SHORTCUT: LocData(121, 0, GSWF(605), SPMItem.CATCH_CARD_PARATROOPA),
    SPMLocation.C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE: LocData(122, 0, GSWF(610), SPMItem.CATCH_CARD_BOOMBOXER),
    SPMLocation.C12_OPEN_ITEM_BEHIND_GREENS_BED: LocData(123, 0, GSWF(618), SPMItem.CATCH_CARD_RED_GREEN),
    SPMLocation.C12_STAR_BLOCK: LocData(124, 0, GSW(0, 28), SPMItem.CHAPTER_1_3_KEY),

    # 1-3
    SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM: LocData(125, 0, GSWF(606), SPMItem.CATCH_CARD_SQUIG),
    SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM: LocData(126, 0, GSWF(607), SPMItem.COURAGE_SHELL),
    SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM: LocData(127, 0, GSWF(608), SPMItem.GHOST_SHROOM),
    SPMLocation.C13_STAR_BLOCK: LocData(128, 0, GSW(0, 38), SPMItem.CHAPTER_1_4_KEY),

    # 1-4
    SPMLocation.C14_CHEST_IN_SECOND_ROOM: LocData(129, 0, GSWF(609), SPMItem.LIFE_SHROOM),
    SPMLocation.C14_CHEST_IN_SMALL_SPIKY_TROMP_ROOM: LocData(130, 0, GSW(0, 40), SPMItem.RUINS_KEY),
    SPMLocation.C14_OPEN_KEY_BEHIND_BLOCKS: LocData(131, 0, GSW(0, 43), SPMItem.RUINS_KEY),
    SPMLocation.C14_HIDDEN_CHEST_AFTER_3D_PATH: LocData(132, 0, GSWF(613), SPMItem.CATCH_CARD_BUZZY_BEETLE),
    SPMLocation.C14_OPEN_KEY_BETWEEN_FIRE_BARS: LocData(133, 0, GSW(0, 46), SPMItem.RUINS_KEY),
    SPMLocation.C14_ORANGE_PURE_HEART: LocData(134, 0, GSW(0, 53), SPMItem.ORANGE_PURE_HEART),
    # endregion

    # region Chapter 2
    # TODO: verify all script variables & items
    SPMLocation.C21_CHEST_AFTER_SQUIGS: LocData(135, None, None, None),
    SPMLocation.C21_BOOMER_CHEST: LocData(136, None, None, None),
    SPMLocation.C21_CHEST_BEHIND_BOOMER_CHEST: LocData(137, None, None, None),
    SPMLocation.C21_LEFT_CHEST_BEFORE_STAR_BLOCK: LocData(138, None, None, None),
    SPMLocation.C21_RIGHT_CHEST_BEFORE_STAR_BLOCK: LocData(139, None, None, None),
    SPMLocation.C21_STAR_BLOCK: LocData(140, None, None, None),

    SPMLocation.C22_CHEST_ABOVE_ENTRANCE: LocData(141, None, None, None),
    SPMLocation.C22_CHEST_ON_ROOF: LocData(142, None, None, None),
    SPMLocation.C22_OPEN_ITEM_DRAGGED_BY_ROPE: LocData(143, None, None, None),
    SPMLocation.C22_OPEN_ITEM_HUNG_BY_ROPE: LocData(144, None, None, None),
    SPMLocation.C22_CHEST_ABOVE_SPIKE_ROOF: LocData(145, None, None, None),
    SPMLocation.C22_STAR_BLOCK: LocData(146, None, None, None),

    SPMLocation.C23_CHEST_BEHIND_BLOCKS: LocData(147, None, None, None),
    SPMLocation.C23_SLIM_CHEST: LocData(148, None, None, None),
    SPMLocation.C23_STAR_BLOCK: LocData(149, None, None, None),

    SPMLocation.C24_OPEN_ITEM_BEHIND_ROOM_08_SIGN: LocData(150, None, None, None),
    SPMLocation.C24_YELLOW_PURE_HEART: LocData(151, None, None, None),
    # endregion

    # region Chapter 3
    SPMLocation.C31_TALK_TO_BARRY_AFTER_DEFEATING_FRANCIS: LocData(152, None, None, None),
    SPMLocation.C31_CHEST_IN_WARP_ZONE_RIGHT_PIPE: LocData(153, None, None, None),
    SPMLocation.C31_OPEN_ITEM_IN_BACKGROUND: LocData(154, None, None, None),
    SPMLocation.C31_CHEST_IN_BACKGROUND_PIPE: LocData(155, None, None, None),
    SPMLocation.C31_CHEST_ABOVE_COLORFUL_PERSONS: LocData(156, None, None, None),
    SPMLocation.C31_OPEN_ITEM_IN_BACKGROUND_2: LocData(157, None, None, None),
    SPMLocation.C31_BOWSER: LocData(158, None, None, None),
    SPMLocation.C31_STAR_BLOCK: LocData(159, None, None, None),

    SPMLocation.C32_HIDDEN_CHEST_NEAR_PIPE: LocData(160, None, None, None),
    SPMLocation.C32_THUDLEY_CHEST: LocData(161, None, None, None),
    SPMLocation.C32_STAR_BLOCK: LocData(162, None, None, None),

    SPMLocation.C33_CHOMPS_CHEST: LocData(163, None, None, None),
    SPMLocation.C33_STAR_BLOCK: LocData(164, None, None, None),

    SPMLocation.C34_CHEST_IN_PIPE_OUTSIDE_OF_CASTLE: LocData(165, None, None, None),
    SPMLocation.C34_FREE_CARRIE: LocData(166, None, None, None),
    SPMLocation.C34_RIGHT_FRANCIS_CHAMBER_CHEST: LocData(167, None, None, None),
    SPMLocation.C34_LEFT_FRANCIS_CHAMBER_CHEST: LocData(168, None, None, None),
    SPMLocation.C34_GREEN_PURE_HEART: LocData(169, None, None, None),
    # endregion

    # region Chapter 4
    SPMLocation.C41_SQUIRPS: LocData(170, None, None, None),  # randomize squirps maybe?
    SPMLocation.C41_OPEN_ITEM_BEHIND_ASTEROID_1: LocData(171, None, None, None),
    SPMLocation.C41_OPEN_ITEM_BEHIND_ASTEROID_2: LocData(172, None, None, None),
    SPMLocation.C41_STAR_BLOCK: LocData(173, None, None, None),

    SPMLocation.C42_FLIP_THE_DIMENSIONAL_RIFT: LocData(174, None, None, None),
    SPMLocation.C42_OPEN_ITEM_IN_CHASM_3_D: LocData(175, None, None, None),
    SPMLocation.C42_OPEN_ITEM_BEHIND_PIPE_NEAR_BLAPPYS_HOUSE: LocData(176, None, None, None),
    SPMLocation.C42_TALK_TO_BLAPPY: LocData(177, None, None, None),
    SPMLocation.C42_FLEEP: LocData(178, None, None, None),
    SPMLocation.C42_STAR_BLOCK: LocData(179, None, None, None),

    SPMLocation.C43_OPEN_ITEM_BEHIND_FIRST_BLOCKS: LocData(180, None, None, None),
    SPMLocation.C43_OPEN_ITEM_BEHIND_BLOCKS_IN_MANY_WORMHOLE_ROOM: LocData(181, None, None, None),
    SPMLocation.C43_VISIBLE_OPEN_ITEM_IN_BLOCKS: LocData(182, None, None, None),
    SPMLocation.C43_STAR_BLOCK: LocData(183, None, None, None),

    SPMLocation.C44_CHEST_NEAR_BARRIBAD: LocData(184, None, None, None),
    SPMLocation.C44_CHEST_ABOVE_LOCKED_DOOR: LocData(185, None, None, None),
    SPMLocation.C44_CHEST_IN_3_BLOCK_ROOM: LocData(186, None, None, None),
    SPMLocation.C44_BLUE_PURE_HEART: LocData(187, None, None, None),
    # endregion

    # region Chapter 5
    SPMLocation.C51_CHEST_NEAR_WHACKA: LocData(188, None, None, None),
    SPMLocation.C51_CHEST_AFTER_SHLORPS: LocData(189, None, None, None),
    SPMLocation.C51_CHEST_IN_CHASM_3_D: LocData(190, None, None, None),
    SPMLocation.C51_STAR_BLOCK: LocData(191, None, None, None),

    SPMLocation.C52_FIRE_TABLET: LocData(192, None, None, None),
    SPMLocation.C52_OPEN_ITEM_IN_BACKGROUND: LocData(193, None, None, None),
    SPMLocation.C52_OPEN_ITEM_IN_FRONT_OF_PIPE: LocData(194, None, None, None),
    SPMLocation.C52_STONE_TABLET: LocData(195, None, None, None),
    SPMLocation.C52_WATER_TABLET: LocData(196, None, None, None),
    SPMLocation.C52_CUDGE: LocData(197, None, None, None),
    SPMLocation.C52_CHEST_NEAR_STAR_BLOCK: LocData(198, None, None, None),
    SPMLocation.C52_STAR_BLOCK: LocData(199, None, None, None),

    SPMLocation.C53_OPEN_ITEM_IN_CAVE: LocData(200, None, None, None),
    SPMLocation.C53_SAVE_CRAGLEY_S_CREW: LocData(201, None, None, None),
    SPMLocation.C53_STAR_BLOCK: LocData(202, None, None, None),

    SPMLocation.C54_DOTTIE: LocData(203, None, None, None),
    SPMLocation.C54_OPEN_ITEM_NEAR_PROCESSING_CENTER: LocData(204, None, None, None),
    SPMLocation.C54_OPEN_ITEM_BEHIND_PIPE: LocData(205, None, None, None),
    SPMLocation.C54_FLIP_THE_SKULL: LocData(206, None, None, None),
    SPMLocation.C54_DEFEAT_FLORO_CHUNKS: LocData(207, None, None, None),
    SPMLocation.C54_INDIGO_PURE_HEART: LocData(208, None, None, None),
    # endregion

    # region Chapter 6
    # TODO: how to randomize chapter 6? There's only a single check before post-game
    SPMLocation.C61_PETRIFIED_PURE_HEART: LocData(209, None, None, None),
    SPMLocation.C61_STAR_BLOCK: LocData(210, None, None, None),

    SPMLocation.C62_STAR_BLOCK: LocData(211, None, None, None),

    SPMLocation.C63_STAR_BLOCK: LocData(212, None, None, None),

    SPMLocation.C64_SAMMER_KING_REWARD_1: LocData(213, None, None, None),
    SPMLocation.C64_SAMMER_KING_REWARD_2: LocData(214, None, None, None),
    SPMLocation.C64_SAMMER_KING_REWARD_3: LocData(215, None, None, None),
    SPMLocation.C64_SAMMER_KING_REWARD_4: LocData(216, None, None, None),
    SPMLocation.C64_SAMMER_KING_REWARD_5: LocData(217, None, None, None),
    SPMLocation.C64_SAMMER_KING_REWARD_6: LocData(218, None, None, None),
    SPMLocation.C64_SAMMER_KING_REWARD_7: LocData(219, None, None, None),
    SPMLocation.C64_STAR_BLOCK: LocData(220, None, None, None),
    # endregion

    # region Chapter 7
    SPMLocation.C71_CHEST_AFTER_GIGABYTE: LocData(221, None, None, None),
    SPMLocation.C71_OPEN_ITEM_ABOVE_PIPE: LocData(222, None, None, None),
    SPMLocation.C71_GIVE_THE_PETRIFIED_PURE_HEART_TO_JAYDES: LocData(223, None, None, None),
    SPMLocation.C71_LUIGI: LocData(224, None, None, None),
    SPMLocation.C71_HIDDEN_OPEN_ITEM_NEAR_LUIGI: LocData(225, None, None, None),
    SPMLocation.C71_HIDDEN_CHEST_IN_LUIGI_S_ROOM: LocData(226, None, None, None),
    SPMLocation.C71_STAR_BLOCK: LocData(227, None, None, None),

    SPMLocation.C72_CHEST_IN_FIRST_DARK_ROOM: LocData(228, None, None, None),
    SPMLocation.C72_DEFEAT_BOWSER: LocData(229, None, None, None),
    SPMLocation.C72_TALK_TO_HAGRA_AND_GET_THE_BOOK_FROM_THE_D_MAN: LocData(230, None, None, None),
    SPMLocation.C72_BRING_THE_DIET_BOOK_TO_HAGRA: LocData(231, None, None, None),
    SPMLocation.C72_STAR_BLOCK: LocData(232, None, None, None),

    SPMLocation.C73_CHEST_RIGHT_OF_25: LocData(233, None, None, None),
    SPMLocation.C73_CHEST_AT_34: LocData(234, None, None, None),
    SPMLocation.C73_CHEST_LEFT_OF_47: LocData(235, None, None, None),
    SPMLocation.C73_WAKE_PEACH_UP: LocData(236, None, None, None),
    SPMLocation.C73_CHEST_AT_68: LocData(237, None, None, None),
    SPMLocation.C73_CHEST_RIGHT_OF_69: LocData(238, None, None, None),
    SPMLocation.C73_CHEST_RIGHT_OF_CYRRUS: LocData(239, None, None, None),
    SPMLocation.C73_CHEST_ATOP_BUILDING_AT_80: LocData(240, None, None, None),
    SPMLocation.C73_CHEST_BEHIND_STAR_BLOCK: LocData(241, None, None, None),
    SPMLocation.C73_STAR_BLOCK: LocData(242, None, None, None),

    SPMLocation.C74_SAVE_SUNBI: LocData(243, None, None, None),
    SPMLocation.C74_CHEST_AFTER_GIGABYTE: LocData(244, None, None, None),
    SPMLocation.C74_FREE_WHIBBI: LocData(245, None, None, None),
    SPMLocation.C74_TALK_TO_YEBBI: LocData(246, None, None, None),
    SPMLocation.C74_OPEN_ITEM_ABOVE_TWO_DOORS: LocData(247, None, None, None),
    SPMLocation.C74_TALK_TO_REBBI: LocData(248, None, None, None),
    SPMLocation.C74_BIG_CHEST_BELOW_REBBI: LocData(249, None, None, None),
    SPMLocation.C74_TALK_TO_BLUBI_AFTER_WHIBBI: LocData(250, None, None, None),
    SPMLocation.C74_CHEST_BEHIND_STAIRS: LocData(251, None, None, None),
    SPMLocation.C74_CHEST_FAR_RIGHT_OF_MELEE: LocData(252, None, None, None),
    SPMLocation.C74_WHITE_PURE_HEART: LocData(253, None, None, None),
    # endregion

    # region Chapter 8
    SPMLocation.C81_RIGHT_CHEST_ABOVE_PEACH_CUTSCENE_START: LocData(254, None, None, None),
    SPMLocation.C81_LEFT_CHEST_ABOVE_PEACH_CUTSCENE_START: LocData(255, None, None, None),
    SPMLocation.C81_CHEST_IN_SOOPA_STRIKER_HALLWAY: LocData(256, None, None, None),

    SPMLocation.C82_LEFT_CHEST_ABOVE_MERLON_ROOM: LocData(257, None, None, None),
    SPMLocation.C82_MIDDLE_CHEST_ABOVE_MERLON_ROOM: LocData(258, None, None, None),
    SPMLocation.C82_RIGHT_CHEST_ABOVE_MERLON_ROOM: LocData(259, None, None, None),
    SPMLocation.C82_OPEN_ITEM_BEHIND_5TH_PIPE: LocData(260, None, None, None),
    SPMLocation.C82_CHEST_IN_CURSYA_ROOM: LocData(261, None, None, None),
    SPMLocation.C82_FIRST_HUNG_ITEM: LocData(262, None, None, None),
    SPMLocation.C82_SECOND_HUNG_ITEM: LocData(263, None, None, None),
    SPMLocation.C82_THIRD_HUNG_ITEM: LocData(264, None, None, None),
    SPMLocation.C82_DEFEAT_THE_CHROMEBA: LocData(265, None, None, None),
    SPMLocation.C82_MERLEES_THUNDER_RAGE: LocData(266, None, None, None),

    SPMLocation.C83_RIGHT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS: LocData(267, None, None, None),
    SPMLocation.C83_LEFT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS: LocData(268, None, None, None),
    SPMLocation.C83_CHEST_AFTER_BLOCK_PUZZLE: LocData(269, None, None, None),
    SPMLocation.C83_RIGHT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS: LocData(270, None, None, None),
    SPMLocation.C83_LEFT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS: LocData(271, None, None, None),

    SPMLocation.C84_CHEST_AFTER_TINY_PASSAGE: LocData(272, None, None, None),
    SPMLocation.C84_CHEST_IN_FIRST_3_D_HALLWAYS: LocData(273, None, None, None),
    SPMLocation.C84_CHEST_IN_SECOND_3_D_HALLWAYS: LocData(274, None, None, None),
    SPMLocation.C84_CHEST_IN_THIRD_3_D_HALLWAYS: LocData(275, None, None, None),
    # endregion

    # New location to represent the Pure Heart Merlin gives you at the start of the game
    SPMLocation.FLIPSIDE_MERLONS_GIFT: LocData(276, None, None, SPMItem.RED_PURE_HEART),
}

location_groups: dict[str, set[str]] = {
    "Flipside Pit": {SPMLocation.FLIPSIDE_PIT_10, SPMLocation.FLIPSIDE_PIT_20, SPMLocation.FLIPSIDE_PIT_30,
                     SPMLocation.FLIPSIDE_PIT_40, SPMLocation.FLIPSIDE_PIT_50, SPMLocation.FLIPSIDE_PIT_60,
                     SPMLocation.FLIPSIDE_PIT_70, SPMLocation.FLIPSIDE_PIT_80, SPMLocation.FLIPSIDE_PIT_90,
                     SPMLocation.FLIPSIDE_PIT_100},
    "Flopside Pit": {SPMLocation.FLOPSIDE_PIT_10, SPMLocation.FLOPSIDE_PIT_20, SPMLocation.FLOPSIDE_PIT_30,
                     SPMLocation.FLOPSIDE_PIT_40, SPMLocation.FLOPSIDE_PIT_50, SPMLocation.FLOPSIDE_PIT_60,
                     SPMLocation.FLOPSIDE_PIT_70, SPMLocation.FLOPSIDE_PIT_80, SPMLocation.FLOPSIDE_PIT_90,
                     SPMLocation.FLOPSIDE_PIT_100_1, SPMLocation.FLOPSIDE_PIT_100_2, SPMLocation.FLOPSIDE_PIT_100_3,
                     SPMLocation.FLOPSIDE_PIT_100_4, SPMLocation.FLOPSIDE_PIT_100_5, SPMLocation.FLOPSIDE_PIT_100_6,
                     SPMLocation.FLOPSIDE_PIT_100_7, SPMLocation.FLOPSIDE_PIT_100_8},
    "Pit": {SPMLocation.FLIPSIDE_PIT_10, SPMLocation.FLIPSIDE_PIT_20, SPMLocation.FLIPSIDE_PIT_30,
            SPMLocation.FLIPSIDE_PIT_40, SPMLocation.FLIPSIDE_PIT_50, SPMLocation.FLIPSIDE_PIT_60,
            SPMLocation.FLIPSIDE_PIT_70, SPMLocation.FLIPSIDE_PIT_80, SPMLocation.FLIPSIDE_PIT_90,
            SPMLocation.FLIPSIDE_PIT_100,
            SPMLocation.FLOPSIDE_PIT_10, SPMLocation.FLOPSIDE_PIT_20, SPMLocation.FLOPSIDE_PIT_30,
            SPMLocation.FLOPSIDE_PIT_40, SPMLocation.FLOPSIDE_PIT_50, SPMLocation.FLOPSIDE_PIT_60,
            SPMLocation.FLOPSIDE_PIT_70, SPMLocation.FLOPSIDE_PIT_80, SPMLocation.FLOPSIDE_PIT_90,
            SPMLocation.FLOPSIDE_PIT_100_1, SPMLocation.FLOPSIDE_PIT_100_2, SPMLocation.FLOPSIDE_PIT_100_3,
            SPMLocation.FLOPSIDE_PIT_100_4, SPMLocation.FLOPSIDE_PIT_100_5, SPMLocation.FLOPSIDE_PIT_100_6,
            SPMLocation.FLOPSIDE_PIT_100_7, SPMLocation.FLOPSIDE_PIT_100_8}
}
