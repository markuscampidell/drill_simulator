import random
import threading
from queue import Queue

from generation.chunk_gen import ChunkGenerator


class World:
    def __init__(self, chunk_size=32, tile_size=32, region_size=128, seed=None):
        self.chunk_size = chunk_size
        self.tile_size = tile_size
        self.region_size = region_size

        self.seed = seed or random.randint(0, 999999)

        self.chunks = {}

        self.chunk_queue = Queue()
        self.generating = set()
        self.lock = threading.Lock()

        self.generator = ChunkGenerator(self.seed, chunk_size, region_size)

        self.worker = threading.Thread(target=self._chunk_worker, daemon=True)
        self.worker.start()

    def _chunk_worker(self):
        while True:
            cx, cy = self.chunk_queue.get()

            chunk = self.generator.generate(cx, cy)

            with self.lock:
                self.chunks[(cx, cy)] = chunk
                self.generating.discard((cx, cy))

    def get_chunk(self, cx, cy):
        pos = (cx, cy)

        with self.lock:
            if pos in self.chunks:
                return self.chunks[pos]

            if pos not in self.generating:
                self.generating.add(pos)
                self.chunk_queue.put(pos)

        return None  # not ready yet

    def get_tile(self, x, y):
        cx, local_x = divmod(x, self.chunk_size)
        cy, local_y = divmod(y, self.chunk_size)

        chunk = self.get_chunk(cx, cy)

        if chunk is None:
            return None

        return chunk.get_tile(local_x, local_y)

    def visible_chunk_range(self, camera, screen_width, screen_height):
        tile_left = int(camera.x // self.tile_size)
        tile_top = int(camera.y // self.tile_size)

        tile_right = int((camera.x + screen_width) // self.tile_size)
        tile_bottom = int((camera.y + screen_height) // self.tile_size)

        return (
            tile_left // self.chunk_size,
            tile_top // self.chunk_size,
            tile_right // self.chunk_size,
            tile_bottom // self.chunk_size
        )