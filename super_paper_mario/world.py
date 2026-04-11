import logging
from typing import Any, TextIO

from BaseClasses import Item, ItemClassification, Location, Region
from Options import Option, Visibility

from . import items, patch, rules
from .locations import LOCATION_GROUP_MAP, LOCATION_NAME_TO_ID, create_all_locations, get_location_map
from .names import ItemName, LocationName, RegionName
from .options import FlopsidePitAccess, PitAccess
from .regions import create_regions, get_region_map
from .types import GAME, SPMWorldBase

logger = logging.getLogger(__name__)


# TODO: Explore using CachedRuleBuilderWorld.
# Last test when rules were just flip/flopside & chapter 1, the fuzzer was slower with the following settings:
# python fuzz.py -g super_paper_mario -j 8 -r 100 -m fuzz.meta.yaml -n 10
class SuperPaperMarioWorld(SPMWorldBase):
    """Super Paper Mario is a 2007 action role-playing game developed by Intelligent Systems and published by Nintendo
    for the Wii. The game follows Mario, Peach, Bowser, and Luigi as they attempt to collect Pure Hearts and stop Count
    Bleck and his minions from destroying the universe."""

    game = GAME

    # Generic AP World stuffs
    item_name_to_id = items.ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID
    origin_region_name = RegionName.MAC02_L_TOWER
    location_name_groups = LOCATION_GROUP_MAP
    item_name_groups = items.ITEM_GROUP_MAP

    # SPM specific stuffs
    rm: dict[RegionName, Region]
    lm: dict[LocationName, Location]
    slot_data = {}
    disabled_locations: set[str] = set()
    filler_options: dict[ItemName, int] = {}
    starting_pair: tuple[ItemName, ItemName]

    # Universal Tracker stuffs
    ut_can_gen_without_yaml = True
    is_ut: bool
    # tracker_world: ClassVar[dict[str, Any]] = {
    #     "map_page_folder": "tracker",
    #     "map_page_maps": "maps/maps.json",
    #     "map_page_locations": "locations/locations.json",
    # }

    # region APWorld Generation
    # sorted in execution order

    def generate_early(self):
        options = self.options

        # Override options if necessary
        if (
            options.flopside_pit_access.value == PitAccess.option_normal
            and options.flipside_pit_access.value == PitAccess.option_closed
        ):
            options.flopside_pit_access.value = FlopsidePitAccess.option_no_flipside

        # UT shenanigans
        self.is_ut = getattr(self.multiworld, "generation_is_fake", False)
        self.prepare_ut()

        # Populate slot data from options
        visible_option_keys = [
            key for key in self.options.__dict__.keys() if getattr(self.options, key).visibility != Visibility.none
        ]
        self.slot_data["options"] = self.options.as_dict(*visible_option_keys)

        # Start Inventory
        character = items.CHARACTERS[self.options.starting_character.value]
        pixl = items.PIXLS[self.options.starting_pixl.value]
        self.starting_pair = (character, pixl)
        self.push_precollected(self.create_item(character))
        self.push_precollected(self.create_item(pixl))

        # Disabled Locations
        if self.options.flipside_pit_access.value == PitAccess.option_closed:
            self.disabled_locations.update(LOCATION_GROUP_MAP["Flipside Pit"])
        if self.options.flopside_pit_access.value == PitAccess.option_closed:
            self.disabled_locations.update(LOCATION_GROUP_MAP["Flopside Pit"])

    # push start_inventory and start_inventory_from_pool into precollected_items

    def create_regions(self):
        create_regions(self)
        self.rm = get_region_map(self)
        self.lm = get_location_map(self)
        # create_all_locations also gives the sum of each individual vanilla item from randomized locations
        # this lets us maintain a similar amount of filler to vanilla for randomized locations regardless of options
        self.filler_options = create_all_locations(self)

    # All non-event locations finalized

    def create_items(self):
        items.override_filler_options(self)
        base_pool = items.create_items(self)
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        filler_pool = self.random.choices(
            population=list(self.filler_options.keys()),
            weights=list(self.filler_options.values()),
            k=total_locations - len(base_pool),
        )
        filler_pool = [self.create_item(name) for name in filler_pool]
        self.multiworld.itempool.extend(base_pool)
        self.multiworld.itempool.extend(filler_pool)

    # local_items overrides non_local_items

    def set_rules(self):
        rules.set_rules(self)

    def connect_entrances(self):
        entrances = rules.connect_regions(self)
        if self.options.randomize_entrances.value:
            er_placement = rules.randomize_entrances(self, entrances)
            self.slot_data["entrances"] = er_placement.pairings

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

    def create_item(self, name: str) -> items.SPMItem:
        return items.create_item(self, ItemName(name))

    def create_event(self, name: str) -> items.SPMItem:
        return items.SPMItem(name, ItemClassification.progression, None, self.player)

    def get_pre_fill_items(self) -> list[Item]:
        return []

    def gen_diagram(self) -> None:
        if self.player_name != "TEST123":
            return
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

    # endregion

    # region Universal Tracker

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any] | None:
        return slot_data

    def prepare_ut(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if not (re_gen_passthrough and self.game in re_gen_passthrough):
            return
        # Get the passed through slot data from the real generation
        slot_data: dict[str, Any] = re_gen_passthrough[self.game]

        slot_options: dict[str, Any] = slot_data.get("options", {})
        # Set all your options here instead of getting them from the yaml
        for key, value in slot_options.items():
            opt: Option | None = getattr(self.options, key, None)
            if opt is not None:
                # You can also set .value directly but that won't work if you have OptionSets
                setattr(self.options, key, opt.from_any(value))

    # endregion
