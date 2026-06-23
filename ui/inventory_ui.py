import pygame as py


class InventoryUI:
    """UI for displaying the global inventory."""

    def __init__(self, inventory):
        self.inventory = inventory
        if not py.get_init():
            py.init()
        self.font = py.font.Font(None, 16)

    def draw(self, surface):
        items = self.inventory.all_items()

        panel_height = 40 + max(len(items), 1) * 20
        inventory_rect = py.Rect(10, 10, 260, panel_height)
        py.draw.rect(surface, (35, 35, 40), inventory_rect)
        py.draw.rect(surface, (120, 120, 120), inventory_rect, 1)

        title_surf = self.font.render("Global Inventory", True, (255, 255, 255))
        surface.blit(title_surf, (18, 15))

        y_offset = 40
        if not items:
            empty_surf = self.font.render("No items", True, (200, 200, 200))
            surface.blit(empty_surf, (18, y_offset))
            return

        for item_name, quantity in items.items():
            item_surf = self.font.render(f"{item_name}: {quantity:.2f}", True, (255, 255, 255))
            surface.blit(item_surf, (18, y_offset))
            y_offset += 20