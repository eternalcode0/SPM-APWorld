"""All types related to the yaml options and presets"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from Options import Choice, ItemDict, ItemSet, OptionGroup, PerGameCommonOptions, Range, Toggle, Visibility

from .names import ItemName


class Goal(Choice):
    """
    **Dimentio:** You goal when you defeat Super Dimentio in Chapter 8-4.
        Set "Pure Hearts Required" to access 8-4 eariler.
    """

    display_name = "Goal"
    internal_name = "goal"

    option_dimentio = 0  # Defeat Super Dimentio after collecting all the Pure Hearts
    # option_cards = 1  # Catch Card Hunt
    # option_wracktail = 2  # Clear the Flipside Pit of 100 Trials
    # option_shadoo = 4  # Clear the Flopside Pit of 100 Trials (flopside pit should prob always need only 1 clear)
    default = option_dimentio


class PureHeartsRequired(Range):
    """How many pure hearts are required to goal and/or enter 8-4?"""

    display_name = "Pure Hearts Required"
    internal_name = "pure_hearts_required"

    range_start = 1
    range_end = 8
    default = 8


class ChapterDoorAccess(Choice):
    """
    Do Chapter Keys lock access to specific chapters or subchapters?

    **Open:** Chapter Keys are not placed in the pool, every chapter is unlocked from the start.

    **Chapter Locked:** Chapter Keys unlock all subchapters of a given chapter.
        They will be named without their subchapter number, Ex. Chapter 1 Key

    **Subchapters Locked:** Chapter Keys unlock a single given subchapter.
        They will be named with their subchapter number, Ex. Chapter 1-1 Key
    """

    display_name = "Chapter Door Access"
    internal_name = "chapter_door_access"

    option_open = 0
    # option_chapter_locked = 1
    # option_subchapters_locked = 2
    # option_closed = 3  # no chapters accessible, some kind of pit only goal maybe?
    default = option_open


class ShufflePureHearts(Toggle):
    """Should Pure Hearts get placed anywhere in the multiworld?"""

    display_name = "Shuffle Pure Hearts"
    internal_name = "shuffle_pure_hearts"


class StartingCharacter(Choice):
    """Which character will you start as?"""

    display_name = "Starting Character"
    internal_name = "starting_character"

    default = "random"
    option_mario = 0
    option_peach = 1
    option_bowser = 2
    option_luigi = 3


class StartingPixl(Choice):
    """Which pixl will you start with?"""

    display_name = "Starting Pixl"
    internal_name = "starting_pixl"

    default = "random"
    option_tippi = 0
    option_thoreau = 1
    option_boomer = 2
    option_slim = 3
    option_thudley = 4
    option_carrie = 5
    option_fleep = 6
    option_cudge = 7
    option_dottie = 8
    option_piccolo = 9
    option_barry = 10
    option_dashell = 11


class PitAccess(Choice):
    option_closed = 0
    option_open = 1
    option_normal = 2


class PitLogic(Choice):
    option_minimum = 0b00
    option_characters = 0b01
    option_chapters = 0b10
    option_maximum = 0b11

    @property
    def requires_characters(self) -> bool:
        return bool(self.value & self.option_characters)

    @property
    def requires_chapters(self) -> bool:
        return bool(self.value & self.option_chapters)


class FlipsidePitAccess(PitAccess):
    """When is the first floor of Flipside's Pit accessible? Following floors use the setting from Flipside Pit Logic.

    *Closed:* Flipside Pit is never accessible, the pipe doesn't work.

    *Open:* The switch on top of the cage is already hit and the cage open.
        The first floor may be considered in-logic based off whether minimum, characters, chapters, or goal is set.

    *Normal:* Access to Flipside Pit requires hitting the switch above the cage to open it.
        The first floor may be considered in-logic based off whether minimum, characters, chapters, or goal is set.
    """

    display_name = "Flipside Pit Access"
    internal_name = "flipside_pit_access"

    default = PitAccess.option_closed


# class FlipsidePitLogic(PitLogic):
#     """When is each individual floor of the Flipside Pit considered in-logic?
#     *Minimum:* Each floor of the Pit is considered in-logic as soon as the enemies of that floor are defeatable.
#         Ex. Floor 1-12 will be in-logic once the pit is accessible but Floor 13+ will be considered out-of-logic until
#         you have Boomer to defeat the Shlurps.

