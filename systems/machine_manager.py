import pygame as py

from data.machines import create_machine

class MachineManager:
    ORE_TILES = {"iron", "copper", "coal", "stone"}
    SPATIAL_GRID_SIZE = 16  # Group machines into 16x16 tile chunks

    def __init__(self, world=None, production_system=None):
        self.machines = []
        self.world = world
        self.production_system = production_system
        self.spatial_grid = {}  # Dict of {(grid_x, grid_y): [machines]}

    def _get_grid_cells(self, x, y, width, height):
        """Get all grid cells that a machine occupies."""
        cells = set()
        for gx in range(x // self.SPATIAL_GRID_SIZE, (x + width - 1) // self.SPATIAL_GRID_SIZE + 1):
            for gy in range(y // self.SPATIAL_GRID_SIZE, (y + height - 1) // self.SPATIAL_GRID_SIZE + 1):
                cells.add((gx, gy))
        return cells

    def _add_to_spatial_grid(self, machine):
        """Add machine to spatial grid."""
        cells = self._get_grid_cells(machine.x, machine.y, machine.width, machine.height)
        for cell in cells:
            if cell not in self.spatial_grid:
                self.spatial_grid[cell] = []
            self.spatial_grid[cell].append(machine)

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
        self._add_to_spatial_grid(machine)
        
        # Register with production system if available
        if self.production_system is not None:
            self.production_system.register_machine(machine)
        
        return True

    def update(self, dt):
        for machine in self.machines:
            machine.update(dt)

    def draw(self, screen, camera):
        if self.world is None:
            tile_size = 16
        else:
            tile_size = self.world.tile_size

        screen_rect = screen.get_rect()
        screen_width = screen_rect.width
        screen_height = screen_rect.height

        # Calculate visible grid cells
        start_gx = int(camera.x // (self.SPATIAL_GRID_SIZE * tile_size))
        start_gy = int(camera.y // (self.SPATIAL_GRID_SIZE * tile_size))
        end_gx = int((camera.x + screen_width) // (self.SPATIAL_GRID_SIZE * tile_size)) + 1
        end_gy = int((camera.y + screen_height) // (self.SPATIAL_GRID_SIZE * tile_size)) + 1

        # Only iterate visible grid cells
        for gx in range(start_gx, end_gx + 1):
            for gy in range(start_gy, end_gy + 1):
                grid_machines = self.spatial_grid.get((gx, gy), [])
                for machine in grid_machines:
                    # Calculate screen position
                    screen_x = machine.x * tile_size - camera.x
                    screen_y = machine.y * tile_size - camera.y
                    width = machine.width * tile_size
                    height = machine.height * tile_size
                    
                    # Quick culling check (should all be visible, but double-check)
                    if screen_x + width < 0 or screen_x >= screen_width or screen_y + height < 0 or screen_y >= screen_height:
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
