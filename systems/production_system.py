class ProductionSystem:
    def __init__(self):
        self.machines = {}
        self.items_per_minute = 0
    
    def update(self):
        self.update_items_per_minute()

    def update_items_per_minute(self, world):
        self.items_per_minute = len(self.machines)