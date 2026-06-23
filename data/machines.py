import pygame as py

from data.recipes import RECIPES

MACHINE_COLORS = {
    "Miner": (220, 220, 80),
    "Furnace": (220, 120, 80),
    "Assembler": (100, 180, 240),
}

_machine_surface_cache = {}

class Machine:
    def __init__(self, name, width=1, height=1):
        self.name = name
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.color = MACHINE_COLORS.get(name, (180, 180, 180))
        self.recipe = None  # Recipe this machine is running
        self.allowed_recipes = []

    def bounds(self, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        return (x, y, x + self.width, y + self.height)

    @property
    def is_miner(self):
        return self.name.lower() == "miner"


    def can_run(self, recipe_key):
        return recipe_key in self.allowed_recipes

    def set_recipe(self, recipe):
        if not self.can_run(recipe.key):
            raise ValueError(
                f"{self.name} cannot run recipe {recipe.key}"
            )

        self.recipe = recipe

    def _get_surface(self, tile_size):
        key = (self.name, self.width, self.height, tile_size)
        surf = _machine_surface_cache.get(key)
        if surf is None:
            surf = py.Surface((self.width * tile_size, self.height * tile_size), py.SRCALPHA)
            surf.fill(self.color)
            surf = surf.convert_alpha()  # Convert for faster blitting
            _machine_surface_cache[key] = surf
        return surf

    def __repr__(self):
        return (
            f"Machine(name={self.name!r}, width={self.width}, height={self.height}, "
            f"x={self.x}, y={self.y})"
        )

    def clone(self):
        return self.__class__()

    def get_available_recipes(self):
        return [
            RECIPES[key]
            for key in self.allowed_recipes
            if key in RECIPES
        ]


class Miner(Machine):
    def __init__(self):
        super().__init__("Miner", width=1, height=1)

        self.allowed_recipes = [
            "iron_ore_recipe",
            "copper_ore_recipe",
            "stone_recipe",
            "coal_recipe",
            ]

class Furnace(Machine):
    def __init__(self):
        super().__init__("Furnace", width=2, height=2)
        
        self.allowed_recipes = [
                "iron_ingot_recipe",
                "copper_ingot_recipe",
                "stone_brick_recipe",
                ]

class Assembler(Machine):
    def __init__(self):
        super().__init__("Assembler", width=3, height=3)
        
        self.allowed_recipes = [
                "iron_plate_recipe",
                "iron_gear_recipe",
                "copper_wire_recipe",
                ]


MACHINE_CLASSES = {
    "miner": Miner,
    "furnace": Furnace,
    "assembler": Assembler,
}


def create_machine(machine_key):
    machine_class = MACHINE_CLASSES.get(machine_key)

    if machine_class is None:
        raise KeyError(f"Unknown machine: {machine_key}")

    return machine_class()