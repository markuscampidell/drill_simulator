import pygame as py

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

        self.move_speed = 8
        self.velocity = py.Vector2()
        self.friction = 0.85
    
    def update(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

        self.velocity *= self.friction
    
    def move(self, direction):
        self.velocity += direction * self.move_speed
    
    def zoom(self, screen_center, scale):
        """Zoom the camera by a scale factor, keeping the center of the screen stable."""
        screen_center *= scale

        # update camera position to keep center stable
        self.x = screen_center.x - self.width / 2
        self.y = screen_center.y - self.height / 2

    def screen_to_tile(self, screen_pos, tile_size):
        sx, sy = screen_pos
        return (
            int((self.x + sx) // tile_size),
            int((self.y + sy) // tile_size)
        )