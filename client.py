import asyncio
import subprocess
import traceback
from typing import TYPE_CHECKING

import dolphin_memory_engine as dme

import Patch
import settings
import Utils
from CommonClient import (
    ClientCommandProcessor,
    CommonContext,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)

from .data import GAME

if TYPE_CHECKING:
    import kvui


DOLPHIN_STATUS_INITIALIZING = "Dolphin connection has not been initiated."
DOLPHIN_STATUS_CONNECTED = "Dolphin connected successfully."
DOLPHIN_STATUS_LOST = "Dolphin connection was lost. Please restart your emulator."
DOLPHIN_STATUS_BAD_GAME = "Dolphin failed to connect. Please load a randomized ROM for Super Paper Mario."


class SPMCommandProcessor(ClientCommandProcessor):
    """Command Processor for Super Paper Mario"""

    def _cmd_dolphin(self) -> None:
        if isinstance(self.ctx, SuperPaperMarioContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class SuperPaperMarioContext(CommonContext):
    game = GAME
    system = "WII"
    patch_suffix = ".apspm"

    awaiting_rom: bool
    dolphin_sync_task: asyncio.Task[None] | None
    dolphin_status: str

    def __init__(self, server_address, password) -> None:
        super().__init__(server_address, password)
        self.awaiting_rom = False
        self.dolphin_status = "Dolphin connection has not been initiated."

    async def validate_rom(self, ctx: CommonContext):
        pass

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        return await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information.")
            return
        await self.send_connect()

    def make_gui(self) -> type["kvui.GameManager"]:
        """Initialize the GUI for Super Paper Mario client."""
        ui = super().make_gui()
        ui.base_title = "Archipelago Super Paper Mario Client"
        return ui


def check_ingame() -> bool:
    return read_string(MEMORY["file_name"], 8) != "default"


def read_string(address: int, strlen: int) -> str:
    return dme.read_bytes(address, strlen).split(b"\0", 1)[0].decode()


def read_short(address: int) -> int:
    """
    Read a 2-byte short from Dolphin memory.

    :param address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(dme.read_bytes(address, 2), byteorder="big")


def write_short(address: int, value: int) -> None:
    """
    Write a 2-byte short to Dolphin memory.

    :param address: Address to write to.
    :param value: Value to write.
    """
    dme.write_bytes(address, value.to_bytes(2, byteorder="big"))


def read_word(address: int) -> int:
    """
    Read a 2-byte short from Dolphin memory.

    :param address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(dme.read_bytes(address, 2), byteorder="big")


def write_short(address: int, value: int) -> None:
    """
    Write a 2-byte short to Dolphin memory.

    :param address: Address to write to.
    :param value: Value to write.
    """
    dme.write_bytes(address, value.to_bytes(2, byteorder="big"))


async def dolphin_sync_task(ctx: SuperPaperMarioContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: Super Paper Mario client context.
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information")
    sleep_time = 0.0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                # ctx.watcher_event gets set when receiving ReceivedItems or LocationInfo, or when shutting down.
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except TimeoutError:
                pass
            sleep_time = 0.0
        ctx.watcher_event.clear()

        try:
            if dme.is_hooked() and ctx.dolphin_status == DOLPHIN_STATUS_CONNECTED:
                if not check_ingame():
                    sleep_time = 0.1
                    continue
                dme.write_word(0x804CEA34, 10)
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        # death check
                        pass
                    # give items, check locations, etc.

                else:
                    if not ctx.auth:
                        # set auth from slot name in rom
                        pass
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                sleep_time = 0.1
            else:
                if ctx.dolphin_status == DOLPHIN_STATUS_CONNECTED:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = DOLPHIN_STATUS_LOST
                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if dme.is_hooked():
                    if dme.read_bytes(0x80000000, 6) != b"R8PE01":
                        logger.info(DOLPHIN_STATUS_BAD_GAME)
                        ctx.dolphin_status = DOLPHIN_STATUS_BAD_GAME
                        dme.un_hook()
                        sleep_time = 5
                    else:
                        logger.info(DOLPHIN_STATUS_CONNECTED)
                        ctx.dolphin_status = DOLPHIN_STATUS_CONNECTED
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = DOLPHIN_STATUS_LOST
                    await ctx.disconnect()
                    sleep_time = 5
                    continue
        except Exception:
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = DOLPHIN_STATUS_LOST
            await ctx.disconnect()
            sleep_time = 5
            continue


async def _run_game(rom: str):
    import os

    # TODO: Fix weird settings name
    auto_start = settings.get_settings()['super_paper_mario.world_options'].rom_start

    if auto_start is True:
        dolphin_path = settings.get_settings()['super_paper_mario.world_options'].dolphin_path
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
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APTTYD file")
    args = parser.parse_args(args)

    import colorama

    colorama.init()
    asyncio.run(_main(args))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APSPM file")
    args = parser.parse_args()
    main(args.connect, args.password, args.patch_file)


MEMORY = {
    "file_name": 0x804E2570,
    "gswf_start": 0x804E2694,
}
