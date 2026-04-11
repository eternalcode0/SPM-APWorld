from .data.item_data import ItemData
from .data.location_data import LocationData
from .names import ItemName
from .options import SuperPaperMarioOptions
from .types import SPMWorldBase


class SPMFillPlan:
    """The Fill Plan is responsible for tallying the required item and
    location pools, then projecting various item placements from options.
    It can then be queried for things such as valid options, the amount of
    filler items required & necessary location changes. Afterwards it can
    perform basic fill operations like placing locked items
    """

    world: SPMWorldBase
    options: SuperPaperMarioOptions

    # Item related variables
    base_pool = set[ItemData]
    filler_weights = dict[ItemName, int]

    # World related variables
    static_world_locations = set[LocationData]

    def __init__(self, world: SPMWorldBase):
        self.world = world
        self.options = world.options

    def plan(world: SPMWorldBase):
        pass
