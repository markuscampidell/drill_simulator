import pygame as py

from data.machines import create_machine

class MachineManager:
    ORE_TILES = {"iron", "gold", "coal", "stone"}

    def __init__(self, world=None):
        self.machines = []
        self.world = world

    def add_machine(self, machine, x, y):
        if isinstance(machine, str):
            machine = create_machine(machine)

        x -= (machine.width - 1) // 2
        y -= (machine.height - 1) // 2

        if not self.validate_position(machine, x, y):
            return False

        if not self.validate_miner_position(machine, x, y):
            return False

        machine.x = x
        machine.y = y
        self.machines.append(machine)
        return True

    def update(self, dt):
        for machine in self.machines:
            machine.update(dt)

    def draw(self, screen, camera):
        tile_size = self.world.tile_size if self.world is not None else 16
        screen_rect = screen.get_rect()

        for machine in self.machines:
            # Calculate screen position
            screen_x = machine.x * tile_size - camera.x
            screen_y = machine.y * tile_size - camera.y
            width = machine.width * tile_size
            height = machine.height * tile_size
            
            # Cull off-screen machines
            if screen_x + width < 0 or screen_x >= screen_rect.width or screen_y + height < 0 or screen_y >= screen_rect.height:
                continue
            
            # Get cached surface and blit directly
            surf = machine._get_surface(tile_size)
            screen.blit(surf, (screen_x, screen_y))

    def validate_miner_position(self, machine, x, y):
        if not getattr(machine, "is_miner", False):
            return True

        if self.world is None:
            raise ValueError("MachineManager needs a world reference to validate miner placement")

        for tile_x, tile_y in self._machine_tiles(machine, x, y):
            if self._is_adjacent_to_ore(tile_x, tile_y):
                return True

        return False

    def validate_position(self, machine, x, y):
        new_left, new_top, new_right, new_bottom = machine.bounds(x, y)

        for existing in self.machines:
            left, top, right, bottom = existing.bounds()
            if (new_left < right and new_right > left and
                new_top < bottom and new_bottom > top):
                return False

        return True

    def _machine_tiles(self, machine, x, y):
        return (
            (tile_x, tile_y)
            for tile_y in range(y, y + machine.height)
            for tile_x in range(x, x + machine.width)
        )

    def _is_adjacent_to_ore(self, tile_x, tile_y):
        if self._is_ore(self.world.get_tile(tile_x, tile_y)):
            return True

        neighbors = [
            (tile_x - 1, tile_y),
            (tile_x + 1, tile_y),
            (tile_x, tile_y - 1),
            (tile_x, tile_y + 1),
        ]

        return any(self._is_ore(self.world.get_tile(nx, ny)) for nx, ny in neighbors)

    def _is_ore(self, tile):
        return tile in self.ORE_TILES
