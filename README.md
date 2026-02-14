# Super Paper Mario: APWorld

## Development Notes

### APWorld Assumptions

The following are assumptions I've made about what changes will be modded into
the game for the sake of randomization. I've kept development of the apworld
going under these assumptions. Should any of these need to change then the
APWorld will also need updating.

The save file starts at what *would* be Sequence 11 and the flags listed in `save.py` set.

Other changes required for logic:
- 2 Elevators in Flipside require a specific sequence to be used. One uses 53 another 73
- Waking up Peach in Flipside shouldn't require a Spicy Soup. There'd be an awkward single Spicy Soup in the progression pool if it has to.
- 3 sets of keys are used in different ways, they should probably be changed to work the same to make logic consistent. Whichever way that is, doesn't particularly matter
    - The 3 Ruins keys all share one item id but set Sequence values when picking up. Either change the 3 sets of keys to not depend on the sequence and ensure the keys are interchangeable between doors or...
    - The 3 Fort keys & 3 Dimension keys all use their own unique id. Change the Ruins keys to have their own unique ids as well so they can only be used on specific doors.
- afaik, The Empty Goldfish Bowl & Helmet are more or less the same item logically. The bowl just changes into the helmet when transitioning to chapter 4-1. The chapter 4-1 entrance should probably just check for helmet only with the Empty Goldfish Bowl never being added to the item pool.
- Not sure if shop items will be randomizable but I'm going to assume they will be and always randomize them (more sphere 1 checks in flipside makes *early* testing of logic easier)
- Thoreau has a weird quirk of being thrown relative to the character's height. In chapter 1-3 & 1-4 there's a required thoreau check through a one vertical tile gap. Mario being a short king is the only one who can throw Thoreau through the gap. Pls fix so every character throws him at Mario's height.
- I've added a setting for Ability Shuffle. This adds Mario's Flip, Peach's Umbrella, Bowser's Fire Breath & Luigi's Super Jump to the pool. I assume this can easily be enabled in a mod by hijacking the `no skills` status used by Tech Cursyas. See [this](https://github.com/SeekyCt/spm-headers/blob/fe1e8d94807614e20cfb41a82b8fc519341c53a2/include/spm/mario.h#L302) status flag.
- All of the logic is being written on the assumption that Entrance Rando will *eventually* be possible. No big deal if it isn't but... pls.

There may be other minor considerations for the mod's development. Search the codebase for `MOD:` and to see all my reminder notes for these.
