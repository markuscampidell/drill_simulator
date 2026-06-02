import random

from generation.chunk_gen import ChunkGenerator


class World:
    """Simple world chunk cache and coordinate system.
    
    Delegates generation to ChunkGenerator.
    """

    def __init__(self, chunk_size=32, tile_size=32, region_size=128, seed=None):
        self.chunk_size = chunk_size
        self.tile_size = tile_size
        self.region_size = region_size

        self.seed = seed or random.randint(0, 999999)

        self.chunks = {}
        self.generator = ChunkGenerator(self.seed, chunk_size, region_size)

    def get_chunk(self, cx, cy):
        """Get or generate a chunk at (cx, cy)."""
        pos = (cx, cy)

        if pos not in self.chunks:
            self.chunks[pos] = self.generator.generate(cx, cy)

        return self.chunks[pos]

    def get_tile(self, x, y):
        """Get a tile from world coordinates."""
        cx, local_x = divmod(x, self.chunk_size)
        cy, local_y = divmod(y, self.chunk_size)

        chunk = self.get_chunk(cx, cy)
        return chunk.get_tile(local_x, local_y)

    def visible_chunk_range(self, camera, screen_width, screen_height):
        """Calculate which chunk coordinates are visible in camera."""
        tile_left = int(camera.x) // self.tile_size
        tile_top = int(camera.y) // self.tile_size

        tile_right = (int(camera.x) + screen_width) // self.tile_size
        tile_bottom = (int(camera.y) + screen_height) // self.tile_size

        return (tile_left // self.chunk_size,
                tile_top // self.chunk_size,
                tile_right // self.chunk_size,
                tile_bottom // self.chunk_size)