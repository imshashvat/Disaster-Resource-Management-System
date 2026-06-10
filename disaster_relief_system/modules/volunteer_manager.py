# modules/volunteer_manager.py
# VolunteerManager — Register volunteers, assign tasks, track availability

import random
from models.volunteer import Volunteer
from utils.validators import InvalidVolunteerID
from utils.helpers import print_header, print_separator


class VolunteerManager:
    """Manages volunteer registration and task assignment."""

    def __init__(self, system):
        self.system = system

    def _new_ids(self) -> tuple:
        """Return (person_id, volunteer_id) pair."""
        n = random.randint(1000, 9999)
        return f"PER{n}", f"VOL{n}"

    # ─────────────────────────────────────────────
    # Register
    # ─────────────────────────────────────────────
    def register_volunteer(self, name: str, contact: str, address: str,
                           skill: str) -> Volunteer:
        pid, vid = self._new_ids()
        while any(v.volunteer_id == vid for v in self.system.volunteers):
            pid, vid = self._new_ids()

        v = Volunteer(pid, name, contact, address, vid, skill)
        self.system.volunteers.append(v)
        print(f"  Volunteer registered: {v.volunteer_id} - {name}")
        return v

    # ─────────────────────────────────────────────
    # Assign / Complete Tasks
    # ─────────────────────────────────────────────
    def assign_task(self, volunteer_id: str, task: str) -> None:
        v = self._find(volunteer_id)
        v.assign_task(task)

    def complete_task(self, volunteer_id: str) -> None:
        v = self._find(volunteer_id)
        v.complete_task()
        print(f"  Task completed. {v.name} is now available.")

    # ─────────────────────────────────────────────
    # View
    # ─────────────────────────────────────────────
    def view_all(self) -> None:
        if not self.system.volunteers:
            print("  No volunteers registered.")
            return
        for v in self.system.volunteers:
            v.display_details()

    def view_available(self) -> None:
        """List comprehension — volunteers with no assigned task."""
        available = [v for v in self.system.volunteers if v.assigned_task is None]
        if not available:
            print("  All volunteers are currently assigned.")
            return
        print(f"  Available Volunteers ({len(available)}):")
        for v in available:
            print(f"    {v}")

    def generate_volunteer_report(self) -> None:
        """Display a volunteer activity summary."""
        total     = len(self.system.volunteers)
        assigned  = sum(1 for v in self.system.volunteers if v.assigned_task)
        available = total - assigned

        print(f"  Total Volunteers  : {total}")
        print(f"  On Active Task    : {assigned}")
        print(f"  Available         : {available}")
        print_separator()

        skill_groups: dict = {}
        for v in self.system.volunteers:
            skill_groups.setdefault(v.skill, []).append(v.name)
        for skill, names in skill_groups.items():
            print(f"  {skill}: {', '.join(names)}")

    def _find(self, volunteer_id: str) -> Volunteer:
        for v in self.system.volunteers:
            if v.volunteer_id == volunteer_id:
                return v
        raise InvalidVolunteerID(f"Volunteer ID '{volunteer_id}' not found.")

    # ─────────────────────────────────────────────
    # CLI Sub-Menu
    # ─────────────────────────────────────────────
    def menu(self) -> None:
        while True:
            print_header("Volunteer Management")
            print("  1. Register Volunteer")
            print("  2. Assign Task to Volunteer")
            print("  3. Mark Task as Complete")
            print("  4. View All Volunteers")
            print("  5. View Available Volunteers")
            print("  6. Volunteer Activity Report")
            print("  0. Back to Main Menu")
            print_separator()
            choice = input("  Enter choice: ").strip()

            if choice == "1":
                self._register_ui()
            elif choice == "2":
                self._assign_ui()
            elif choice == "3":
                self._complete_ui()
            elif choice == "4":
                print_header("All Volunteers")
                self.view_all()
            elif choice == "5":
                print_header("Available Volunteers")
                self.view_available()
            elif choice == "6":
                print_header("Volunteer Report")
                self.generate_volunteer_report()
            elif choice == "0":
                break
            else:
                print("  [!] Invalid choice.")

    def _register_ui(self) -> None:
        print_header("Register Volunteer")
        name    = input("  Full Name: ").strip() or "Unknown"
        contact = input("  Contact Number: ").strip() or "N/A"
        address = input("  Address: ").strip() or "N/A"
        skill   = input("  Skill (e.g. Medical/Rescue/Logistics/Cooking): ").strip() or "General"
        self.register_volunteer(name, contact, address, skill)

    def _assign_ui(self) -> None:
        self.view_available()
        vid  = input("  Volunteer ID: ").strip()
        task = input("  Task Description: ").strip()
        try:
            self.assign_task(vid, task)
        except InvalidVolunteerID as e:
            print(f"  [!] {e}")

    def _complete_ui(self) -> None:
        vid = input("  Volunteer ID: ").strip()
        try:
            self.complete_task(vid)
        except InvalidVolunteerID as e:
            print(f"  [!] {e}")
