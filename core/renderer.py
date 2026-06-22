import pygame as py
from data.tile_colors import TILE_COLORS


class Renderer:
    # Cache surfaces at class level to avoid recreating for multiple renderer instances
    _surfaces_cache = {}
    _cache_tile_size = None
    # Chunk surface cache for small zoom levels (using chunk object id as key)
    _chunk_surfaces_cache = {}
    _chunk_cache_tile_size = None
    CHUNK_CACHE_MIN_TILE_SIZE = 4  # Only cache chunks below this tile size

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
    
    @classmethod
    def _clear_chunk_cache(cls):
        """Clear the chunk surface cache when zoom changes."""
        cls._chunk_surfaces_cache.clear()
        cls._chunk_cache_tile_size = None
    
    def _get_chunk_surface(self, chunk, tile_size):
        """Get or create a pre-rendered surface for a chunk at the given tile_size."""
        if tile_size >= self.CHUNK_CACHE_MIN_TILE_SIZE:
            return None  # Don't cache for larger tile sizes
        
        if tile_size != self._chunk_cache_tile_size:
            self._clear_chunk_cache()
            self._chunk_cache_tile_size = tile_size
        
        chunk_id = id(chunk)
        if chunk_id not in self._chunk_surfaces_cache:
            # Pre-render the entire chunk
            cs = self.world.chunk_size
            chunk_pixel_size = cs * tile_size
            surf = py.Surface((chunk_pixel_size, chunk_pixel_size), py.SRCALPHA)
            
            for y in range(cs):
                for x in range(cs):
                    tile = chunk.get_tile(x, y)
                    if tile is None:
                        continue
                    color = TILE_COLORS.get(tile, (128, 128, 128))
                    if tile_size == 1:
                        surf.set_at((x, y), color)
                    else:
                        py.draw.rect(surf, color, (x * tile_size, y * tile_size, tile_size, tile_size))
            
            surf = surf.convert_alpha()
            self._chunk_surfaces_cache[chunk_id] = surf
        
        return self._chunk_surfaces_cache[chunk_id]

    def draw_chunk(self, screen, chunk, cx, cy, camera):
        ts = self.world.tile_size
        cs = self.world.chunk_size

        # Try to use pre-rendered chunk surface at small zoom levels
        chunk_surf = self._get_chunk_surface(chunk, ts)
        if chunk_surf is not None:
            # Draw the pre-rendered chunk surface
            screen_x = cx * cs * ts - camera.x
            screen_y = cy * cs * ts - camera.y
            screen.blit(chunk_surf, (screen_x, screen_y))
            return

        # Fall back to per-tile rendering for larger tile sizes
        base_x = cx * cs * ts
        base_y = cy * cs * ts
        
        # Pre-calculate screen bounds to skip off-screen tiles
        screen_width, screen_height = screen.get_size()

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
        if self.machine_manager is not None:
            self.machine_manager.draw(screen, camera)