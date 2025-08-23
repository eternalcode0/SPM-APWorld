import typing
from BaseClasses import Region

from .constants import ALL_REGIONS, SPMLocation, SPMRegion, SuperPaperMarioLocation
from .locations import BASE_LOCATION_ID, location_table

if typing.TYPE_CHECKING:
    from . import SuperPaperMarioWorld


def create_regions(world: "SuperPaperMarioWorld", disabled_locations: set[str]):
    """Create each region needed for the world and add it to the multiworld"""
    player = world.player
    multiworld = world.multiworld
    region_locations = get_locations(world)
    # Initialize the regions
    for region_name in ALL_REGIONS:
        r = Region(region_name, player, multiworld)
        if region_name in region_locations:
            r.add_locations({loc: location_table[loc].code + BASE_LOCATION_ID
                             for loc in region_locations[region_name]
                             if location_table[loc].code is not None
                             and location_table[loc].code != 0
                             and loc not in disabled_locations},
                            SuperPaperMarioLocation)
        multiworld.regions.append(r)


# SPMRegion -> [SPMLocation]
def get_locations(world: "SuperPaperMarioWorld") -> dict[str, list[str]]:
    """Get the list of location names per each region name"""
    return {
        # region Flipside
        SPMRegion.MAC01_LAYER1: [
            SPMLocation.FLIPSIDE_HEART_PILLAR_RED, SPMLocation.FLIPSIDE_3F_EAT_A_SPICY_SOUP,
            SPMLocation.FLIPSIDE_3F_FISHBOWL],
        SPMRegion.MAC01_LAYER2: [
            SPMLocation.FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK, SPMLocation.FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS],

        SPMRegion.MAC02_LAYER1: [
            SPMLocation.PICCOLO_FETCH_MERLUVLEE,
            SPMLocation.FLIPSIDE_HOWZITS_1, SPMLocation.FLIPSIDE_HOWZITS_2, SPMLocation.FLIPSIDE_HOWZITS_3,
            SPMLocation.FLIPSIDE_HOWZITS_4, SPMLocation.FLIPSIDE_HOWZITS_5, SPMLocation.FLIPSIDE_HOWZITS_6,
            SPMLocation.FLIPSIDE_HOWZITS_7, SPMLocation.FLIPSIDE_HOWZITS_8, SPMLocation.FLIPSIDE_HOWZITS_9,
            SPMLocation.FLIPSIDE_HOWZITS_10],
        # SPMRegion.MAC02_LAYER2: [],
        SPMRegion.MAC02_LAYER3: [SPMLocation.FLIPSIDE_HEART_PILLAR_GREEN],
        SPMRegion.MAC02_L_TOWER: [SPMLocation.FLIPSIDE_MERLONS_GIFT],

        # SPMRegion.MAC03_LAYER1: [],
        # SPMRegion.MAC03_LAYER2: [],

        SPMRegion.MAC04_LAYER1: [SPMLocation.FLIPSIDE_B1_3D_CHEST],
        SPMRegion.MAC04_ITTY_BITS: [
            SPMLocation.FLIPSIDE_ITTY_BITS_1, SPMLocation.FLIPSIDE_ITTY_BITS_2, SPMLocation.FLIPSIDE_ITTY_BITS_3],
        # SPMRegion.MAC04_ARCADE_PIPE: [],

        # SPMRegion.MAC05_LAYER1: [],
        SPMRegion.MAC05_LAYER2: [SPMLocation.FLIPSIDE_B2_CHEST_AFTER_PIPE],

        # SPMRegion.MAC06_LAYER1: [],
        SPMRegion.MAC06_LAYER2: [SPMLocation.FLIPSIDE_HEART_PILLAR_ORANGE],

        SPMRegion.MAC07_LAYER1: [SPMLocation.FLIPSIDE_B1_OUTSKIRTS_CHEST_BEHIND_PILLAR],
        SPMRegion.MAC07_LAYER2: [SPMLocation.FLIPSIDE_HEART_PILLAR_YELLOW],

        SPMRegion.MAC08: [
            SPMLocation.FLIPSIDE_1F_OUTSKIRTS_LEFT_CHEST_IN_HOLE,
            SPMLocation.FLIPSIDE_1F_OUTSKIRTS_RIGHT_CHEST_IN_HOLE],

        # SPMRegion.MAC09_LAYER1: [],
        # SPMRegion.MAC09_LAYER2: [],
        # SPMRegion.MAC09_LAYER3: [],
        # endregion

        # region Flopside
        SPMRegion.MAC11_LAYER1: [SPMLocation.FLOPSIDE_HEART_PILLAR_CYAN],
        SPMRegion.MAC11_LAYER2: [
            SPMLocation.FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK, SPMLocation.FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS],

        SPMRegion.MAC12_LAYER1: [
            SPMLocation.PICCOLO_FETCH_MERLEE,
            SPMLocation.FLOPSIDE_NOTSOS_1, SPMLocation.FLOPSIDE_NOTSOS_2, SPMLocation.FLOPSIDE_NOTSOS_3,
            SPMLocation.FLOPSIDE_NOTSOS_4, SPMLocation.FLOPSIDE_NOTSOS_5, SPMLocation.FLOPSIDE_NOTSOS_6,
            SPMLocation.FLOPSIDE_NOTSOS_7, SPMLocation.FLOPSIDE_NOTSOS_8, SPMLocation.FLOPSIDE_NOTSOS_9,
            SPMLocation.FLOPSIDE_NOTSOS_10],
        # SPMRegion.MAC12_LAYER2: [],
        SPMRegion.MAC12_LAYER3: [SPMLocation.FLOPSIDE_HEART_PILLAR_WHITE],

        # SPMRegion.MAC14_RIGHT: [],
        SPMRegion.MAC14_L_ITTY_BITS: [
            SPMLocation.FLOPSIDE_ITTY_BITS_1, SPMLocation.FLOPSIDE_ITTY_BITS_2, SPMLocation.FLOPSIDE_ITTY_BITS_3],

        # SPMRegion.MAC15_LAYER1: [],
        SPMRegion.MAC15_LAYER2: [SPMLocation.FLOPSIDE_B2_CHEST_AFTER_PIPE],

        # SPMRegion.MAC16_LAYER1: [],
        SPMRegion.MAC16_LAYER2: [SPMLocation.FLOPSIDE_HEART_PILLAR_BLUE],

        SPMRegion.MAC17_LAYER1: [SPMLocation.FLOPSIDE_B1_OUTSKIRT_CHEST_BEHIND_PILLAR],
        SPMRegion.MAC17_LAYER2: [SPMLocation.FLOPSIDE_HEART_PILLAR_PURPLE],

        SPMRegion.MAC18: [SPMLocation.FLOPSIDE_B2_CHASM_CHEST],

        SPMRegion.MAC19_LAYER1: [SPMLocation.PICCOLO_FETCH_END],
        # SPMRegion.MAC19_LAYER2: [],
        # SPMRegion.MAC19_LAYER3: [],

        SPMRegion.L_FLIPSIDE_PIT: [
            SPMLocation.FLIPSIDE_PIT_10, SPMLocation.FLIPSIDE_PIT_20, SPMLocation.FLIPSIDE_PIT_30,
            SPMLocation.FLIPSIDE_PIT_40, SPMLocation.FLIPSIDE_PIT_50, SPMLocation.FLIPSIDE_PIT_60,
            SPMLocation.FLIPSIDE_PIT_70, SPMLocation.FLIPSIDE_PIT_80, SPMLocation.FLIPSIDE_PIT_90,
            SPMLocation.FLIPSIDE_PIT_100],

        SPMRegion.L_FLOPSIDE_PIT: [
            SPMLocation.FLOPSIDE_PIT_10, SPMLocation.FLOPSIDE_PIT_20, SPMLocation.FLOPSIDE_PIT_30,
            SPMLocation.FLOPSIDE_PIT_40, SPMLocation.FLOPSIDE_PIT_50, SPMLocation.FLOPSIDE_PIT_60,
            SPMLocation.FLOPSIDE_PIT_70, SPMLocation.FLOPSIDE_PIT_80, SPMLocation.FLOPSIDE_PIT_90,
            SPMLocation.FLOPSIDE_PIT_100_1, SPMLocation.FLOPSIDE_PIT_100_2, SPMLocation.FLOPSIDE_PIT_100_3,
            SPMLocation.FLOPSIDE_PIT_100_4, SPMLocation.FLOPSIDE_PIT_100_5, SPMLocation.FLOPSIDE_PIT_100_6,
            SPMLocation.FLOPSIDE_PIT_100_7, SPMLocation.FLOPSIDE_PIT_100_8],
        # endregion

        # region Chapter 1
        SPMRegion.HE101: [
            SPMLocation.C11_OPEN_ITEM_ABOVE_BESTOVIUS_HOUSE,
            SPMLocation.C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY],
        SPMRegion.HE102: [SPMLocation.C11_OPEN_ITEM_BEHIND_PIPE],
        SPMRegion.HE103: [SPMLocation.C11_CHEST_INSIDE_FIRST_PIPE],
        SPMRegion.HE104: [],
        SPMRegion.HE105: [SPMLocation.C11_CHEST_AFTER_STAR_BLOCK, SPMLocation.C11_STAR_BLOCK],
        SPMRegion.HE106: [
            SPMLocation.C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM,
            SPMLocation.C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM,
            SPMLocation.C11_TALK_TO_BESTOVIUS],

        SPMRegion.HE201: [SPMLocation.C12_CHEST_IN_SHORTCUT],
        SPMRegion.HE202: [],
        SPMRegion.HE203: [SPMLocation.C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE, SPMLocation.C12_STAR_BLOCK],
        SPMRegion.HE204: [],
        SPMRegion.HE205: [SPMLocation.C12_OPEN_ITEM_BEHIND_GREENS_BED],
        SPMRegion.HE206: [],
        SPMRegion.HE207: [SPMLocation.C12_THOREAU_CHEST],
        SPMRegion.HE208: [],
        SPMRegion.HE209: [],

        SPMRegion.HE301: [SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM],
        SPMRegion.HE302: [SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM],
        SPMRegion.HE303: [],
        SPMRegion.HE304: [],
        SPMRegion.HE305: [],
        SPMRegion.HE306: [SPMLocation.C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM],
        SPMRegion.HE307: [],
        SPMRegion.HE308: [SPMLocation.C13_STAR_BLOCK],

        SPMRegion.HE401: [],
        SPMRegion.HE402: [SPMLocation.C14_CHEST_IN_SECOND_ROOM],
        SPMRegion.HE403: [],
        SPMRegion.HE404: [SPMLocation.C14_CHEST_IN_SMALL_SPIKY_TROMP_ROOM],
        SPMRegion.HE405: [SPMLocation.C14_OPEN_KEY_BEHIND_BLOCKS],
        SPMRegion.HE406: [],
        SPMRegion.HE407: [SPMLocation.C14_HIDDEN_CHEST_AFTER_3D_PATH, SPMLocation.C14_OPEN_KEY_BETWEEN_FIRE_BARS],
        SPMRegion.HE408: [],
        SPMRegion.HE409: [],
        SPMRegion.HE410: [],
        SPMRegion.HE411: [SPMLocation.C14_ORANGE_PURE_HEART],
        SPMRegion.HE412: [],
        # endregion

        # region Chapter 2
        SPMRegion.MI104: [
            SPMLocation.C21_LEFT_CHEST_BEFORE_STAR_BLOCK, SPMLocation.C21_RIGHT_CHEST_BEFORE_STAR_BLOCK,
            SPMLocation.C21_STAR_BLOCK],
        SPMRegion.MI105: [SPMLocation.C21_CHEST_AFTER_SQUIGS],
        SPMRegion.MI107: [SPMLocation.C21_BOOMER_CHEST, SPMLocation.C21_CHEST_BEHIND_BOOMER_CHEST],

        SPMRegion.MI201: [SPMLocation.C22_CHEST_ABOVE_ENTRANCE, SPMLocation.C22_CHEST_ON_ROOF],
        SPMRegion.MI204: [SPMLocation.C22_OPEN_ITEM_HUNG_BY_ROPE],
        SPMRegion.MI206: [SPMLocation.C22_CHEST_ABOVE_SPIKE_ROOF],
        # SPMRegion.MI207: [SPMLocation.C22_OPEN_ITEM_DRAGGED_BY_ROPE],
        SPMRegion.MI208: [SPMLocation.C22_STAR_BLOCK],
        # endregion

        # TODO: Remaining region locations
        SPMRegion.MI301: [SPMLocation.C23_CHEST_BEHIND_BLOCKS, SPMLocation.C23_SLIM_CHEST, SPMLocation.C23_STAR_BLOCK],
        SPMRegion.MI401: [SPMLocation.C24_OPEN_ITEM_BEHIND_ROOM_08_SIGN, SPMLocation.C24_YELLOW_PURE_HEART],
        SPMRegion.TA101: [SPMLocation.C31_TALK_TO_BARRY_AFTER_DEFEATING_FRANCIS, SPMLocation.C31_CHEST_IN_WARP_ZONE_RIGHT_PIPE, SPMLocation.C31_OPEN_ITEM_IN_BACKGROUND, SPMLocation.C31_CHEST_IN_BACKGROUND_PIPE, SPMLocation.C31_CHEST_ABOVE_COLORFUL_PERSONS, SPMLocation.C31_OPEN_ITEM_IN_BACKGROUND_2, SPMLocation.C31_BOWSER, SPMLocation.C31_STAR_BLOCK],
        SPMRegion.TA201: [SPMLocation.C32_HIDDEN_CHEST_NEAR_PIPE, SPMLocation.C32_THUDLEY_CHEST, SPMLocation.C32_STAR_BLOCK],
        SPMRegion.TA301: [SPMLocation.C33_CHOMPS_CHEST, SPMLocation.C33_STAR_BLOCK],
        SPMRegion.TA401: [SPMLocation.C34_CHEST_IN_PIPE_OUTSIDE_OF_CASTLE, SPMLocation.C34_FREE_CARRIE, SPMLocation.C34_RIGHT_FRANCIS_CHAMBER_CHEST, SPMLocation.C34_LEFT_FRANCIS_CHAMBER_CHEST, SPMLocation.C34_GREEN_PURE_HEART],
        SPMRegion.SP101: [SPMLocation.C41_SQUIRPS, SPMLocation.C41_OPEN_ITEM_BEHIND_ASTEROID_1, SPMLocation.C41_OPEN_ITEM_BEHIND_ASTEROID_2, SPMLocation.C41_STAR_BLOCK],
        SPMRegion.SP201: [SPMLocation.C42_FLIP_THE_DIMENSIONAL_RIFT, SPMLocation.C42_OPEN_ITEM_IN_CHASM_3_D, SPMLocation.C42_OPEN_ITEM_BEHIND_PIPE_NEAR_BLAPPYS_HOUSE, SPMLocation.C42_TALK_TO_BLAPPY, SPMLocation.C42_FLEEP, SPMLocation.C42_STAR_BLOCK],
        SPMRegion.SP301: [SPMLocation.C43_OPEN_ITEM_BEHIND_FIRST_BLOCKS, SPMLocation.C43_OPEN_ITEM_BEHIND_BLOCKS_IN_MANY_WORMHOLE_ROOM, SPMLocation.C43_VISIBLE_OPEN_ITEM_IN_BLOCKS, SPMLocation.C43_STAR_BLOCK],
        SPMRegion.SP401: [SPMLocation.C44_CHEST_NEAR_BARRIBAD, SPMLocation.C44_CHEST_ABOVE_LOCKED_DOOR, SPMLocation.C44_CHEST_IN_3_BLOCK_ROOM, SPMLocation.C44_BLUE_PURE_HEART],
        SPMRegion.GN101: [SPMLocation.C51_CHEST_NEAR_WHACKA, SPMLocation.C51_CHEST_AFTER_SHLORPS, SPMLocation.C51_CHEST_IN_CHASM_3_D, SPMLocation.C51_STAR_BLOCK],
        SPMRegion.GN201: [SPMLocation.C52_FIRE_TABLET, SPMLocation.C52_OPEN_ITEM_IN_BACKGROUND, SPMLocation.C52_OPEN_ITEM_IN_FRONT_OF_PIPE, SPMLocation.C52_STONE_TABLET, SPMLocation.C52_WATER_TABLET, SPMLocation.C52_CUDGE, SPMLocation.C52_CHEST_NEAR_STAR_BLOCK, SPMLocation.C52_STAR_BLOCK],
        SPMRegion.GN301: [SPMLocation.C53_OPEN_ITEM_IN_CAVE, SPMLocation.C53_SAVE_CRAGLEY_S_CREW, SPMLocation.C53_STAR_BLOCK],
        SPMRegion.GN401: [SPMLocation.C54_DOTTIE, SPMLocation.C54_OPEN_ITEM_NEAR_PROCESSING_CENTER, SPMLocation.C54_OPEN_ITEM_BEHIND_PIPE, SPMLocation.C54_FLIP_THE_SKULL, SPMLocation.C54_DEFEAT_FLORO_CHUNKS, SPMLocation.C54_INDIGO_PURE_HEART],
        SPMRegion.WA101: [SPMLocation.C61_PETRIFIED_PURE_HEART, SPMLocation.C61_STAR_BLOCK],
        SPMRegion.WA201: [SPMLocation.C62_STAR_BLOCK],
        SPMRegion.WA301: [SPMLocation.C63_STAR_BLOCK],
        SPMRegion.WA401: [SPMLocation.C64_SAMMER_KING_REWARD_1, SPMLocation.C64_SAMMER_KING_REWARD_2, SPMLocation.C64_SAMMER_KING_REWARD_3, SPMLocation.C64_SAMMER_KING_REWARD_4, SPMLocation.C64_SAMMER_KING_REWARD_5, SPMLocation.C64_SAMMER_KING_REWARD_6, SPMLocation.C64_SAMMER_KING_REWARD_7, SPMLocation.C64_STAR_BLOCK],
        SPMRegion.AN101: [SPMLocation.C71_CHEST_AFTER_GIGABYTE, SPMLocation.C71_OPEN_ITEM_ABOVE_PIPE, SPMLocation.C71_GIVE_THE_PETRIFIED_PURE_HEART_TO_JAYDES, SPMLocation.C71_LUIGI, SPMLocation.C71_HIDDEN_OPEN_ITEM_NEAR_LUIGI, SPMLocation.C71_HIDDEN_CHEST_IN_LUIGI_S_ROOM, SPMLocation.C71_STAR_BLOCK],
        SPMRegion.AN201: [SPMLocation.C72_CHEST_IN_FIRST_DARK_ROOM, SPMLocation.C72_DEFEAT_BOWSER, SPMLocation.C72_TALK_TO_HAGRA_AND_GET_THE_BOOK_FROM_THE_D_MAN, SPMLocation.C72_BRING_THE_DIET_BOOK_TO_HAGRA, SPMLocation.C72_STAR_BLOCK],
        SPMRegion.AN301: [SPMLocation.C73_CHEST_RIGHT_OF_25, SPMLocation.C73_CHEST_AT_34, SPMLocation.C73_CHEST_LEFT_OF_47, SPMLocation.C73_CHEST_AT_68, SPMLocation.C73_CHEST_RIGHT_OF_69, SPMLocation.C73_CHEST_RIGHT_OF_CYRRUS, SPMLocation.C73_CHEST_ATOP_BUILDING_AT_80, SPMLocation.C73_CHEST_BEHIND_STAR_BLOCK, SPMLocation.C73_STAR_BLOCK],
        SPMRegion.AN401: [SPMLocation.C74_SAVE_SUNBI, SPMLocation.C74_CHEST_AFTER_GIGABYTE, SPMLocation.C74_FREE_WHIBBI, SPMLocation.C74_TALK_TO_YEBBI, SPMLocation.C74_OPEN_ITEM_ABOVE_TWO_DOORS, SPMLocation.C74_TALK_TO_REBBI, SPMLocation.C74_BIG_CHEST_BELOW_REBBI, SPMLocation.C74_TALK_TO_BLUBI_AFTER_WHIBBI, SPMLocation.C74_CHEST_BEHIND_STAIRS, SPMLocation.C74_CHEST_FAR_RIGHT_OF_MELEE, SPMLocation.C74_WHITE_PURE_HEART],
        SPMRegion.LS101: [SPMLocation.C81_RIGHT_CHEST_ABOVE_PEACH_CUTSCENE_START, SPMLocation.C81_LEFT_CHEST_ABOVE_PEACH_CUTSCENE_START, SPMLocation.C81_CHEST_IN_SOOPA_STRIKER_HALLWAY],
        SPMRegion.LS201: [SPMLocation.C82_LEFT_CHEST_ABOVE_MERLON_ROOM, SPMLocation.C82_MIDDLE_CHEST_ABOVE_MERLON_ROOM, SPMLocation.C82_RIGHT_CHEST_ABOVE_MERLON_ROOM, SPMLocation.C82_OPEN_ITEM_BEHIND_5TH_PIPE, SPMLocation.C82_CHEST_IN_CURSYA_ROOM, SPMLocation.C82_FIRST_HUNG_ITEM, SPMLocation.C82_SECOND_HUNG_ITEM, SPMLocation.C82_THIRD_HUNG_ITEM, SPMLocation.C82_DEFEAT_THE_CHROMEBA, SPMLocation.C82_MERLEES_THUNDER_RAGE],
        SPMRegion.LS301: [SPMLocation.C83_RIGHT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS, SPMLocation.C83_LEFT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS, SPMLocation.C83_CHEST_AFTER_BLOCK_PUZZLE, SPMLocation.C83_RIGHT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS, SPMLocation.C83_LEFT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS],
        SPMRegion.LS401: [SPMLocation.C84_CHEST_AFTER_TINY_PASSAGE, SPMLocation.C84_CHEST_IN_FIRST_3_D_HALLWAYS, SPMLocation.C84_CHEST_IN_SECOND_3_D_HALLWAYS, SPMLocation.C84_CHEST_IN_THIRD_3_D_HALLWAYS],
    }
