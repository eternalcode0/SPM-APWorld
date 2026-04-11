"""Defines the set of game items and item pools"""

from BaseClasses import ItemClassification

from .data import item_data
from .names import ItemName
from .types import SPMItem, SPMWorldBase

ITEM_ENUM_TO_DATA: dict[ItemName, item_data.ItemData] = {
    data.name: data for data in item_data.ITEM_DATA if data.code is not None
}
ITEM_NAME_TO_ID: dict[str, int] = {name.value: data.code for name, data in ITEM_ENUM_TO_DATA.items()}
ITEM_GROUPS: set[str] = {group for item in item_data.ITEM_DATA for group in item.groups}
ITEM_GROUP_MAP: dict[str, set[str]] = {
    group: {item.name.value for item in item_data.ITEM_DATA if group in item.groups} for group in ITEM_GROUPS
}


CHARACTERS = [hero.name for hero in item_data.ITEM_DATA if "Hero" in hero.groups]
PIXLS = [pixl.name for pixl in item_data.ITEM_DATA if "Pixl" in pixl.groups]
CHAPTER_KEYS = list(ITEM_GROUP_MAP["Chapter Key"])
SUBCHAPTER_KEYS = list(ITEM_GROUP_MAP["Subchapter Key"])


def create_items(world: SPMWorldBase) -> list[SPMItem]:
    items = []

    for idata in item_data.ITEM_DATA:
        amount = idata.amount if not callable(idata.amount) else idata.amount(world)
        # Don't add the starting character/pixl or filler to the base pool
        if idata.name in world.starting_pair or idata.classification == ItemClassification.filler:
            continue
        if amount > 0:
            items.extend(world.create_item(idata.name) for _ in range(0, amount))

    return items


def create_item(world: SPMWorldBase, item_name: ItemName) -> SPMItem:
    data = ITEM_ENUM_TO_DATA[item_name]
    clazz = data.classification if not callable(data.classification) else data.classification(world.options)
    return SPMItem(item_name, clazz, data.code, world.player)


def override_filler_options(world: SPMWorldBase) -> None:
    for item_name, weight in world.options.filler_weights.items():
        item_name = ItemName(item_name)
        data = ITEM_ENUM_TO_DATA[item_name]
        clazz = data.classification if not callable(data.classification) else data.classification(world.options)
        if not (clazz == ItemClassification.filler or clazz == ItemClassification.trap):
            continue
        world.filler_options[item_name] = weight
