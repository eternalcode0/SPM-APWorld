from collections.abc import Sequence

from worlds.AutoWorld import Tutorial, WebWorld

from .data import GAME
from .options import option_groups, option_presets


class SuperPaperMarioWebWorld(WebWorld):
    """Super Paper Mario Webpage Configuration"""

    game = GAME

    theme = "dirt"

    bug_report_page = "https://github.com/eternalcode0/SPM-APWorld/issues"

    option_groups = option_groups
    options_presets = option_presets

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
