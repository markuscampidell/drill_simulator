from collections import Counter

from data.items import ITEMS


class Inventory:
    """Stores item counts keyed by item ID from data.items.ITEMS."""

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

    def remove(self, item_key: str, amount: int = 1):
        """Remove items from the inventory.

        Args:
            item_key: Key from ITEMS.
            amount: Positive number of items to remove.

        Raises:
            ValueError: If amount is invalid or inventory lacks enough items.
        """
        self._validate_item_key(item_key)
        if amount <= 0:
            raise ValueError("Amount to remove must be positive")

        if self._counts[item_key] < amount:
            raise ValueError(
                f"Not enough {item_key} in inventory: {self._counts[item_key]} available"
            )

        self._counts[item_key] -= amount
        if self._counts[item_key] == 0:
            del self._counts[item_key]

    def get_count(self, item_key: str) -> int:
        """Return the quantity of the given item key."""
        self._validate_item_key(item_key)
        return self._counts[item_key]

    def has(self, item_key: str, amount: int = 1) -> bool:
        """Return whether the inventory contains at least amount of item_key."""
        self._validate_item_key(item_key)
        return self._counts[item_key] >= amount

    def all_items(self):
        """Return a dictionary of item_key to count for all stored items."""
        return dict(self._counts)

    def total_count(self) -> int:
        """Return total number of items in the inventory."""
        return sum(self._counts.values())

    def clear(self):
        """Remove all items from the inventory."""
        self._counts.clear()

    def _validate_item_key(self, item_key: str):
        if item_key not in ITEMS:
            raise KeyError(f"Unknown item key: {item_key}")

    def __repr__(self):
        if not self._counts:
            return "Inventory(empty)"
        return "Inventory(" + ", ".join(
            f"{key}: {count}" for key, count in self._counts.items()
        ) + ")"