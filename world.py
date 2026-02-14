import logging
from typing import ClassVar, TextIO

from BaseClasses import ItemClassification, Region
from settings import Group, UserFilePath
from worlds.AutoWorld import World

from . import patch
from .data import GAME
from .items import CHARACTERS, ITEM_GROUP_MAP, ITEM_NAME_TO_ID, PIXLS, SPMItem, create_item, create_items
from .locations import LOCATION_GROUP_MAP, LOCATION_NAME_TO_ID, SPMLocation, create_all_locations, get_location_map
from .names import EventName, ItemName, LocationName, RegionName
from .options import PitAccess, SuperPaperMarioOptions, Traps
from .regions import create_regions, get_region_map
from .rules import set_rules, connect_regions

logger = logging.getLogger(__name__)


class SuperPaperMarioSettings(Group):
    class DolphinPath(UserFilePath):
        """The location of the Dolphin you want to auto launch patched ROMs with"""

        is_exe = True
        description = "Dolphin Executable"

    class RomFile(UserFilePath):
        """File name of the Super Paper Mario US0 rom"""

        copy_to = "SuperPaperMario-US0.wbfs"
        description = "Super Paper Mario US0 ROM File"

    dolphin_path: DolphinPath = DolphinPath(None)
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True



class SuperPaperMarioWorld(World):
    """Super Paper Mario is a 2007 action role-playing game developed by Intelligent Systems and published by Nintendo
    for the Wii. The game follows Mario, Peach, Bowser, and Luigi as they attempt to collect Pure Hearts and stop Count
    Bleck and his minions from destroying the universe."""

    settings: ClassVar[SuperPaperMarioSettings]
    options_dataclass = SuperPaperMarioOptions
    options: SuperPaperMarioOptions
    game = GAME
    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID
    origin_region_name = RegionName.MAC02_L_TOWER
    location_name_groups = LOCATION_GROUP_MAP
    item_name_groups = ITEM_GROUP_MAP

    rm: dict[RegionName, Region]
    lm: dict[LocationName, SPMLocation]
    slot_data = {}
    disabled_locations: set[str] = set()
    filler_options: list[str] = []

    # region APWorld Generation
    # sorted in execution order

    def generate_early(self):
        # Override options if necessary

        # Populate slot data from options
        self.slot_data = self.options.as_dict(
            "goal", "pure_hearts_required", "chapter_keys_lock", "shuffle_pure_hearts", toggles_as_bools=True
        )

        # Start Inventory
        character = CHARACTERS[self.options.starting_character.value]
        pixl = PIXLS[self.options.starting_pixl.value]
        self.push_precollected(self.create_item(character))
        self.push_precollected(self.create_item(pixl))

        self.slot_data.setdefault("starting_character", self.item_name_to_id[character])
        self.slot_data.setdefault("starting_pixl", self.item_name_to_id[pixl])

        if self.options.flipside_pit_access == PitAccess.option_open:
            self.push_precollected(self.create_event(EventName.SWITCH_FLIPSIDE_PIT_CAGE))

        # Disabled Locations
        if self.options.flipside_pit_access.value == PitAccess.option_closed:
            self.disabled_locations.update(LOCATION_GROUP_MAP["Flipside Pit"])
        if self.options.flopside_pit_access.value == PitAccess.option_closed:
            self.disabled_locations.update(LOCATION_GROUP_MAP["Flopside Pit"])

        self.filler_options.append(ItemName.SHROOM_SHAKE)
        # self.filler_options.extend(LOCATION_GROUP_MAP["filler"])
        # if self.options.traps.value != Traps.option_none:
        #     self.filler_options.extend(
        #         [
        #             ItemName.SLOW_CURSYA_TRAP,
        #             ItemName.HEAVY_CURSYA_TRAP,
        #             ItemName.REVERSYA_CURSYA_TRAP,
        #             ItemName.TECH_CURSYA_TRAP,
        #         ]
        #     )
        # if self.options.traps.value == Traps.option_all:
        #     self.filler_options.append(ItemName.BACK_CURSYA_TRAP)

    # push start_inventory and start_inventory_from_pool into precollected_items

    def create_regions(self):
        create_regions(self)
        self.rm = get_region_map(self)
        create_all_locations(self)
        self.lm = get_location_map(self)

    # All non-event locations finalized

    def create_items(self):
        base_pool, filler_choices = create_items(self)
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        excluded_pool = [item for item in base_pool if item not in self.multiworld.precollected_items[self.player]]
        filler_pool = [self.create_filler() for _ in range(total_locations - len(excluded_pool))]
        self.multiworld.itempool.extend(excluded_pool)
        self.multiworld.itempool.extend(filler_pool)

    # local_items overrides non_local_items

    def set_rules(self):
        set_rules(self)

    def connect_entrances(self):
        connect_regions(self)
        # if self.options.randomize_entrances.value:
        #     self.rule_builder.randomize_entrances()

    # All rules finalized
    # location progress type assigned, excluded overrides priority
    # locality for local_items and non_local_item set

    def generate_basic(self):
        self.gen_diagram()

    # remove start_inventory_from_pool from the pool
    # process item_links
    # item plando is processed

    def pre_fill(self):
        pass

    # finalize item pool
    # perform standard fill

    def post_fill(self):
        pass

    # finalize randomization, no more calls to self.random
    # process progression balancing
    # perform accessibility check

    def generate_output(self, output_directory: str):
        patch.output_patch(self, output_directory)
        self.gen_diagram()

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        pass

    def fill_slot_data(self):
        return self.slot_data

    # playthrough is calculated

    def write_spoiler_header(self, spoiler_handle: TextIO):
        pass

    def write_spoiler(self, spoiler_handle: TextIO):
        pass

    def write_spoiler_end(self, spoiler_handle: TextIO):
        pass

    # output zip
    # endregion

    # region Utility Methods

    def create_item(self, name: str) -> SPMItem:
        return create_item(self, name)

    def create_event(self, name: str) -> SPMItem:
        return SPMItem(name, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_options)

    def get_pre_fill_items(self) -> list[SPMItem]:
        return []

    def gen_diagram(self) -> None:
        from Utils import visualize_regions

        state = self.multiworld.get_all_state(False)
        state.update_reachable_regions(self.player)
        visualize_regions(
            self.get_region(self.origin_region_name),
            f"spm_{self.player_name}.puml",
            show_other_regions=True,
            linetype_ortho=False,
            show_entrance_names=True,
            regions_to_highlight=set(state.reachable_regions[self.player]),
        )
        pass

    # endregion
