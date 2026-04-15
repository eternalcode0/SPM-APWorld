import asyncio
import subprocess
import traceback
from typing import TYPE_CHECKING, ClassVar

import dolphin_memory_engine as dme
import Patch
import settings
import Utils
from CommonClient import (
    ClientCommandProcessor,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)

from .locations import BASE_LOCATION_ID, LOCATION_SETUP
from .types import GAME, StorageType

if TYPE_CHECKING:
    import kvui

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext

    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext


DOLPHIN_STATUS_INITIALIZING = "Dolphin connection has not been initiated."
DOLPHIN_STATUS_CONNECTED = "Dolphin connected successfully."
DOLPHIN_STATUS_LOST = "Dolphin connection was lost. Please restart your emulator."
DOLPHIN_STATUS_BAD_GAME = "Dolphin failed to connect. Please load a randomized ROM for Super Paper Mario."

# US0 addresses until I figure out how to support more versions.
# GP and its associated offsets: see https://github.com/SeekyCt/spm-decomp/blob/master/spm-headers/include/spm/spmario.h
GP_BASE = 0x804E2550
SAVE_NAME = 0x20 + GP_BASE
MAP_NAME = 0x44 + GP_BASE
GSW0 = 0x140 + GP_BASE
GSWF_BASE = 0x144 + GP_BASE
GSW_BASE = 0x544 + GP_BASE
COIN_ENTRIES = 0x1184 + GP_BASE

EXPECTED_GAME_ID = b"R8PE01"


class SPMCommandProcessor(ClientCommandProcessor):
    """Command Processor for Super Paper Mario"""

    def _cmd_dolphin(self) -> None:
        if isinstance(self.ctx, SuperPaperMarioContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_set_gswf(self, bit_number: int):
        """Used to manually set a GSWF bit."""
        byte_address, bit = gswf_set(int(bit_number))
        logger.info(f"Bit {bit} written at {hex(byte_address)}")

    def _cmd_check_gswf(self, bit_number: int):
        """Used to manually check a GSWF bit."""
        result = gswf_check(int(bit_number))
        logger.info(f"GSWF Check: 0x{format(result, 'x')}")

    def _cmd_set_gsw(self, gsw: int, value: int):
        """Used to manually set a GSW flag."""
        gsw_set(int(gsw), int(value))

    def _cmd_check_gsw(self, gsw: int):
        """Used to manually check a GSW flag."""
        result = gsw_check(int(gsw))
        logger.info(f"GSWF Check: {result}")


class SuperPaperMarioContext(SuperContext):
    command_processor = SPMCommandProcessor
    tags: ClassVar[set[str]] = {"AP"}
    game = GAME
    system = "WII"
    patch_suffix = ".apspm"

    awaiting_rom: bool
    dolphin_sync_task: asyncio.Task[None] | None
    dolphin_status: str
    checked_locations = set()

    def __init__(self, server_address, password) -> None:
        super().__init__(server_address, password)
        self.awaiting_rom = False
        self.dolphin_status = "Dolphin connection has not been initiated."

    async def validate_rom(self, ctx: SuperContext):
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

    async def check_spm_locations(self):
        locations_to_send = set()
        try:
            # TODO: optimize to exclude locations that have already been checked
            for ldata, _ in LOCATION_SETUP:
                lid = ldata.code + BASE_LOCATION_ID
                if ldata.var is None or lid is None or lid in self.checked_locations:
                    continue
                mode = ldata.var.mode
                addr = ldata.var.addr
                value = ldata.var.value
                if mode == StorageType.GSW:
                    if gsw_check(addr) >= value:
                        locations_to_send.add(lid)
                elif mode == StorageType.GSWF:
                    if gswf_check(addr):
                        locations_to_send.add(lid)
            if len(locations_to_send) > 0:
                self.checked_locations &= locations_to_send
                await self.send_msgs([{"cmd": "LocationChecks", "locations": locations_to_send}])
        except Exception:
            logger.error(traceback.format_exc())


def check_ingame() -> bool:
    return read_string(SAVE_NAME, 8) != "default"


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


def _get_bit_address(bit_number: int) -> tuple:
    word_index = bit_number >> 5
    bit_position = bit_number & 0x1F
    word_address = (word_index * 4) + GSWF_BASE
    byte_within_word = 3 - (bit_position >> 3)
    byte_address = word_address + byte_within_word
    bit = bit_position & 0x7
    return byte_address, bit


def gswf_set(bit_number: int):
    result = _get_bit_address(bit_number)
    if not result:
        return False
    byte_address, bit = result
    current_byte = dme.read_byte(byte_address)
    bit_mask = 1 << bit
    new_byte = current_byte | bit_mask
    dme.write_byte(byte_address, new_byte)
    return result


def gswf_check(bit_number: int) -> bool:
    result = _get_bit_address(bit_number)
    if not result:
        return False
    byte_address, bit = result
    current_byte = dme.read_byte(byte_address)
    bit_mask = 1 << bit
    return bool(current_byte & bit_mask)


def gsw_set(index, value):
    dme.write_word(GSW0, value) if index == 0 else dme.write_byte(GSW_BASE + index, value)


def gsw_check(index):
    return dme.read_word(GSW0) if index == 0 else dme.read_byte(GSW_BASE + index)


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
                    await ctx.check_spm_locations()
                else:
                    if not ctx.auth:
                        # set auth from slot name in rom
                        ctx.auth = "Player1"  # TODO: player name should be read from rom
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
                    if dme.read_bytes(0x80000000, 6) != EXPECTED_GAME_ID:
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
    auto_start = settings.get_settings()["super_paper_mario.world_options"].rom_start

    if auto_start is True:
        dolphin_path = settings.get_settings()["super_paper_mario.world_options"].dolphin_path
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
        if tracker_loaded:
            ctx.run_generator()
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


# Only US0 addresses for now until I figure out if I can support more revisions
# MEMORY = {
#     "file_name": 0x804E2570,
#     "gsw0": 0x804E2690,
#     "gswf_start": 0x804E2694,
#     "gsw1": 0x804E2A95,
# }
