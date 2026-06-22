from data.recipes import RECIPES

class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value

# Raw ore items
ITEMS = {
    "stone": Item("Stone", 1),
    "coal": Item("Coal", 1),
    "iron_ore": Item("Iron Ore", 1),
    "copper_ore": Item("Copper Ore", 1),
}

def calculate_item_value(recipe_key):
    if recipe_key not in RECIPES:
        return 0

    recipe = RECIPES[recipe_key]

    total_input_value_per_minute = 0

    # Value of all consumed resources per minute
    for item, amount_per_minute in recipe.inputs_per_minute.items():
        if item not in ITEMS:
            return 0

        total_input_value_per_minute += (
            ITEMS[item].value * amount_per_minute
        )

    # Total produced items per minute
    total_output_per_minute = sum(
        recipe.outputs_per_minute.values()
    )

    if total_output_per_minute == 0:
        return 0

    return total_input_value_per_minute / total_output_per_minute

# Processed items and machines
ITEMS.update({
    "iron_ingot": Item("Iron Ingot", calculate_item_value("iron_ingot_recipe")),
    "stone_brick": Item("Stone Brick", calculate_item_value("stone_brick_recipe")),
})

# Basic components
ITEMS.update({
    "iron_plate": Item("Iron Plate", calculate_item_value("iron_plate_recipe")),
    "iron_gear": Item("Iron Gear", calculate_item_value("iron_gear_recipe")),
    "copper_wire": Item("Copper Wire", calculate_item_value("copper_wire_recipe")),
})