#     *Characters:* Every floor is considered out-of-logic until you have all Heroes & Pixls

#     *Chapters:* Every floor is considered out-of-logic until you have access to Chapters 1-7

#     *Maximum:* Every floor is considered out-of-logic until you have all Heroes, Pixls, and access to Chapters 1-7
#     """

#     display_name = "Flipside Pit Logic"
#     internal_name = "flipside_pit_logic"

#     default = PitLogic.option_minimum


class FlopsidePitAccess(PitAccess):
    """When is the first floor of Flopside's Pit accessible? Following floors use the setting from Flopside Pit Logic.
    *Closed:* Flopside Pit is never accessible, the pipe doesn't work.

    *Open:* The rift above the pipe has already been Fleep'd from the beginning of the save file.

    *Normal:* Access to Flopside Pit requires beating the Flipside Pit then Fleep'ing the rift above the pipe.

    *No Flipside:* The rift is available before the Flipside Pit is completed.
        Access to Flopside Pit only requires Fleep'ing the rift.
    """

    display_name = "Flopside Pit Access"
    internal_name = "flopside_pit_access"

    option_no_flipside = 3
    default = PitAccess.option_closed


# class FlopsidePitLogic(PitLogic):
#     """
#     *Minimum:* Each floor of the Pit is considered in-logic as soon as the enemies of that floor are defeatable.
#         Ex. Floor 1-4 will be in-logic once the pit is accessible but Floor 5+ will be considered out-of-logic until
#         you have Carrie, Boomer, or Bowser to kill the Dark Spiked Goombas.

#     *Characters:* Every floor is considered out-of-logic until you have all Heroes & Pixls

#     *Chapters:* Every floor is considered out-of-logic until you have access to Chapters 1-7

#     *Maximum:* Every floor is considered out-of-logic until you have all Heroes, Pixls, and access to Chapters 1-7
#     """

#     display_name = "Flopside Pit Logic"
#     internal_name = "flopside_pit_logic"

#     default = PitLogic.option_minimum


class TrapTypes(ItemSet):
    """Which Traps should be included in the item pool"""

    display_name = "Cursya Traps"
    internal_name = "trap_types"

    valid_keys: Sequence[str] = [
        ItemName.SLOW_CURSYA_TRAP.value,
        ItemName.HEAVY_CURSYA_TRAP.value,
        ItemName.REVERSYA_CURSYA_TRAP.value,
        ItemName.TECH_CURSYA_TRAP.value,
        ItemName.BACK_CURSYA_TRAP.value,
    ]
    default = frozenset(
        {
            ItemName.SLOW_CURSYA_TRAP.value,
            ItemName.HEAVY_CURSYA_TRAP.value,
            ItemName.REVERSYA_CURSYA_TRAP.value,
            ItemName.TECH_CURSYA_TRAP.value,
        }
    )


class FillerWeights(ItemDict):
    """How common should each filler item be?

    Without using this setting, the filler pool will be decided from the amount of items shuffled *out* of its
    vanilla locations. Each item specified in here will override its default amount.
    Cursya Traps can also be listed here."""

    display_name = "Filler Weights"
    internal_name = "filler_weights"


class EntranceRando(Choice):
    """Do you want entrances to be randomized?
    Doesn't randomize small buildings / entrances that use the spinning black square transition.
    """

    display_name = "Entrance Randomization"
    internal_name = "randomize_entrances"
    visibility = Visibility.none

    option_disabled = 0
    option_coupled = 1
    option_disjointed = 2
    default = option_disabled


