from collections.abc import Sequence

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .data import GAME
from .options import OPTION_GROUPS, OPTION_PRESETS


class SuperPaperMarioWebWorld(WebWorld):
    """Super Paper Mario Webpage Configuration"""

    game = GAME

    theme = "dirt"

    bug_report_page = "https://github.com/eternalcode0/SPM-APWorld/issues"

    option_groups = OPTION_GROUPS
    options_presets = OPTION_PRESETS

    rich_text_options_doc = True

    tutorials: Sequence[Tutorial] = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Super Paper Mario with Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["EternalCode"],
        )
    ]
