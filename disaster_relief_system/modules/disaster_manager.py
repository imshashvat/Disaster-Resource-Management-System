# modules/disaster_manager.py
# DisasterManager — Register, update, view, and search disasters

import random
from models.disaster import Disaster
from utils.validators import InvalidDisasterID
from utils.helpers import (
    search_disaster, sort_disasters_by_severity,
    print_header, print_separator
)


class DisasterManager:
    """Manages all disaster-related operations."""

    def __init__(self, system):
        self.system = system                     # reference to DisasterManagementSystem

    def _new_id(self) -> str:
        return f"DIS{random.randint(1000, 9999)}"

    # ─────────────────────────────────────────────
    # Register Disaster
    # ─────────────────────────────────────────────
    def register_disaster(self, disaster_type: str, location: str,
                          severity_level: int, status: str = "Active") -> Disaster:
        """Create and register a new disaster."""
        did = self._new_id()
        while any(d.disaster_id == did for d in self.system.disasters):
            did = self._new_id()

        d = Disaster(did, disaster_type, location, severity_level, status)
        self.system.disasters.append(d)
        self.system.disaster_categories.add(disaster_type)   # SET usage
        d.register_disaster()
        print(f"  Disaster ID assigned: {did}")
        return d

    # ─────────────────────────────────────────────
    # Update Disaster Status
    # ─────────────────────────────────────────────
    def update_status(self, disaster_id: str, new_status: str) -> None:
        """Find disaster by ID and update its status."""
        d = search_disaster(self.system.disasters, disaster_id)   # recursive search
        if not d:
            raise InvalidDisasterID(f"No disaster found with ID '{disaster_id}'.")
        d.update_status(new_status)

    # ─────────────────────────────────────────────
    # View All / Single Disaster
    # ─────────────────────────────────────────────
    def view_all(self, sort_by_severity: bool = False) -> None:
        """Display all registered disasters."""
        if not self.system.disasters:
            print("  No disasters registered yet.")
            return
        records = (sort_disasters_by_severity(self.system.disasters)
                   if sort_by_severity else self.system.disasters)
        for d in records:
            d.display_disaster()

    def view_single(self, disaster_id: str) -> None:
        """Display details for a specific disaster."""
        d = search_disaster(self.system.disasters, disaster_id)
        if not d:
            raise InvalidDisasterID(f"No disaster found with ID '{disaster_id}'.")
        d.display_disaster()

    # ─────────────────────────────────────────────
    # Search (recursive via helpers.py)
    # ─────────────────────────────────────────────
    def search(self, disaster_id: str) -> Disaster:
        result = search_disaster(self.system.disasters, disaster_id)
        if not result:
            raise InvalidDisasterID(f"Disaster ID '{disaster_id}' not found.")
        return result

    # ─────────────────────────────────────────────
    # Statistics
    # ─────────────────────────────────────────────
    def show_statistics(self) -> None:
        total  = len(self.system.disasters)
        active = sum(1 for d in self.system.disasters if d.status == "Active")
        cats   = self.system.disaster_categories        # SET
        print(f"  Total Disasters   : {total}")
        print(f"  Active Disasters  : {active}")
        print(f"  Disaster Types    : {', '.join(cats) if cats else 'None'}")

    # ─────────────────────────────────────────────
    # CLI Sub-Menu
    # ─────────────────────────────────────────────
    def menu(self) -> None:
        while True:
            print_header("Disaster Management")
            print("  1. Register New Disaster")
            print("  2. Update Disaster Status")
            print("  3. View All Disasters")
            print("  4. View Disasters (by severity)")
            print("  5. Search Disaster by ID")
            print("  6. Disaster Statistics")
            print("  7. Emergency Helplines")
            print("  0. Back to Main Menu")
            print_separator()
            choice = input("  Enter choice: ").strip()

            if choice == "1":
                self._register_ui()
            elif choice == "2":
                self._update_status_ui()
            elif choice == "3":
                print_header("All Disasters")
                self.view_all()
            elif choice == "4":
                print_header("Disasters (Severity High → Low)")
                self.view_all(sort_by_severity=True)
            elif choice == "5":
                self._search_ui()
            elif choice == "6":
                print_header("Disaster Statistics")
                self.show_statistics()
            elif choice == "7":
                from utils.helpers import get_emergency_helpline
                print(get_emergency_helpline())
            elif choice == "0":
                break
            else:
                print("  [!] Invalid choice.")

    def _register_ui(self) -> None:
        print_header("Register New Disaster")
        types = Disaster.get_emergency_types()
        print("  Disaster Types:")
        for i, t in enumerate(types, 1):
            print(f"    {i}. {t}")
        dtype_input = input("  Select type (number) or enter custom: ").strip()
        try:
            idx = int(dtype_input) - 1
            dtype = types[idx] if 0 <= idx < len(types) else dtype_input
        except ValueError:
            dtype = dtype_input if dtype_input else "Other"

        location = input("  Location: ").strip() or "Unknown"
        sev_raw  = input("  Severity (1=Minor … 5=Catastrophic): ").strip()
        try:
            from utils.validators import validate_severity
            severity = validate_severity(sev_raw)
        except ValueError as e:
            print(f"  [!] {e}")
            return

        self.register_disaster(dtype, location, severity)

    def _update_status_ui(self) -> None:
        did = input("  Enter Disaster ID: ").strip()
        statuses = list(Disaster.VALID_STATUSES)
        print("  Statuses:")
        for i, s in enumerate(statuses, 1):
            print(f"    {i}. {s}")
        s_in = input("  Select status (number): ").strip()
        try:
            status = statuses[int(s_in) - 1]
            self.update_status(did, status)
        except (InvalidDisasterID, ValueError, IndexError) as e:
            print(f"  [!] {e}")

    def _search_ui(self) -> None:
        did = input("  Enter Disaster ID to search: ").strip()
        try:
            d = self.search(did)
            d.display_disaster()
        except InvalidDisasterID as e:
            print(f"  [!] {e}")
