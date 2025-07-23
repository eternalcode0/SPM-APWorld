from enum import auto, IntEnum
from dataclasses import dataclass


class StorageType(IntEnum):
    """The various types of script variables"""
    LSW = auto()
    LSWF = auto()
    GF = auto()
    GSW = auto()
    GSWF = auto()
    GW = auto()


@dataclass
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
