import pygame as py
from data.tile_colors import TILE_COLORS


class Renderer:
    # Cache surfaces at class level to avoid recreating for multiple renderer instances
    _surfaces_cache = {}
    _cache_tile_size = None

    def __init__(self, world, machine_manager):
        self.world = world
        self.machine_manager = machine_manager
        self.tile_surfaces = self._get_surfaces(world.tile_size)

    @classmethod
    def _get_surfaces(cls, tile_size):
        """Get or create cached tile surfaces."""
        if tile_size != cls._cache_tile_size or not cls._surfaces_cache:
            cls._surfaces_cache = {}
            for tile, color in TILE_COLORS.items():
                surf = py.Surface((tile_size, tile_size)).convert()
                surf.fill(color)
                cls._surfaces_cache[tile] = surf
            cls._cache_tile_size = tile_size
        return cls._surfaces_cache

    def draw_chunk(self, screen, chunk, cx, cy, camera):
        ts = self.world.tile_size
        cs = self.world.chunk_size

        base_x = cx * cs * ts
        base_y = cy * cs * ts
        
        # Pre-calculate screen bounds to skip off-screen tiles
        screen_width, screen_height = screen.get_size()
        """
        min_screen_x = int(camera.x)
        max_screen_x = min_screen_x + screen_width
        min_screen_y = int(camera.y)
        max_screen_y = min_screen_y + screen_height
        """

        for y in range(chunk.size):
            for x in range(chunk.size):
                tile = chunk.get_tile(x, y)
                
                if tile is None:
                    continue
                
                screen_x = base_x + x * ts - camera.x
                screen_y = base_y + y * ts - camera.y
                
                # Skip tiles completely outside screen
                if screen_x + ts < 0 or screen_x >= screen_width or screen_y + ts < 0 or screen_y >= screen_height:
                    continue

                screen.blit(self.tile_surfaces[tile], (screen_x, screen_y))

    def draw_world(self, screen, world, camera):
        width, height = screen.get_size()
        start_x, start_y, end_x, end_y = world.visible_chunk_range(camera, width, height)

        for cy in range(start_y, end_y + 1):
            for cx in range(start_x, end_x + 1):
                chunk = world.get_chunk(cx, cy)
                self.draw_chunk(screen, chunk, cx, cy, camera)
        
        self.draw_machines(screen, camera)
        
    def draw_machines(self, screen, camera):
        if self.machine_manager is None:
            return

        draw_method = getattr(self.machine_manager, 'draw', None)
        if callable(draw_method):
            draw_method(screen, camera)