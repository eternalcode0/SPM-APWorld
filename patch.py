import json
import os
import random
import shutil
from typing import TYPE_CHECKING

from settings import get_settings
from worlds.Files import APPatchExtension, APProcedurePatch, AutoPatchExtensionRegister

from .data import GAME
from .wit import WIT

if TYPE_CHECKING:
    from . import SuperPaperMarioWorld

TMP_EXTRACT = "temp_spm"

class SPMProcedurePatch(APProcedurePatch):
    game = GAME
    patch_file_ending = ".apspm"
    result_file_ending = ".wbfs"
    file_path: str
    hash = ""

    procedure = [
        (("patch_iso"), []),
    ]

    def patch(self, target) -> None:
        self.file_path = target
        self.read()
        patch_extender = AutoPatchExtensionRegister.get_handler(self.game)
        assert not isinstance(self.procedure, str), f"{type(self)} must define procedures"
        for step, args in self.procedure:
            if isinstance(patch_extender, list):
                extension = next(
                    (
                        item
                        for item in [getattr(extender, step, None) for extender in patch_extender]
                        if item is not None
                    ),
                    None,
                )
            else:
                extension = getattr(patch_extender, step, None)
            if extension is not None:
                extension(self, *args)


class SPMPatchExtension(APPatchExtension):
    game = GAME

    @staticmethod
    def patch_iso(spmpp: SPMProcedurePatch):
        options = json.loads(spmpp.get_file("options.json").decode("UTF-8"))
        WIT.unpack_iso(get_settings()['super_paper_mario.world_options'].rom_file, TMP_EXTRACT)
        if options["randomize_enemies"]:
            SPMPatchExtension.randomize_enemies()
        if options["randomize_music"]:
            SPMPatchExtension.randomize_music()
        if options["practice_codes"]:
            SPMPatchExtension.apply_practice_codes()
        WIT.pack_iso(TMP_EXTRACT, spmpp.file_path)
        shutil.rmtree(TMP_EXTRACT)

    @staticmethod
    def randomize_enemies():
        # with open(f"{TMP_EXTRACT}/files/setup/he1_01.dat", "r+b") as file:
        #     file.seek(0x13)
        #     file.write(bytes([3])) # Changes the 1-1 Goomba to a Spiked Goomba
        pass

    @staticmethod
    def randomize_music():
        folder_path = f"{TMP_EXTRACT}/files/sound"
        # Credit to SacredGhost for the music shuffler
        # Get all .brstm files
        brstms = [
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(".brstm")
        ]

        if len(brstms) < 2:
            return

        # rename temp
        temp_names = []
        for i, filename in enumerate(brstms):
            temp_name = f"__temp_{i}.brstm"
            os.rename(
                os.path.join(folder_path, filename),
                os.path.join(folder_path, temp_name),
            )
            temp_names.append((temp_name, filename))  # store mapping

        # shuffle
        original_names = [name for _, name in temp_names]
        random.shuffle(original_names)

        # rename
        for (temp_name, orig), new_name in zip(temp_names, original_names):
            os.rename(
                os.path.join(folder_path, temp_name),
                os.path.join(folder_path, new_name),
            )

    @staticmethod
    def apply_practice_codes():
        os.mkdir(f"{TMP_EXTRACT}/mod")
        shutil.copyfile("./worlds/super_paper_mario/rel/spm-practice-codes.us0.rel", f"{TMP_EXTRACT}/mod/mod.rel")


def output_patch(world: "SuperPaperMarioWorld", output_directory: str):
    options_dict = {
        "randomize_enemies": world.options.randomize_enemies.value,
        "randomize_music": world.options.randomize_music.value,
        "practice_codes": world.options.practice_codes.value,
    }
    patch = SPMProcedurePatch(player=world.player, player_name=world.multiworld.player_name[world.player])
    path = os.path.join(
        output_directory,
        world.multiworld.get_out_file_name_base(world.player) + patch.patch_file_ending,
    )
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))
    patch.write(path)
