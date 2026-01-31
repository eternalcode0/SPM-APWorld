"""A wrapper to interface with Wiimms ISO Tools
It is expected that v3.05a-r8638 is placed in your AP lib folder.
The path to the binary folder should look like /Archipelago/lib/wit/bin/
"""
import os
import platform
import shutil
import subprocess


TMP = "temp"
TMP_EXTRACT = f"{TMP}/spm_extract"


def get_binary_path() -> str:
    system = platform.system()
    if system == "Windows":
        return "lib/wit/bin/wit.exe"
    if system == "Linux":
        return "lib/wit/bin/wit"
    raise NotImplementedError(f"unsure how to interface with wit on '{system}'")


class WIT:
    def unpack_iso(in_path: str, out_path: str):
        wit = get_binary_path()
        subprocess.call([
            wit,
            "extract",
            in_path,
            out_path,
        ])

    def pack_iso(in_path: str, out_path: str):
        wit = get_binary_path()
        subprocess.call([
            wit,
            "copy",
            "--align-files",
            "--name",
            "Super Paper Mario - AP Randomizer",
            "--modify",
            "AUTO",
            in_path,
            out_path,
        ])
