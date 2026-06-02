import pygame as py


class ZoomController:
    """Manage discrete zoom levels and apply them to camera/world/renderer.

    Responsibilities:
    - Store allowed zoom levels
    - Report whether the current zoom allows building
    - Apply zoom changes while keeping the screen center stable
    """

    def __init__(self, zoom_levels=None, build_min=16, build_max=256):
        self.zoom_levels = zoom_levels or [16, 24, 32, 48, 64, 128, 256]
        self.build_min = build_min
        self.build_max = build_max
        self.zoom_index = 0

    def find_index(self, tile_size):
        if tile_size in self.zoom_levels:
            return self.zoom_levels.index(tile_size)
        # choose nearest
        return min(range(len(self.zoom_levels)), key=lambda i: abs(self.zoom_levels[i] - tile_size))

    @property
    def tile_size(self):
        return self.zoom_levels[self.zoom_index]

    @property
    def can_build(self):
        return self.build_min <= self.tile_size <= self.build_max

    def apply_zoom(self, new_index, camera, world, renderer, camera_vel=None):
        """Apply zoom change centered on screen.

        Returns True if a change was applied.
        """
        new_index = max(0, min(new_index, len(self.zoom_levels) - 1))
        if new_index == self.zoom_index:
            return False

        old_tile_size = world.tile_size
        new_tile_size = self.zoom_levels[new_index]

        # screen center in world coordinates
        screen_center = py.Vector2(camera.x + camera.width / 2, camera.y + camera.height / 2)

        scale = new_tile_size / old_tile_size

        # update sizes and cached surfaces
        world.tile_size = new_tile_size
        renderer.tile_surfaces = renderer._get_surfaces(new_tile_size)

        # scale camera so center stays the same
        screen_center *= scale
        camera.x = screen_center.x - camera.width / 2
        camera.y = screen_center.y - camera.height / 2

        # scale camera velocity if provided
        if camera_vel is not None:
            camera_vel *= scale

        self.zoom_index = new_index
        return True

    def force_apply(self, camera, world, renderer, camera_vel=None):
        """Force applying the current zoom index (useful on init)."""
        # apply with same index but ensure surfaces and tile_size are set
        old_tile_size = world.tile_size
        new_tile_size = self.tile_size
        world.tile_size = new_tile_size
        renderer.tile_surfaces = renderer._get_surfaces(new_tile_size)
        if camera_vel is not None and old_tile_size != 0:
            camera_vel *= (new_tile_size / old_tile_size)
