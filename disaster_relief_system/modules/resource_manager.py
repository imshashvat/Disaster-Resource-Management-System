# modules/resource_manager.py
# ResourceManager — Inventory management using Dictionary data structure

import random
from models.resource import Resource
from utils.validators import InvalidResourceQuantity, ResourceNotFound
from utils.decorators import log_allocation
from utils.helpers import print_header, print_separator


class ResourceManager:
    """
    Manages resource inventory.
    resources is a DICTIONARY: {resource_id: Resource}
    """

    def __init__(self, system):
        self.system = system

    def _new_id(self) -> str:
        return f"RES{random.randint(1000, 9999)}"

    # ─────────────────────────────────────────────
    # Add Resource
    # ─────────────────────────────────────────────
    def add_resource(self, resource_name: str, quantity: int,
                     category: str, unit: str = "units") -> Resource:
        rid = self._new_id()
        while rid in self.system.resources:
            rid = self._new_id()
        res = Resource(rid, resource_name, quantity, category, unit)
        self.system.resources[rid] = res         # DICTIONARY — key: resource_id
        res.add_resource()
        return res

    # ─────────────────────────────────────────────
    # Allocate Resource  — decorated with @log_allocation
    # ─────────────────────────────────────────────
    @log_allocation
    def allocate_resource(self, resource_id: str, amount: int,
                          destination: str = "Unknown") -> None:
        """Deduct resource from inventory; logs action via decorator."""
        res = self._find(resource_id)
        res.allocate_resource(amount)
        print(f"  Destination: {destination}")

    # ─────────────────────────────────────────────
    # Restock
    # ─────────────────────────────────────────────
    def restock_resource(self, resource_id: str, amount: int) -> None:
        res = self._find(resource_id)
        res.update_quantity(amount)

    # ─────────────────────────────────────────────
    # View
    # ─────────────────────────────────────────────
    def view_inventory(self) -> None:
        """Display all resources (dict values) using list comprehension for in-stock."""
        if not self.system.resources:
            print("  Inventory is empty.")
            return
        # LIST COMPREHENSION — all resources in stock
        in_stock = [r for r in self.system.resources.values() if r.quantity > 0]
        out_of_stock = [r for r in self.system.resources.values() if r.quantity == 0]

        print(f"  Total resource types : {len(self.system.resources)}")
        print(f"  In stock             : {len(in_stock)}")
        print(f"  Out of stock         : {len(out_of_stock)}")
        print_separator()
        for res in self.system.resources.values():
            res.display_resource()

    def view_available(self) -> None:
        """List comprehension — only resources with qty > 0."""
        available = [r for r in self.system.resources.values() if r.quantity > 0]
        if not available:
            print("  No resources currently in stock.")
            return
        for r in available:
            print(f"  {r}")

    def view_by_category(self, category: str) -> None:
        """Filter by category using list comprehension."""
        filtered = [r for r in self.system.resources.values()
                    if r.category.lower() == category.lower()]
        if not filtered:
            print(f"  No resources found in category '{category}'.")
            return
        for r in filtered:
            r.display_resource()

    def _find(self, resource_id: str) -> Resource:
        if resource_id not in self.system.resources:
            raise ResourceNotFound(f"Resource ID '{resource_id}' not found in inventory.")
        return self.system.resources[resource_id]

    # ─────────────────────────────────────────────
    # CLI Sub-Menu
    # ─────────────────────────────────────────────
    def menu(self) -> None:
        while True:
            print_header("Resource Management")
            print("  1. Add Resource to Inventory")
            print("  2. Allocate Resource")
            print("  3. Restock Resource")
            print("  4. View Full Inventory")
            print("  5. View Available Resources Only")
            print("  6. View by Category")
            print("  0. Back to Main Menu")
            print_separator()
            choice = input("  Enter choice: ").strip()

            if choice == "1":
                self._add_ui()
            elif choice == "2":
                self._allocate_ui()
            elif choice == "3":
                self._restock_ui()
            elif choice == "4":
                print_header("Full Inventory")
                self.view_inventory()
            elif choice == "5":
                print_header("Available Resources")
                self.view_available()
            elif choice == "6":
                cat = input("  Category (Food/Water/Medicine/Emergency Kit/...): ").strip()
                self.view_by_category(cat)
            elif choice == "0":
                break
            else:
                print("  [!] Invalid choice.")

    def _add_ui(self) -> None:
        print_header("Add Resource")
        name = input("  Resource Name: ").strip() or "Resource"
        print(f"  Categories: {', '.join(Resource.CATEGORIES)}")
        cat  = input("  Category: ").strip().title() or "Other"
        if cat not in Resource.CATEGORIES:
            cat = "Other"
        unit = input("  Unit (e.g. kg/litres/packets, default 'units'): ").strip() or "units"
        qty_raw = input("  Initial Quantity: ").strip()
        try:
            qty = int(qty_raw)
            if qty < 0:
                raise ValueError
        except ValueError:
            print("  [!] Quantity must be a non-negative integer.")
            return
        self.add_resource(name, qty, cat, unit)

    def _allocate_ui(self) -> None:
        self.view_available()
        rid = input("  Resource ID to allocate: ").strip()
        amt_raw = input("  Quantity to allocate: ").strip()
        dest    = input("  Destination (camp/area): ").strip() or "Unknown"
        try:
            amt = int(amt_raw)
            if amt <= 0:
                raise InvalidResourceQuantity("Quantity must be positive.")
            self.allocate_resource(rid, amt, dest)
        except (ResourceNotFound, InvalidResourceQuantity, ValueError) as e:
            print(f"  [!] {e}")

    def _restock_ui(self) -> None:
        rid = input("  Resource ID to restock: ").strip()
        amt_raw = input("  Quantity to add: ").strip()
        try:
            amt = int(amt_raw)
            if amt <= 0:
                raise ValueError("Must be positive.")
            self.restock_resource(rid, amt)
        except (ResourceNotFound, InvalidResourceQuantity, ValueError) as e:
            print(f"  [!] {e}")
