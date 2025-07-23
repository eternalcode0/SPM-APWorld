"""Super Paper Mario APWorld"""

import logging
from typing import TextIO

from BaseClasses import Location, Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld

from .items import create_items, item_groups, item_table, CHARACTERS, PIXLS
from .constants import GAME, SuperPaperMarioItem, SPMEvent, SPMItem, SPMLocation, SPMRegion
from .locations import BASE_LOCATION_ID, location_groups, location_table
from .options import SuperPaperMarioOptions
from .regions import create_regions
from .rules import set_rules, SPMRuleBuilder


logger = logging.getLogger(__name__)


class SuperPaperMarioWebWorld(WebWorld):
    """Super Paper Mario Webpage Configuration"""
    theme = "dirt"
    bug_report_page = "https://github.com/eternalcode0/Archipelago"

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to playing Super Paper Mario with Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["EternalCode"]
        )]


class SuperPaperMarioWorld(World):
    """Super Paper Mario is a 2007 action role-playing game developed by Intelligent Systems and published by Nintendo
    for the Wii. The game follows Mario, Peach, Bowser, and Luigi as they attempt to collect Pure Hearts and stop Count
    Bleck and his minions from destroying the universe."""
    options_dataclass = SuperPaperMarioOptions
    options: SuperPaperMarioOptions
    game = GAME
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code + BASE_LOCATION_ID for name, data in location_table.items()
                           if data.code is not None and data.code != 0}
    origin_region_name = SPMRegion.MAC02_L_TOWER
    location_name_groups = location_groups
    item_name_groups = item_groups

    slot_data = {}
    rule_builder: SPMRuleBuilder

    # region APWorld Generation
    # sorted in execution order

    def generate_early(self):
        # Override options if necessary

        # Populate slot data from options
        self.slot_data = self.options.as_dict(
            "goal", "pure_hearts_required", "chapter_keys_lock", "shuffle_pure_hearts",
            toggles_as_bools=True)

        # Start Inventory
        character = CHARACTERS[self.options.starting_character]
        pixl = PIXLS[self.options.starting_pixl]
        self.push_precollected(self.create_item(character))
        self.push_precollected(self.create_item(pixl))

        self.slot_data.setdefault("starting_character", self.item_name_to_id[character])
        self.slot_data.setdefault("starting_pixl", self.item_name_to_id[pixl])

    # push start_inventory and start_inventory_from_pool into precollected_items

    def create_regions(self):
        create_regions(self)

    # All non-event locations finalized

    def create_items(self):
        base_pool = create_items(self)
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        excluded_pool = [item for item in base_pool if item not in self.multiworld.precollected_items[self.player]]
        filler_pool = [self.create_filler() for _ in range(total_locations - len(excluded_pool))]
        self.multiworld.itempool.extend(excluded_pool)
        self.multiworld.itempool.extend(filler_pool)

    # local_items overrides non_local_items

    def set_rules(self):
        self.rule_builder = SPMRuleBuilder(self)
        set_rules(self.rule_builder)

    def connect_entrances(self):
        # if self.options.randomize_entrances.value:
        #     self.rule_builder.randomize_entrances()
        from Utils import visualize_regions
        state = self.multiworld.get_all_state(False)
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region(self.origin_region_name), f"spm_{self.player_name}.puml",
                          linetype_ortho=False, regions_to_highlight=state.reachable_regions[self.player])

    # All rules finalized
    # location progress type assigned, excluded overrides priority
    # locality for local_items and non_local_item set

    def generate_basic(self):
        pass

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
        pass

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

    def create_item(self, name: str) -> SuperPaperMarioItem:
        item = item_table[name]
        return SuperPaperMarioItem(name, item.classification, item.code, self.player)

    def create_event(self, name: str) -> SuperPaperMarioItem:
        return SuperPaperMarioItem(name, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(item_groups["filler"]))

    def get_pre_fill_items(self) -> list[SuperPaperMarioItem]:
        return []

    # endregion
