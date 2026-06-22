import pygame as py

from core.world import World
from core.camera import Camera
from core.renderer import Renderer
from core.zoom import ZoomController
from systems.machine_manager import MachineManager
from systems.inventory import Inventory
from ui.inventory_ui import InventoryUI


class Game:
    FRICTION = 0.85
    MOVE_SPEED = 8
    MIN_WINDOW_SIZE = 100

    def __init__(self):
        py.init()

        self.screen = py.display.set_mode((1280, 720), py.RESIZABLE)
        self.clock = py.time.Clock()
        self.running = True

        self.world = World()
        self.camera = Camera(*self.screen.get_size())
        self.machine_manager = MachineManager(self.world)
        self.renderer = Renderer(self.world, self.machine_manager)

        self.inventory = Inventory()
        self.inventory.add("iron_ore", 100)
        self.inventory.add("coal", 50)

        self.inventory_ui = InventoryUI(self.inventory)

        self.camera_vel = py.Vector2()

        self.zoom = ZoomController()
        self.zoom.zoom_index = self.zoom.find_index(self.world.tile_size)
        self.zoom.force_apply(self.camera, self.world, self.renderer, self.camera_vel)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

            self.clock.tick(60)

        py.quit()

    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False

            elif event.type == py.VIDEORESIZE:
                self.videoresize(event.w, event.h)

            elif event.type == py.MOUSEWHEEL:
                self.zoom.apply_zoom(self.zoom.zoom_index + event.y, self.camera, self.world, self.renderer, self.camera_vel)

            elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = py.mouse.get_pos()
                tile_size = self.world.tile_size
                world_x = int((self.camera.x + mx) // tile_size)
                world_y = int((self.camera.y + my) // tile_size)
                self.machine_manager.add_machine("assembler", world_x, world_y)

    def update(self):
        self.handle_input()

        # move camera
        self.camera.x += self.camera_vel.x
        self.camera.y += self.camera_vel.y

        # friction
        self.camera_vel *= self.FRICTION

    def handle_input(self):
        keys = py.key.get_pressed()

        direction = py.Vector2((keys[py.K_d] or keys[py.K_RIGHT]) - (keys[py.K_a] or keys[py.K_LEFT]),
                               (keys[py.K_s] or keys[py.K_DOWN]) - (keys[py.K_w] or keys[py.K_UP]))

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.camera_vel += direction * self.MOVE_SPEED

    def videoresize(self, width, height):
        width = max(self.MIN_WINDOW_SIZE, width)
        height = max(self.MIN_WINDOW_SIZE, height)

        self.screen = py.display.set_mode((width, height), py.RESIZABLE)

        self.camera.width = width
        self.camera.height = height

    def draw(self):
        self.renderer.draw_world(self.screen, self.world, self.camera)

        self.inventory_ui.draw(self.screen)

        py.display.flip()