class EnemyRando(Choice):
    """Should enemies be randomized? Bosses are never randomized, many of them crash the game outside their usual room.

    *Shuffle:* Every type of enemy is swapped with another.
        Ex. Every Goomba might be swapped with a Squig, every Squig with a Boomboxer, etc.

    *Random:* Every enemy is randomized.
        Ex. One Goomba might be replaced with a Squig, another Goomba replaced with a Boomboxer.

    *Same Difficulty:* Attempt to keep enemies difficulty the same as what is replacing them.

    *Similar Difficulty:* Attempt to make enemies relatively more/less difficult than what is replacing them.

    *Any Difficulty:* Enemies can be replaced by any other enemy regardless of difficulty.
    """

    display_name = "Enemy Randomization"
    internal_name = "randomize_enemies"
    visibility = Visibility.none  # hidden until feature complete

    value_shuffle = 0b0_00
    value_random = 0b1_00
    value_same_difficulty = 0b0_01
    value_similar_difficulty = 0b0_10
    value_any_difficulty = 0b0_11

    option_vanilla = 0
    option_shuffle_same_difficulty = value_same_difficulty
    option_shuffle_similar_difficulty = value_similar_difficulty
    option_shuffle_any_difficulty = value_any_difficulty
    option_random_same_difficulty = value_same_difficulty | value_random
    option_random_similar_difficulty = value_similar_difficulty | value_random
    option_random_any_difficulty = value_any_difficulty | value_random
    default = option_vanilla


class MusicRando(Toggle):
    """Do you want the music and sound effects to be randomized?"""

    display_name = "Music Randomization"
    internal_name = "randomize_music"


class PracticeCodes(Toggle):
    """Do you want to enable Seeky's SPM Practice Codes?"""

    # No display name, this should always be hidden
    internal_name = "practice_codes"
    visibility = Visibility.none


class ShuffleAbilities(Toggle):
    """Should each character's ability be randomized into an obtainable item? Adds the following items to the pool:

    - Mario's Flip
    - Peach's Umbrella
    - Bowser's Fire
    - Luigi's Super Jump
    """

    display_name = "Ability Shuffle"
    internal_name = "ability_shuffle"


class ObscureTricks(Toggle):
    """Should logic consider obscure tricks to be required for logic.
    Some examples:

    - Jumping off of enemies, some require using Thoraeu to move the enemy first
    - Mid-air flip jumps to jump around 3d objects
    """

    display_name = "Obscure Tricks"
    internal_name = "obscure_tricks"


# class TrickEnemyJumps(Toggle):
#     """Should logic expect you to jump off enemies to reach higher locations?
#     Some of these may also expect you to use Thoreau to place the enemy in a specific spot first."""
#     display_name = "Enemy Jumps"
#     internal_name = "enemy_jumps"


# class TrickThudleyJumps(Choice):
#     """Should logic expect you to perform mid-air jumps using Thudley?

#     Easy only requires doing the jump once or twice in a row.
#     """
#     display_name = "Thudley Jumps"
#     internal_name = "thudley_jumps"

#     option_disabled = 0
#     option_easy = 1
#     option_hard = 2


class TradingQuest(Toggle):
    """
    Should the Piccolo trading quest items & locations be added to the pool?
    Piccolo will still be in the pool, only the intermediary items/locations are removed.
    """

    display_name = "Trading Quest"
    internal_name = "trading_quest"


