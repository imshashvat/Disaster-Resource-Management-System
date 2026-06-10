# modules/camp_manager.py
# ReliefCampManager — Create camps, manage occupancy

import random
from models.relief_camp import ReliefCamp
from utils.validators import CampCapacityExceeded, InvalidCampID
from utils.helpers import sort_camps_by_occupancy, print_header, print_separator


class CampManager:
    """Manages all relief camp operations."""

    def __init__(self, system):
        self.system = system

    def _new_id(self) -> str:
        return f"CAMP{random.randint(100, 999)}"

    # ─────────────────────────────────────────────
    # Create Camp
    # ─────────────────────────────────────────────
    def create_camp(self, camp_name: str, location: str, capacity: int) -> ReliefCamp:
        cid = self._new_id()
        while any(c.camp_id == cid for c in self.system.camps):
            cid = self._new_id()
        camp = ReliefCamp(cid, camp_name, location, capacity)
        self.system.camps.append(camp)
        camp.add_camp()
        return camp

    # ─────────────────────────────────────────────
    # Allocate / Release People
    # ─────────────────────────────────────────────
    def allocate_people(self, camp_id: str, count: int) -> None:
        camp = self._find(camp_id)
        camp.allocate_people(count)     # raises CampCapacityExceeded if over limit

    def release_people(self, camp_id: str, count: int) -> None:
        camp = self._find(camp_id)
        camp.release_people(count)

    # ─────────────────────────────────────────────
    # View
    # ─────────────────────────────────────────────
    def view_all(self, sort_by_occ: bool = False) -> None:
        if not self.system.camps:
            print("  No relief camps registered.")
            return
        records = sort_camps_by_occupancy(self.system.camps) if sort_by_occ else self.system.camps
        for c in records:
            c.display_camp_details()

    def occupancy_summary(self) -> None:
        """Quick occupancy snapshot of all camps."""
        if not self.system.camps:
            print("  No camps to summarise.")
            return
        total_cap = sum(c.capacity for c in self.system.camps)
        total_occ = sum(c.occupied for c in self.system.camps)
        print(f"  Total Camps     : {len(self.system.camps)}")
        print(f"  Total Capacity  : {total_cap:,}")
        print(f"  Total Occupied  : {total_occ:,}")
        if total_cap > 0:
            print(f"  Overall Occ.    : {total_occ/total_cap*100:.1f}%")

    def _find(self, camp_id: str) -> ReliefCamp:
        for c in self.system.camps:
            if c.camp_id == camp_id:
                return c
        raise InvalidCampID(f"Camp ID '{camp_id}' not found.")

    # ─────────────────────────────────────────────
    # CLI Sub-Menu
    # ─────────────────────────────────────────────
    def menu(self) -> None:
        while True:
            print_header("Relief Camp Management")
            print("  1. Create New Relief Camp")
            print("  2. Allocate People to Camp")
            print("  3. Release People from Camp")
            print("  4. View All Camps")
            print("  5. View Camps (by Occupancy %)")
            print("  6. Occupancy Summary")
            print("  7. View Single Camp")
            print("  0. Back to Main Menu")
            print_separator()
            choice = input("  Enter choice: ").strip()

            if choice == "1":
                self._create_ui()
            elif choice == "2":
                self._allocate_ui()
            elif choice == "3":
                self._release_ui()
            elif choice == "4":
                print_header("All Relief Camps")
                self.view_all()
            elif choice == "5":
                print_header("Camps by Occupancy")
                self.view_all(sort_by_occ=True)
            elif choice == "6":
                print_header("Occupancy Summary")
                self.occupancy_summary()
            elif choice == "7":
                cid = input("  Camp ID: ").strip()
                try:
                    self._find(cid).display_camp_details()
                except InvalidCampID as e:
                    print(f"  [!] {e}")
            elif choice == "0":
                break
            else:
                print("  [!] Invalid choice.")

    def _create_ui(self) -> None:
        print_header("Create Relief Camp")
        name = input("  Camp Name: ").strip() or "Camp"
        location = input("  Location: ").strip() or "Unknown"
        cap_raw = input("  Capacity (number of people): ").strip()
        try:
            cap = int(cap_raw)
            if cap <= 0:
                raise ValueError
        except ValueError:
            print("  [!] Capacity must be a positive integer.")
            return
        self.create_camp(name, location, cap)

    def _allocate_ui(self) -> None:
        cid = input("  Camp ID: ").strip()
        cnt_raw = input("  Number of people to admit: ").strip()
        try:
            cnt = int(cnt_raw)
            if cnt <= 0:
                raise ValueError("Count must be positive.")
            self.allocate_people(cid, cnt)
        except (CampCapacityExceeded, InvalidCampID, ValueError) as e:
            print(f"  [!] {e}")

    def _release_ui(self) -> None:
        cid = input("  Camp ID: ").strip()
        cnt_raw = input("  Number of people to release: ").strip()
        try:
            cnt = int(cnt_raw)
            self.release_people(cid, cnt)
        except (InvalidCampID, ValueError) as e:
            print(f"  [!] {e}")
