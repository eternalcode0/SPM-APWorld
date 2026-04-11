import struct
from collections.abc import Sequence
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import ClassVar

from BaseClasses import Item, Location, MultiWorld, Tutorial
from settings import Group, UserFilePath
from worlds.AutoWorld import WebWorld, World

from .options import OPTION_GROUPS, OPTION_PRESETS, SuperPaperMarioOptions

# region AP Types

GAME = "Super Paper Mario"


class SPMItem(Item):
    """An Item belonging to an instance of Super Paper Mario"""

    game: str = GAME


class SPMLocation(Location):
    """A Location belonging to an instance of Super Paper Mario"""

    game: str = GAME


class RandomizationType(IntEnum):
    """A descriptor for how/when a location gets randomized"""

    DISABLED = auto()
    """The check is not added to the multiworld in any way"""
    VANILLA_WORLD = auto()
    """
    The location has its vanilla item and is added to the multiworld via place_locked_item.
    Good for checks that should always be to be shared with the tracker/multiworld.
    """
    VANILLA_EVENT = auto()
    """
    The location has its vanilla item but is only added to the multiworld via region.add_event.
    Good for story progression or checks.
    """
    SHUFFLED = auto()
    """
    The location is added to the multiworld but should be restricted to certain item pools.
    Intended to be used with pre-fill.
    """
    RANDOM = auto()
    """The location is added to the multiworld and is randomized as normal."""


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


class SuperPaperMarioSettings(Group):
    class DolphinPath(UserFilePath):
        """The location of the Dolphin you want to auto launch patched ROMs with"""

        is_exe = True
        description = "Dolphin Executable"

    class RomFile(UserFilePath):
        """File name of the Super Paper Mario US0 rom"""

        copy_to = "SuperPaperMario-US0.wbfs"
        description = "Super Paper Mario US0 ROM File"

    dolphin_path: DolphinPath = DolphinPath(None)
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class SPMWorldBase(World):
    """Base world for importing into other files. Helps prevent circular dependencies, better TypeVar usage, and
    separation of concerns."""

    settings: ClassVar[SuperPaperMarioSettings]
    options_dataclass = SuperPaperMarioOptions
    options: SuperPaperMarioOptions
    web: ClassVar[WebWorld] = SuperPaperMarioWebWorld()

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld, player)


# endregion

# region Game Types

# region Script Types


class StorageType(IntEnum):
    """The various types of script variables"""

    LSW = auto()
    LSWF = auto()
    GF = auto()
    GSW = auto()
    GSWF = auto()
    GW = auto()


class ScriptVariable:
    """A class intended to be inherited to keep track of specific script
    variables in the game"""

    mode: StorageType
    addr: int
    value: int

    def __init__(self, mode: StorageType, addr: int, value: int):
        self.mode = mode
        self.addr = addr
        self.value = value


class LSW(ScriptVariable):
    """No idea what these are used for yet. LSW 0-1023 exist."""

    def __init__(self, addr: int, value: int):
        assert 0 <= addr <= 1023
        super().__init__(StorageType.LSW, addr, value)


class LSWF(ScriptVariable):
    """No idea what these are used for yet. LSWF 0-511 exist."""

    def __init__(self, addr: int, value: bool = True):
        assert 0 <= addr <= 511
        super().__init__(StorageType.LSWF, addr, int(value))


class GF(ScriptVariable):
    """GF are global flags which don't persist between game reloads. They can be
    accessed directly by evt scripts, or by code through the EvtWork struct. GF
    0-91 exist."""

    def __init__(self, addr: int, value: bool = True):
        assert 0 <= addr <= 91
        super().__init__(StorageType.GF, addr, int(value))


class GSW(ScriptVariable):
    """GSW are global integers which persist between game reloads. GSW 0 is
    32-bit, and all others are 8-bit. They can be accessed directly by evt
    scripts, or by code through the swByteGet/swByteSet functions. GSW 0-2047
    exist."""

    def __init__(self, addr: int, value: int):
        assert (addr == 0 and 0 <= value <= 0xFFFFFFFF) or (1 <= addr <= 2047 and 0 <= value <= 0xFF)
        super().__init__(StorageType.GSW, addr, value)