class TreasureMaps(Choice):
    """What should Flamm sell and when can Fleep reveal Treasure Map locations?

    - *Disabled*: Flamm doesn't sell anything. Map Items aren't in the item and there are no Treasure spots for Fleep to reveal.
    - *No Flamm and Open Treasures*: Flamm doesn't sell anything. Map Items aren't in the item pool, Fleep can access the Treasure spots without them.
    - *No Flamm and Standard Treasures*: Flamm doesn't sell anything. Map Items are in the item pool, Fleep has to reveal the Treasure spots like normal.
    - *Vanilla*: Flamm sells maps like normal. Fleep requires the Map Item to reveal the Treasure spot.
    - *Only Flamm*: Flamm sells randomized items. Map Items/Treasures aren't in the pool for Fleep to reveal.
    - *Flamm and Open Treasures*: Flamm sells randomized items. Map Items aren't in the pool but Fleep can reveal them anyway.
    - *All*: Flamm sells randomized items. Map Items are in the pool for Fleep to use to reveal Map Treasures.
    """

    display_name = "Treasure Maps"
    internal_name = "treasure_maps"

    value_flamm_disabled = 0b00_00  # Flamm doesn't sell anything
    value_flamm_vanilla = 0b00_01  # Flamm sells the vanilla maps
    value_flamm_random = 0b00_10  # Flamm sells random items
    value_FLAMM_MASK = 0b00_11

    value_treasures_disabled = 0b00_00  # Fleep can't reveal map locations, they're disabled in the location pool
    value_treasures_open = 0b01_00  # Fleep doesn't require the map to reveal treasures
    value_treasures_standard = 0b10_00  # Treasure locations work as normal, requiring the map to reveal
    value_TREASURES_MASK = 0b11_00

    option_disabled = value_flamm_disabled | value_treasures_disabled
    option_no_flamm_and_open_treasures = value_flamm_disabled | value_treasures_open
    option_no_flamm_and_standard_treasures = value_flamm_disabled | value_treasures_standard
    # If fleep treasures are disabled, there's no point to flamm having vanilla maps
    # If fleep treasures are open, there's no point to flamm having vanilla maps
    option_vanilla = value_flamm_vanilla | value_treasures_standard
    option_flamm_and_no_treasures = value_flamm_random | value_treasures_disabled
    option_flamm_and_open_treasures = value_flamm_random | value_treasures_open
    option_all = value_flamm_random | value_treasures_standard

    default = option_disabled

    @property
    def flamm_disabled(self) -> bool:
        return self.value & self.value_FLAMM_MASK == self.value_flamm_disabled

    @property
    def flamm_vanilla(self) -> bool:
        return self.value & self.value_FLAMM_MASK == self.value_flamm_vanilla

    @property
    def flamm_random(self) -> bool:
        return self.value & self.value_FLAMM_MASK == self.value_flamm_random

    @property
    def treasures_disabled(self) -> bool:
        return self.value & self.value_TREASURES_MASK == self.value_treasures_disabled

    @property
    def treasures_open(self) -> bool:
        return self.value & self.value_TREASURES_MASK == self.value_treasures_open

    @property
    def treasures_standard(self) -> bool:
        return self.value & self.value_TREASURES_MASK == self.value_treasures_standard

    @property
    def map_items_in_pool(self) -> bool:
        return self.value in {self.option_no_flamm_and_standard_treasures, self.option_all, self.option_vanilla}


@dataclass
class SuperPaperMarioOptions(PerGameCommonOptions):
    # World Access
    goal: Goal
    pure_hearts_required: PureHeartsRequired
    chapter_door_access: ChapterDoorAccess
    # Item Pool
    starting_character: StartingCharacter
    starting_pixl: StartingPixl
    ability_shuffle: ShuffleAbilities
    filler_weights: FillerWeights
    # Item Shuffle
    shuffle_pure_hearts: ShufflePureHearts
    # Location Shuffle
    trading_quest: TradingQuest
    # treasure_maps: TreasureMaps
    # Pit of 100 Trials
    flipside_pit_access: FlipsidePitAccess
    # flipside_pit_logic: FlipsidePitLogic
    flopside_pit_access: FlopsidePitAccess
    # flopside_pit_logic: FlopsidePitLogic
    # Other Randomization
    randomize_entrances: EntranceRando
    randomize_enemies: EnemyRando
    randomize_music: MusicRando
    # Logic
    # obscure_tricks: ObscureTricks
    # Hidden
    practice_codes: PracticeCodes


# TODO: send help, I suck at coming up with option group names.
# particularly "Location Shuffle" & "Item/Location Pool"
OPTION_GROUPS = [
    OptionGroup("World Access", [Goal, PureHeartsRequired, ChapterDoorAccess]),
    OptionGroup("Item Pool", [StartingCharacter, StartingPixl, ShuffleAbilities, FillerWeights]),
    OptionGroup("Item Shuffle", [ShufflePureHearts]),
    OptionGroup("Location Shuffle", [TradingQuest, TreasureMaps]),
    OptionGroup("Pit of 100 Trials", [FlipsidePitAccess, FlopsidePitAccess]),
    OptionGroup(
        "Logic",
        [ObscureTricks],
    ),
    OptionGroup("Other Randomization", [EntranceRando, EnemyRando, MusicRando]),
]

OPTION_PRESETS: dict[str, dict[str, Any]] = {
    "easy": {Goal.internal_name: Goal.option_dimentio, PureHeartsRequired.internal_name: 4}
}
