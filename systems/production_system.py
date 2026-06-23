class ProductionSystem:
    """
    Manages production for all machines using per-minute rates.
    
    Each machine applies its recipe's inputs_per_minute and outputs_per_minute
    to the inventory continuously.
    """
    
    def __init__(self, inventory):
        self.inventory = inventory
        self.machines = []
        self.items_per_second = {}
        self.timer = 0
    
    def register_machine(self, machine):
        """Register a machine to the production system."""
        self.machines.append(machine)
        self._update_production_rates()
    
    def update(self, dt):
        self.timer += dt

        while self.timer >= 1.0:
            self.timer -= 1.0

            # --- Phase 1: compute total requested inputs ---
            requested = {}

            for m in self.machines:
                r = m.recipe
                if r is None:
                    continue

                for item, req in r.inputs_per_second.items():
                    if req > 0:
                        requested[item] = requested.get(item, 0.0) + req

            # --- Phase 2: compute per-item scale ---
            item_scale = {}

            for item, req in requested.items():
                available = self.inventory.get_count(item)
                if req <= 0:
                    item_scale[item] = 1.0
                else:
                    item_scale[item] = min(1.0, available / req)

            # --- Phase 3: compute per-machine scale ---
            machine_scale = {}

            for m in self.machines:
                r = m.recipe
                if r is None:
                    machine_scale[m] = 0
                    continue

                scale = 1.0
                for item, req in r.inputs_per_second.items():
                    if req > 0:
                        scale = min(scale, item_scale.get(item, 1.0))

                machine_scale[m] = scale

            # --- Phase 4: remove inputs once ---
            total_consumption = {}

            for m, scale in machine_scale.items():
                if scale <= 0:
                    continue

                r = m.recipe
                for item, req in r.inputs_per_second.items():
                    if req > 0:
                        total_consumption[item] = (
                            total_consumption.get(item, 0.0)
                            + req * scale
                        )

            for item, amount in total_consumption.items():
                self.inventory.remove(item, amount)

            # --- Phase 5: produce outputs ---
            for m, scale in machine_scale.items():
                if scale <= 0:
                    continue

                r = m.recipe
                for item, out in r.outputs_per_second.items():
                    if out > 0:
                        self.inventory.add(item, out * scale)

    
    def _update_production_rates(self):
        self.items_per_second.clear()

        for machine in self.machines:
            if machine.recipe is None:
                continue

            for item, rate_per_second in machine.recipe.outputs_per_second.items():
                self.items_per_second[item] = (
                    self.items_per_second.get(item, 0)
                    + rate_per_second
                )
    
    def get_production_rate(self, item_key):
        """Get items per second for a specific item."""
        return self.items_per_second.get(item_key, 0.0)