class GSWF(ScriptVariable):
    """GSWF are global flags which persist between game reloads. They can be
    accessed directly by evt scripts, or by code through the swGet/swSet/swClear
    functions. GSWF 0-8191 exist."""

    def __init__(self, addr: int, value: bool = True):
        assert 0 <= addr <= 8191
        super().__init__(StorageType.GSWF, addr, int(value))


class GW(ScriptVariable):
    """GW are global integers which persist between game reloads. All GW are
    32-bit. They can be accessed directly by evt scripts, or by code through the
    EvtWork struct. GW 0-31 exist."""

    def __init__(self, addr: int, value: int):
        assert 0 <= addr <= 31 and 0 <= value <= 0xFFFFFFFF
        super().__init__(StorageType.GW, addr, value)


NEW_SAVE = [
    GSW(0, 11),  # Skips Merlon giving red heart, Tippi taking you to 1st Pillar and inserting heart, entering 1-1 door
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
]
"""The set of GSWF flags to set on new save file. Should be moved to basepatch ASAP."""


# endregion

# region Level Data

LEVEL_SETUP_ENTRY_SIZES = [0, 0x20, 0x60, 0x64, 0x68, 0x6C, 0x70]
"""Each /files/setup/ level's 2nd byte describes what type of in-game struct is
used for its entry. This is the size of each entry based off the 2nd byte (1-6).
E.g. he1_01 uses type 6 so each entry is 0x70 bytes. Index 0 here is just
padding for a get by index and is invalid.
"""


@dataclass
class LevelSetupEntry:
    """Internal class to represent an individual entry of /files/setup/ files.
    These entries have variable size based off the file's header, see
    LEVEL_SETUP_ENTRY_SIZES. Typically represents an enemy.
    """

    header: bytes | None  # 4byte unknown
    x_pos: float
    y_pos: float
    z_pos: float
    id: int  # u32
    footer: bytes | None  # 16byte unknown

    def pack(self) -> bytes:
        prepend = self.header or bytes([])
        append = self.footer or bytes([])
        return prepend + struct.pack(">fffI", self.x_pos, self.y_pos, self.z_pos, self.id) + append

    @classmethod
    def unpack(cls, setup_header: bytes, entry: bytes):
        """Instantiate a LevelSetupEntry
        setup_header -- The 4 byte header from the setup file
        entry -- The entry's data, should be sized to exactly one of
            LEVEL_SETUP_ENTRY_SIZES.
        """
        assert len(setup_header) == 4
        assert LEVEL_SETUP_ENTRY_SIZES[setup_header[1]] == len(entry)
        start = 4 if setup_header[1] == 1 else 0  # 2nd byte `1` means there's 4 extra bytes at the start to preserve
        header = entry[0:start]
        data = struct.unpack(">fffI", entry[start : start + 16])
        footer = entry[start + 16 :]
        return cls(header if len(header) else None, *data, footer if len(footer) else None)


@dataclass
class LevelSetupFile:
    """Internal class to represent a whole /files/setup/ file."""

    header: bytes
    entries: list[LevelSetupEntry]
    footer: bytes

    def pack(self) -> bytes:
        result = self.header or bytes([])
        for entry in self.entries:
            result.extend(entry.pack())
        result.extend(self.footer)
        return result

    @classmethod
    def unpack(cls, content: bytes):
        header = content[0:4]
        footer = content[-4:]
        size = LEVEL_SETUP_ENTRY_SIZES[header[1]]
        entries_data = content[4:-4]  # shave off the header/footer
        entries_list = [entries_data[i : i + size] for i in range(0, len(entries_data), size)]
        entries = [LevelSetupEntry.unpack(header, entry) for entry in entries_list]
        return cls(header, entries, footer)


# endregion

# endregion
