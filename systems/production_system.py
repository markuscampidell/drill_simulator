class ProductionSystem:
    """
    Manages production for all machines using per-minute rates.
    
    Each machine applies its recipe's inputs_per_minute and outputs_per_minute
    to the inventory continuously.
    """
    
    def __init__(self, inventory):
        self.inventory = inventory
        self.machines = []
        self.items_per_minute = {}
        self.timer = 0
    
    def register_machine(self, machine):
        """Register a machine to the production system."""
        self.machines.append(machine)
        self._update_production_rates()
    
    def update(self, dt):
        self.timer += dt

        if self.timer < 1.0:
            self.inventory.cleanup()
            return True

        self.timer -= 1.0

        time_fraction = 1 / 60.0

        # STEP 1: collect demands
        demands = []

        for machine in self.machines:
            if machine.recipe is None:
                continue

            demands.append((machine, self._get_demand(machine, time_fraction)))

        # STEP 2: compute allocations
        allocations = self._allocate(demands)

        # STEP 3: execute
        for machine, scale in allocations.items():
            self._run_scaled(machine, time_fraction, scale)

        return True

    def _get_demand(self, machine, time_fraction):
        recipe = machine.recipe

        demand = {}

        for item, per_min in recipe.inputs_per_minute.items():
            demand[item] = per_min * time_fraction

        return demand
    
    def _allocate(self, demands):
        total_needed = {}

        # sum all demand per item
        for machine, demand in demands:
            for item, amount in demand.items():
                total_needed[item] = total_needed.get(item, 0) + amount

        # compute scale per item
        scale_per_item = {}
        for item, needed in total_needed.items():
            available = self.inventory.get_count(item)
            scale_per_item[item] = min(1.0, available / needed) if needed > 0 else 1.0

        # assign each machine a scale (worst-case limiting item)
        result = {}

        for machine, demand in demands:
            scale = 1.0

            for item, amount in demand.items():
                if amount > 0:
                    scale = min(scale, scale_per_item[item])

            result[machine] = scale

        return result
    
    def _run_scaled(self, machine, time_fraction, scale):
        recipe = machine.recipe

        # consume
        for item, per_min in recipe.inputs_per_minute.items():
            amount = per_min * time_fraction * scale

            if amount > 0:
                self.inventory.remove(item, amount)

        # produce
        for item, per_min in recipe.outputs_per_minute.items():
            amount = per_min * time_fraction * scale

            if amount > 0:
                self.inventory.add(item, amount)
    
    def _update_production_rates(self):
        """Calculate total items per minute from all active machines."""
        self.items_per_minute.clear()
        
        for machine in self.machines:
            if machine.recipe is None:
                continue
            
            # Sum outputs per minute
            for output_item, rate in machine.recipe.outputs_per_minute.items():
                if output_item not in self.items_per_minute:
                    self.items_per_minute[output_item] = 0
                self.items_per_minute[output_item] += rate
    
    def get_production_rate(self, item_key):
        """Get items per minute for a specific item."""
        return self.items_per_minute.get(item_key, 0.0)