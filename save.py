"""Utility file for managing the save file"""
from .flags import GSWF

NEW_SAVE = frozenset([
    GSWF(2),  # Save block tutorial text seen
    GSWF(386),  # 3D tutorial text seen
    GSWF(387),  # "Defeat enemies to earn points" text seen, 1-1
    GSWF(392),  # Mushroom text seen
    GSWF(393),  # Mega Star text seen
    GSWF(394),  # Fast Flower text seen
    GSWF(395),  # Slow Flower text seen
    GSWF(396),  # Happy Flower text seen
    GSWF(397),  # Zombie Shroom OR Ghoul Shroom text seen
    GSWF(398),  # Pal Pills text seen
    GSWF(399),  # Caught Card text seen
    GSWF(407),  # Hearing the item shop explanation for the first time
    GSWF(408),  # Talking to Notso for the first time
    GSWF(420),  # Low HP tutorial text seen
    GSWF(431),  # Return pipe tutorial text shown
    GSWF(512),  # Tippi tells you what a save block is
    # I've defaulted logic to expect these for now but they could probably be a yaml option
    GSWF(533),  # Blue Pipe built (mac_05 <-> mac_02)
    GSWF(534),  # Blue Pipe built (mac_12 <-> mac_02)
    GSWF(535),  # Blue Pipe built (mac_15 <-> mac_12)
])
"""The set of GSWF flags to set on new save file. Should be moved to basepatch ASAP."""
