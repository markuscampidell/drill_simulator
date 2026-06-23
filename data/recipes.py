class Recipe:
    def __init__(self, key, name, inputs_per_second, outputs_per_second):
        self.key = key
        self.name = name
        self.inputs_per_second = inputs_per_second
        self.outputs_per_second = outputs_per_second

RECIPES = {
    # Raw Ores

    "iron_ore_recipe": Recipe("iron_ore_recipe", "Iron Ore", {}, {"iron_ore": 1.0}),
    "copper_ore_recipe": Recipe("copper_ore_recipe", "Copper Ore", {}, {"copper_ore": 1.0}),
    "stone_recipe": Recipe("stone_recipe", "Stone", {}, {"stone": 1.0}),
    "coal_recipe": Recipe("coal_recipe", "Coal", {}, {"coal": 1.0}),

    # Processed Ores
    "iron_ingot_recipe": Recipe("iron_ingot_recipe", "Iron Ingot", {"iron_ore": 1.0, "coal": 0.5}, {"iron_ingot": 0.5}),
    "copper_ingot_recipe": Recipe("copper_ingot_recipe", "Copper Ingot", {"copper_ore": 1.0, "coal": 0.5}, {"copper_ingot": 0.5}),
    "stone_brick_recipe": Recipe("stone_brick_recipe", "Stone Brick", {"stone": 4.0, "coal": 1.0}, {"stone_brick": 1.0}),

    # Basic Components
    "iron_plate_recipe": Recipe("iron_plate_recipe", "Iron Plate", {"iron_ingot": 1.0}, {"iron_plate": 1.0}),
    "iron_gear_recipe": Recipe("iron_gear_recipe", "Iron Gear", {"iron_ingot": 2.0}, {"iron_gear": 2.0}),
    "copper_wire_recipe": Recipe("copper_wire_recipe", "Copper Wire", {"copper_ore": 1.0}, {"copper_wire": 2.0}),
}