class Chunk:
    """2D tile grid representing a chunk of the world."""
    
    __slots__ = ('size', 'tiles')
    
    def __init__(self, size, default_tile="grass"):
        self.size = size

        self.tiles = [
            [default_tile for _ in range(size)]
            for _ in range(size)
        ]

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile