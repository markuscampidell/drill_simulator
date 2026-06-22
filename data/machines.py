import pygame as py

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

    def bounds(self, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        return (x, y, x + self.width, y + self.height)

    @property
    def is_miner(self):
        return self.name.lower() == "miner"

    def update(self, dt):
        pass

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
        return Machine(self.name, self.width, self.height)

MACHINES = {
    "miner": Machine("Miner", width=1, height=1),
    "furnace": Machine("Furnace", width=2, height=2),
    "assembler": Machine("Assembler", width=3, height=3),
}


def create_machine(machine_key):
    prototype = MACHINES.get(machine_key)
    if prototype is None:
        raise KeyError(f"Unknown machine key: {machine_key}")
    return prototype.clone()
