"""rom.py handles all things data conversion and representation to/from the rom.
It does not handles reading/writing to the rom, that is handled by patch.py"""

import struct
from dataclasses import dataclass

LEVEL_SETUP_ENTRY_SIZES = [0, 0x20, 0x60, 0x64, 0x68, 0x6C, 0x70]
"""Each /files/setup/ level's 2nd byte describes what type of in-game struct is
used for its entry. This is the size of each entry based off the 2nd byte (1-6).
E.g. he1_01 uses type 6 so each entry is 0x70 bytes. 0 is not a valid 2nd byte,
index 0 here is just padding.
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
