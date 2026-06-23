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
    recipe = RECIPES.get(recipe_key)

    if recipe is None:
        return 0

    try:
        total_input_value = sum(
            ITEMS[item].value * amount
            for item, amount in recipe.inputs_per_second.items()
        )
    except KeyError:
        return 0

    total_output = sum(recipe.outputs_per_second.values())

    return total_input_value / total_output if total_output > 0 else 0

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