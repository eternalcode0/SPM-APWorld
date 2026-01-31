import asyncio
import dolphin_memory_engine
import subprocess
import traceback

from CommonClient import CommonContext, get_base_parser, gui_enabled, logger, server_loop
import Patch
import settings
import Utils

from .constants import GAME


class SuperPaperMarioContext(CommonContext):
    game = GAME
    patch_suffix = ".apspm"
    dolphin_sync_task: asyncio.Task[None] | None

    def __init__(self, server_address, password) -> None:
        super().__init__(server_address, password)

    async def validate_rom(self, ctx: CommonContext):
        raise NotImplementedError("oops")


async def dolphin_sync_task(ctx: SuperPaperMarioContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: Super Paper Mario client context.
    """
    logger.info("Starting Dolphin connector")
    sleep_time = 0.0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                # ctx.watcher_event gets set when receiving ReceivedItems or LocationInfo, or when shutting down.
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except asyncio.TimeoutError:
                pass
            sleep_time = 0.0
        ctx.watcher_event.clear()

        try:
            pass
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            await ctx.disconnect()
            sleep_time = 5
            continue


async def _run_game(rom: str):
    import os
    auto_start = settings.get_settings().super_paper_mario_options.rom_start

    if auto_start is True:
        dolphin_path = settings.get_settings().super_paper_mario_options.dolphin_path
        subprocess.Popen(
            [
                dolphin_path,
                f"--exec={os.path.realpath(rom)}",
            ],
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


async def _patch_and_run_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)
    Utils.async_start(_run_game(output_file))
    return metadata


def main(*args) -> None:
    """
    Run the main async loop for the Super Paper Mario client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Super Paper Mario Client")

    async def _main(args) -> None:
        if args.patch_file:
            await asyncio.create_task(_patch_and_run_game(args.patch_file))
        ctx = SuperPaperMarioContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        # Wake the sync task, if it is currently sleeping, so it can start shutting down when it sees that the
        # exit_event is set.
        ctx.watcher_event.set()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APSPM file")
    args = parser.parse_args(args)

    import colorama

    colorama.init()
    asyncio.run(_main(args))
    colorama.deinit()
