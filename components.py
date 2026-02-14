from worlds.LauncherComponents import Component, Type, components, launch_subprocess, SuffixIdentifier

from .data import GAME


def run_client(*args) -> None:
    from .client import main

    launch_subprocess(main, name="Super Paper Mario Client", args=args)


components.append(
    Component(
        "Super Paper Mario Client",
        func=run_client,
        game_name=GAME,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apspm"),
    )
)
