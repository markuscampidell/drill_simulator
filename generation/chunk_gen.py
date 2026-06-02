from core.chunk import Chunk
from generation.ore_gen import OreGenerator


class ChunkGenerator:
    """Generates chunks using ore patches."""

    def __init__(self, seed, chunk_size, region_size):
        self.seed = seed
        self.chunk_size = chunk_size
        self.region_size = region_size
        self.ore_gen = OreGenerator(seed, region_size)

    def generate(self, chunk_x, chunk_y):
        """Generate a chunk at the given chunk coordinates."""
        chunk = Chunk(self.chunk_size, default_tile="grass")

        chunk_world_x = chunk_x * self.chunk_size
        chunk_world_y = chunk_y * self.chunk_size

        # Find nearby regions and apply ore patches
        for rx, ry in self._nearby_regions(chunk_world_x, chunk_world_y):
            patch = self.ore_gen.get_patch(rx, ry)

            if patch is None:
                continue

            self.ore_gen.paint_patch(
                chunk,
                chunk_world_x,
                chunk_world_y,
                self.chunk_size,
                **patch
            )

        return chunk

    def _nearby_regions(self, world_x, world_y):
        """Yield region coordinates near the given world position."""
        rs = self.region_size
        cs = self.chunk_size
        
        min_rx = (world_x // rs) - 1
        max_rx = ((world_x + cs) // rs) + 1
        min_ry = (world_y // rs) - 1
        max_ry = ((world_y + cs) // rs) + 1

        for ry in range(min_ry, max_ry + 1):
            for rx in range(min_rx, max_rx + 1):
                yield rx, ry
