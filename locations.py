from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items, regions
from .data import GAME, RandomizationType, location_data
from .names import LocationName

if TYPE_CHECKING:
    from .world import SuperPaperMarioWorld

BASE_LOCATION_ID = 4_998_000

LOCATION_ENUM_TO_DATA = {
    data.name: data for data in location_data.LOCATION_DATA if data.code is not None and data.region is not None
}
LOCATION_NAME_TO_ID = {name.value: data.code + BASE_LOCATION_ID for name, data in LOCATION_ENUM_TO_DATA.items()}
LOCATION_GROUPS = {group for loc in location_data.LOCATION_DATA for group in loc.groups}
LOCATION_GROUP_MAP = {
    group: {loc.name.value for loc in location_data.LOCATION_DATA if group in loc.groups} for group in LOCATION_GROUPS
}


class SPMLocation(Location):
    game = GAME


def get_location_names_with_ids(location_names: list[LocationName]) -> dict[str, int]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: "SuperPaperMarioWorld"):
    region_map = regions.get_region_map(world)
    for location in LOCATION_ENUM_TO_DATA.values():
        rt = location.setting(world.options) if callable(location.setting) else location.setting
        if rt == RandomizationType.VANILLA_WORLD:
            loc = SPMLocation(
                world.player, location.name.value, LOCATION_NAME_TO_ID[location.name.value], region_map[location.region.value]
            )
            loc.place_locked_item(world.create_item(location.item.value))
            region_map[location.region].locations.append(loc)
        elif rt == RandomizationType.VANILLA_EVENT:
            region_map[location.region].add_event(location.name.value, location.item.value, None, SPMLocation, items.SPMItem)
        elif rt == RandomizationType.RANDOM:
            region_map[location.region].locations.append(
                SPMLocation(
                    world.player, location.name.value, LOCATION_NAME_TO_ID[location.name.value], region_map[location.region.value]
                )
            )


def get_location_map(world: "SuperPaperMarioWorld", location_names: list[LocationName] | None = None) -> dict[LocationName, SPMLocation]:
    if location_names is None or len(location_names) == 0:
        location_names = list(LocationName)
    return {location.name: location for location in world.get_locations() if location.name in location_names}
