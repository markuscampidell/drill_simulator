class Recipe:
    def __init__(self, name: str, inputs: dict, outputs: dict, time: float):
        self.name = name
        self.inputs = inputs  # dict of item -> quantity
        self.outputs = outputs  # dict of item -> quantity
        self.time = time  # time in seconds to complete the recipe

RECIPES = {
    """Basic items"""

    "iron_ingot_recipe": Recipe("Iron Ingot", {"iron_ore": 2, "coal": 1}, {"iron_ingot": 1}, 2.0),
    "stone_brick_recipe": Recipe("Stone Brick", {"stone": 4, "coal": 1}, {"stone_brick": 1}, 1.0),


    """Machines"""
    "furnace_recipe": Recipe("Furnace", {"stone_brick": 8, "iron_ingot": 4}, {"furnace": 1}, 5.0),
}