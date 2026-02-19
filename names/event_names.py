from enum import StrEnum


class EventName(StrEnum):
    """All Event names"""

    SWITCH_YOLD_RUINS_SQUIG_ROOM = "Hit the Blue Switch in 1-4 Squig Room"
    # GSWF(501)
    SWITCH_FLIPSIDE_PIT_CAGE = "Hit the Blue Switch on the Flipside Pit Cage"
    # GSW(0, 70)
    SWITCH_GLOAM_VALLEY_BACKGROUND = "Hit the Blue Switch in 2-1 Background"
    # GSW(0, 74)
    SWITCH_GLOAM_VALLEY_UNDERGROUND = (
        "Hit the Blue Switch in 2-1 Underground Stacked Rooms 2"
    )
    # GSWF(507)
    SMASH_FLOPSIDE_B1_OUTSKIRTS_BLOCK = "Smashed the block in Flopside B1 Outskirts"
    # GSWF(504)
    SMASH_FLOPSIDE_B2_OUTSKIRTS_BLOCK = "Smashed the block in Flopside B2 Outskirts"
    OPEN_THE_RUBEE_VAULT = "[EVENT][2-3] Open the Rubee Vault"
    COMPLETED_FLIPSIDE_PIT = "Completed Flipside Pit"
    COMPLETED_FLOPSIDE_PIT = "Completed Flopside Pit"
    VICTORY = "Victory"
