from test.bases import WorldTestBase

from ..data import GAME
from ..world import SuperPaperMarioWorld


class SPMTestBase(WorldTestBase):
    game = GAME
    world: SuperPaperMarioWorld
