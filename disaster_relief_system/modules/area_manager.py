# modules/area_manager.py
# AffectedAreaManager — Add, update, view affected areas

import random
from models.affected_area import AffectedArea
from utils.validators import InvalidAreaID
from utils.helpers import print_header, print_separator, calculate_resources_needed


class AreaManager:
    """Manages all affected area operations."""

    def __init__(self, system):
        self.system = system

    def _new_id(self) -> str:
        return f"AREA{random.randint(100, 999)}"

    # ─────────────────────────────────────────────
    # Add Area
    # ─────────────────────────────────────────────
    def add_area(self, area_name: str, affected_population: int,
                 damage_level: str, disaster_id: str = None,
                 lat: float = 0.0, lng: float = 0.0) -> AffectedArea:
        aid = self._new_id()
        while any(a.area_id == aid for a in self.system.areas):
            aid = self._new_id()

        area = AffectedArea(
            area_id             = aid,
            area_name           = area_name,
            affected_population = affected_population,
            damage_level        = damage_level,
            disaster_id         = disaster_id,
            location_coords     = (lat, lng),      # TUPLE — fixed coords
        )
        self.system.areas.append(area)
        area.add_area()
        return area

    # ─────────────────────────────────────────────
    # Update Area
    # ─────────────────────────────────────────────
    def update_area(self, area_id: str, population: int = None, damage: str = None) -> None:
        area = self._find(area_id)
        area.update_area(population, damage)

    # ─────────────────────────────────────────────
    # View
    # ─────────────────────────────────────────────
    def view_all(self) -> None:
        if not self.system.areas:
            print("  No affected areas registered.")
            return
        for area in self.system.areas:
            area.display_area()

    def view_damage_report(self) -> None:
        """Show areas sorted by damage level (Critical first)."""
        order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        sorted_areas = sorted(self.system.areas,
                              key=lambda a: order.get(a.damage_level, 99))
        for area in sorted_areas:
            area.display_area()
            # List comprehension — estimate resources needed
            estimates = calculate_resources_needed(area.affected_population)
            print("    Estimated daily resource needs:")
            for item, qty in estimates.items():
                print(f"      • {item}: {qty:,}")

    def _find(self, area_id: str) -> AffectedArea:
        for a in self.system.areas:
            if a.area_id == area_id:
                return a
        raise InvalidAreaID(f"Area ID '{area_id}' not found.")

    # ─────────────────────────────────────────────
    # CLI Sub-Menu
    # ─────────────────────────────────────────────
    def menu(self) -> None:
        while True:
            print_header("Affected Area Management")
            print("  1. Add Affected Area")
            print("  2. Update Area Information")
            print("  3. View All Areas")
            print("  4. View Damage Report (sorted)")
            print("  5. Track Population (by area ID)")
            print("  0. Back to Main Menu")
            print_separator()
            choice = input("  Enter choice: ").strip()

            if choice == "1":
                self._add_ui()
            elif choice == "2":
                self._update_ui()
            elif choice == "3":
                print_header("All Affected Areas")
                self.view_all()
            elif choice == "4":
                print_header("Damage Report")
                self.view_damage_report()
            elif choice == "5":
                aid = input("  Enter Area ID: ").strip()
                try:
                    a = self._find(aid)
                    print(f"  {a.area_name}: {a.affected_population:,} people affected.")
                except InvalidAreaID as e:
                    print(f"  [!] {e}")
            elif choice == "0":
                break
            else:
                print("  [!] Invalid choice.")

    def _add_ui(self) -> None:
        print_header("Add Affected Area")
        name = input("  Area Name: ").strip() or "Unknown"
        pop_raw = input("  Affected Population: ").strip()
        try:
            pop = int(pop_raw)
            if pop < 0:
                raise ValueError
        except ValueError:
            print("  [!] Invalid population number.")
            return

        print("  Damage Levels: Low, Medium, High, Critical")
        damage = input("  Damage Level: ").strip().capitalize() or "Medium"
        if damage not in AffectedArea.DAMAGE_LEVELS:
            damage = "Medium"

        did = input("  Associated Disaster ID (leave blank to skip): ").strip() or None

        lat_raw = input("  Latitude (e.g. 28.6139, press Enter to skip): ").strip()
        lng_raw = input("  Longitude (e.g. 77.2090, press Enter to skip): ").strip()
        try:
            lat = float(lat_raw) if lat_raw else 0.0
            lng = float(lng_raw) if lng_raw else 0.0
        except ValueError:
            lat, lng = 0.0, 0.0

        self.add_area(name, pop, damage, did, lat, lng)

    def _update_ui(self) -> None:
        aid = input("  Enter Area ID to update: ").strip()
        try:
            pop_raw = input("  New population (press Enter to skip): ").strip()
            pop = int(pop_raw) if pop_raw else None
            damage = input("  New damage level (press Enter to skip): ").strip().capitalize() or None
            self.update_area(aid, pop, damage)
        except (InvalidAreaID, ValueError) as e:
            print(f"  [!] {e}")
