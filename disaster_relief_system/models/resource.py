# models/resource.py
# Resource class — stored in Dictionary-based inventory

from datetime import datetime
from utils.validators import InvalidResourceQuantity


class Resource:
    """Represents a relief resource item (food, water, medicine, etc.)."""

    CATEGORIES = {"Food", "Water", "Medicine", "Emergency Kit", "Clothing", "Shelter", "Other"}

    def __init__(self, resource_id: str, resource_name: str, quantity: int,
                 category: str, unit: str = "units", added_on: str = None):
        self.resource_id   = resource_id
        self.resource_name = resource_name
        self.quantity      = quantity
        self.category      = category
        self.unit          = unit
        self.added_on      = added_on or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Instance Methods ──────────────────────────────────────────────────────
    def add_resource(self) -> None:
        print(f"  Resource '{self.resource_name}' [{self.resource_id}] added. "
              f"Qty: {self.quantity} {self.unit}")

    def update_quantity(self, delta: int) -> None:
        """Add (positive delta) or remove (negative delta) from stock."""
        if self.quantity + delta < 0:
            raise InvalidResourceQuantity(
                f"Cannot reduce '{self.resource_name}' by {abs(delta)}. "
                f"Only {self.quantity} {self.unit} in stock."
            )
        self.quantity += delta
        print(f"  '{self.resource_name}' quantity updated to {self.quantity} {self.unit}.")

    def allocate_resource(self, amount: int) -> None:
        """Deduct allocated quantity from inventory."""
        if amount <= 0:
            raise InvalidResourceQuantity("Allocation amount must be positive.")
        if amount > self.quantity:
            raise InvalidResourceQuantity(
                f"Insufficient '{self.resource_name}'. "
                f"Requested: {amount}, Available: {self.quantity} {self.unit}."
            )
        self.quantity -= amount
        print(f"  Allocated {amount} {self.unit} of '{self.resource_name}'. "
              f"Remaining: {self.quantity} {self.unit}.")

    def display_resource(self) -> None:
        print(f"  ┌─ Resource ───────────────────────────────────")
        print(f"  │  Resource ID : {self.resource_id}")
        print(f"  │  Name        : {self.resource_name}")
        print(f"  │  Category    : {self.category}")
        print(f"  │  Quantity    : {self.quantity} {self.unit}")
        print(f"  │  Added On    : {self.added_on}")
        print(f"  └─────────────────────────────────────────────")

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "resource_id":   self.resource_id,
            "resource_name": self.resource_name,
            "quantity":      self.quantity,
            "category":      self.category,
            "unit":          self.unit,
            "added_on":      self.added_on,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Resource":
        return cls(
            resource_id   = data["resource_id"],
            resource_name = data["resource_name"],
            quantity      = data["quantity"],
            category      = data["category"],
            unit          = data.get("unit", "units"),
            added_on      = data.get("added_on", ""),
        )

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (f"Resource[{self.resource_id}] {self.resource_name} "
                f"| {self.category} | Qty: {self.quantity} {self.unit}")

    def __repr__(self) -> str:
        return (f"Resource(id={self.resource_id!r}, name={self.resource_name!r}, "
                f"qty={self.quantity}, cat={self.category!r})")
