"""All types related to the yaml options and presets"""

from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Range, Toggle


class Goal(Choice):
    """
    **Dimentio:** You goal when you defeat Super Dimentio in Chapter 8-4.
        Set "Pure Hearts Required" to access 8-4 eariler.
    """
    display_name = "Goal"
    rich_text_doc = True

    option_dimentio = 0  # Defeat Super Dimentio after collecting all the Pure Hearts
    # option_cards = 1  # Catch Card Hunt
    # option_wracktail = 2  # Clear the Flipside Pit of 100 Trials
    # option_shadoo = 4  # Clear the Flopside Pit of 100 Trials (flopside pit should prob always need only 1 clear)
    default = option_dimentio


class PureHeartsRequired(Range):
    """How many pure hearts are required to goal and/or enter 8-4?"""
    display_name = "Pure Hearts Required"
    rich_text_doc = True

    range_start = 1
    range_end = 8
    default = 8


class ShufflePureHearts(Toggle):
    """Should Pure Hearts get placed anywhere in the multiworld?"""
    display_name = "Shuffle Pure Hearts"


class ChapterKeysLock(Choice):
    """
    Do Chapter Keys lock access to specific chapters or subchapters?

    **Open:** Chapter Keys are not placed in the pool, every chapter is unlocked from the start.

    **Chapter Locked:** Chapter Keys unlock all subchapters of a given chapter.
        They will be named without their subchapter number, Ex. Chapter 1 Key

    **Subchapters Locked:** Chapter Keys unlock a single given subchapter.
        They will be named with their subchapter number, Ex. Chapter 1-1 Key
    """
    display_name = "Chapter Keys Lock"
    rich_text_doc = True

    option_open = 0
    option_chapter_locked = 1
    option_subchapters_locked = 2
    # option_closed = 3  # no chapters accessible, some kind of pit only goal maybe?
    default = option_open


class StartingCharacter(Choice):
    """Which character will you start as?"""
    display_name = "Starting Character"

    default = "random"
    option_mario = 0
    option_peach = 1
    option_bowser = 2
    option_luigi = 3


class StartingPixl(Choice):
    """Which pixl will you start with?"""
    display_name = "Starting Pixl"

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
    option_barry = 9
    option_dashell = 10
    option_piccolo = 11


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
    default = PitAccess.option_closed


class FlipsidePitLogic(PitLogic):
    """When is each individual floor of the Flipside Pit considered in-logic?
    *Minimum:* Each floor of the Pit is considered in-logic as soon as the enemies of that floor are defeatable.
        Ex. Floor 1-12 will be in-logic once the pit is accessible but Floor 13+ will be considered out-of-logic until
        you have Boomer to defeat the Shlurps.

    *Characters:* Every floor is considered out-of-logic until you have all Heroes & Pixls

    *Chapters:* Every floor is considered out-of-logic until you have access to Chapters 1-7

    *Maximum:* Every floor is considered out-of-logic until you have all Heroes, Pixls, and access to Chapters 1-7
    """
    default = PitLogic.option_minimum


class FlopsidePitAccess(PitAccess):
    """When is the first floor of Flopside's Pit accessible? Following floors use the setting from Flopside Pit Logic.
    *Closed:* Flopside Pit is never accessible, the pipe doesn't work.

    *Open:* The rift above the pipe has already been Fleep'd from the beginning of the save file.

    *Normal:* Access to Flopside Pit requires beating the Flipside Pit then Fleep'ing the rift above the pipe.

    *No Flipside:* The rift is available before the Flipside Pit is completed.
        Access to Flopside Pit only requires Fleep'ing the rift.
    """
    option_no_flipside = 3
    default = PitAccess.option_closed


class FlopsidePitLogic(PitLogic):
    """
    *Minimum:* Each floor of the Pit is considered in-logic as soon as the enemies of that floor are defeatable.
        Ex. Floor 1-4 will be in-logic once the pit is accessible but Floor 5+ will be considered out-of-logic until
        you have Carrie, Boomer, or Bowser to kill the Dark Spiked Goombas.

    *Characters:* Every floor is considered out-of-logic until you have all Heroes & Pixls

    *Chapters:* Every floor is considered out-of-logic until you have access to Chapters 1-7

    *Maximum:* Every floor is considered out-of-logic until you have all Heroes, Pixls, and access to Chapters 1-7
    """
    default = PitLogic.option_minimum


class Traps(Choice):
    """Adds the various cursya traps to the item pool

    *None*: No cursya traps are added to the pool.

    *Some*: Adds the Slow, Heavy, Reverse, and Tech Cursya traps to the pool.

    *All*: Adds all the above traps as well as the Back Cursya trap to the pool.
    """
    display_name = "Cursya Traps"
    rich_text_doc = True

    option_none = 0
    option_some = 1
    option_all = 2
    alias_false = option_none
    alias_true = option_some
    default = option_none


class EntranceRando(Toggle):
    """Do you want entrances to be randomized?
    Doesn't randomize small buildings / entrances that use the spinning black square transition.
    Doesn't randomize the Chapter doors.
    """
    display_name = "Entrance Randomization"


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

    value_shuffle = 0b0_00
    value_random = 0b1_00
    value_same_difficulty = 1
    value_similar_difficulty = 2
    value_any_difficulty = 3

    option_vanilla = 0
    option_shuffle_same_difficulty = value_same_difficulty
    option_shuffle_similar_difficulty = value_similar_difficulty
    option_shuffle_any_difficulty = value_any_difficulty
    option_random_same_difficulty = value_same_difficulty | value_random
    option_random_similar_difficulty = value_similar_difficulty | value_random
    option_random_any_difficulty = value_any_difficulty | value_random
    default = option_vanilla


@dataclass
class SuperPaperMarioOptions(PerGameCommonOptions):
    goal: Goal
    pure_hearts_required: PureHeartsRequired
    chapter_keys_lock: ChapterKeysLock
    starting_character: StartingCharacter
    starting_pixl: StartingPixl
    shuffle_pure_hearts: ShufflePureHearts
    flipside_pit_access: FlipsidePitAccess
    flipside_pit_logic: FlipsidePitLogic
    flopside_pit_access: FlopsidePitAccess
    flopside_pit_logic: FlopsidePitLogic
    traps: Traps
    # randomize_entrances: EntranceRando
    # randomize_enemies: EnemyRando
