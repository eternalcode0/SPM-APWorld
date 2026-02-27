from enum import IntEnum, auto

GAME = "Super Paper Mario"

class RandomizationType(IntEnum):
    DISABLED = auto()
    """The check is not added to the multiworld in any way"""
    VANILLA_WORLD = auto()
    """
    The location has its vanilla item and is added to the multiworld via place_locked_item.
    Good for checks that should always be to be shared with the tracker/multiworld.
    """
    VANILLA_EVENT = auto()
    """
    The location has its vanilla item but is only added to the multiworld via an event.
    Good for story progression or checks that don't make sense as an item such as unlocking the boat or royal stickers.
    """
    SHUFFLED = auto()
    """
    The location is added to the multiworld but should be restricted to certain item pools.
    Intended to be used with pre-fill.
    """
    RANDOM = auto()
    """The location is added to the multiworld and is randomized as normal."""
