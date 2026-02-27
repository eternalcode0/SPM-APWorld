import typing

from BaseClasses import Region

from .names import RegionName

if typing.TYPE_CHECKING:
    from . import SuperPaperMarioWorld


def create_regions(world: "SuperPaperMarioWorld"):
    """Create each region needed for the world and add it to the multiworld"""
    player = world.player
    multiworld = world.multiworld

    multiworld.regions.extend(Region(region_name, player, multiworld) for region_name in RegionName)


def get_region_map(
    world: "SuperPaperMarioWorld", region_names: list[RegionName] | None = None
) -> dict[RegionName, Region]:
    if region_names is None or len(region_names) == 0:
        region_names = list(RegionName)
    return {region_name: world.get_region(region_name) for region_name in region_names}
