from collections import Counter

from data.items import ITEMS


class Inventory:
    """Stores item counts keyed by item ID from data.items.ITEMS."""
    EPSILON = 1e-6  # Threshold for considering a count to be effectively zero

    def __init__(self):
        self._counts = Counter()

    def add(self, item_key: str, amount: int = 1):
        """Add items to the inventory.

        Args:
            item_key: Key from ITEMS.
            amount: Positive number of items to add.
        """
        self._validate_item_key(item_key)
        if amount <= 0:
            raise ValueError("Amount to add must be positive")

        self._counts[item_key] += amount

    def remove(self, item_key: str, amount: float = 1):
        self._validate_item_key(item_key)

        if amount <= self.EPSILON:
            return

        available = self._counts[item_key]

        if available + self.EPSILON < amount:
            raise ValueError(
                f"Not enough {item_key} in inventory: {available} available"
            )

        self._counts[item_key] -= amount

        # Snap tiny leftovers to exactly zero
        if abs(self._counts[item_key]) < self.EPSILON:
            self._counts[item_key] = 0

        if self._counts[item_key] == 0:
            del self._counts[item_key]

    def get_count(self, item_key: str) -> float:
        """Return the quantity of the given item key."""
        self._validate_item_key(item_key)
        return self._counts[item_key]

    def has(self, item_key: str, amount: float = 1) -> bool:
        """Return whether the inventory contains at least amount of item_key."""
        self._validate_item_key(item_key)
        return self._counts[item_key] >= amount

    def all_items(self):
        """Return a dictionary of item_key to count for all stored items."""
        return dict(self._counts)

    def total_count(self) -> float:
        """Return total number of items in the inventory."""
        return sum(self._counts.values())

    def clear(self):
        """Remove all items from the inventory."""
        self._counts.clear()

    def _validate_item_key(self, item_key: str):
        if item_key not in ITEMS:
            raise KeyError(f"Unknown item key: {item_key}")
    
    def cleanup(self):
        for key in list(self._counts.keys()):
            if abs(self._counts[key]) < self.EPSILON:
                del self._counts[key]

    def __repr__(self):
        if not self._counts:
            return "Inventory(empty)"
        return "Inventory(" + ", ".join(
            f"{key}: {count}" for key, count in self._counts.items()
        ) + ")"