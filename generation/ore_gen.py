import random


class OreGenerator:
    """Generates ore patches for world regions."""
    
    ORE_SETTINGS = {
        "iron": {"weight": 20, "radius": (12, 17)},
        "copper": {"weight": 25, "radius": (10, 16)},
        "coal": {"weight": 25, "radius": (6, 10)},
        "stone": {"weight": 30, "radius": (10, 12)},
    }

    def __init__(self, seed, region_size):
        self.seed = seed
        self.region_size = region_size
        # Cache ore types and weights for faster selection
        self._ore_types = list(self.ORE_SETTINGS.keys())
        self._ore_weights = [s["weight"] for s in self.ORE_SETTINGS.values()]

    def get_patch(self, rx, ry):
        """Generate an ore patch for a region, or None if empty."""
        rng = random.Random(self.seed + rx * 928371 + ry * 123781)

        # 35% chance region is empty
        if rng.random() < 0.35:
            return None

        ore_type = rng.choices(self._ore_types, weights=self._ore_weights)[0]

        radius_min, radius_max = self.ORE_SETTINGS[ore_type]["radius"]

        return {
            "ore_type": ore_type,
            "patch_x": rx * self.region_size + rng.randint(20, self.region_size - 20),
            "patch_y": ry * self.region_size + rng.randint(20, self.region_size - 20),
            "radius": rng.randint(radius_min, radius_max),
        }

    def paint_patch(self, chunk, chunk_world_x, chunk_world_y, chunk_size, ore_type, patch_x, patch_y, radius):
        """Paint an ore patch onto a chunk."""
        # Early exit if patch is completely outside chunk bounds
        if (patch_x + radius < chunk_world_x or patch_x - radius >= chunk_world_x + chunk_size or
            patch_y + radius < chunk_world_y or patch_y - radius >= chunk_world_y + chunk_size):
            return
        
        rng = random.Random(self.seed + patch_x * 999 + patch_y * 777)

        radius_sq = radius * radius
        radius_noise = radius * radius + 4  # Pre-calculate max noise offset
        
        min_x = max(0, patch_x - radius - chunk_world_x)
        max_x = min(chunk_size, patch_x + radius - chunk_world_x + 1)
        
        min_y = max(0, patch_y - radius - chunk_world_y)
        max_y = min(chunk_size, patch_y + radius - chunk_world_y + 1)

        for local_y in range(min_y, max_y):
            for local_x in range(min_x, max_x):
                wx = chunk_world_x + local_x
                wy = chunk_world_y + local_y

                dx = wx - patch_x
                dy = wy - patch_y

                dist_sq = dx * dx + dy * dy

                if dist_sq > radius_noise:  # Quick reject far points
                    continue

                noise = rng.uniform(-2.0, 2.0)

                if dist_sq < (radius + noise) ** 2:
                    chunk.set_tile(local_x, local_y, ore_type)