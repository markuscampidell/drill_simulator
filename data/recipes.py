class Recipe:
    def __init__(self, name: str, inputs_per_minute: dict, outputs_per_minute: dict):
        self.name = name
        self.inputs_per_minute = inputs_per_minute  # dict of item -> quantity
        self.outputs_per_minute = outputs_per_minute  # dict of item -> quantity

RECIPES = {
    # Processed Ores
    "iron_ingot_recipe": Recipe("Iron Ingot", {"iron_ore": 60, "coal": 30}, {"iron_ingot": 30}),
    "stone_brick_recipe": Recipe("Stone Brick", {"stone": 240, "coal": 60}, {"stone_brick": 60}),

    # Basic Components
    "iron_plate_recipe": Recipe("Iron Plate", {"iron_ingot": 60}, {"iron_plate": 60}),
    "iron_gear_recipe": Recipe("Iron Gear", {"iron_ingot": 120}, {"iron_gear": 120}),
    "copper_wire_recipe": Recipe("Copper Wire", {"copper_ore": 60}, {"copper_wire": 120}),
}