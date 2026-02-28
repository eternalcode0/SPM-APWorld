from __future__ import annotations

import typing

from BaseClasses import Region

from .names import RegionName
from .options import PitAccess

if typing.TYPE_CHECKING:
    from . import SuperPaperMarioWorld


def create_regions(world: SuperPaperMarioWorld):
    """Create each region needed for the world and add it to the multiworld"""
    player = world.player
    multiworld = world.multiworld

    disabled_regions = disabled_region_list(world)
    multiworld.regions.extend(
        Region(region_name, player, multiworld) for region_name in RegionName if region_name not in disabled_regions
    )


def disabled_region_list(world: SuperPaperMarioWorld) -> list[RegionName]:
    disabled = []
    if world.options.flipside_pit_access == PitAccess.option_closed:
        disabled.append(RegionName.L_FLIPSIDE_PIT)
    if world.options.flopside_pit_access == PitAccess.option_closed:
        disabled.append(RegionName.L_FLOPSIDE_PIT)
    return disabled


def get_region_map(
    world: SuperPaperMarioWorld, region_names: list[RegionName] | None = None
) -> dict[RegionName, Region]:
    disabled_regions = disabled_region_list(world)
    if region_names is None or len(region_names) == 0:
        region_names = [name for name in RegionName if name not in disabled_regions]
    return {region_name: world.get_region(region_name) for region_name in region_names}
