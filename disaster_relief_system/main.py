# main.py
# Entry Point — DisasterManagementSystem (Composition Root) + Main Menu

import sys
import io

# Force UTF-8 output on Windows so Unicode box-drawing chars display correctly
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import json
import os
from datetime import datetime

# ── Models ────────────────────────────────────────────────────────────────────
from models.disaster      import Disaster
from models.affected_area import AffectedArea
from models.relief_camp   import ReliefCamp
from models.resource      import Resource
from models.donation      import Donation
from models.donor         import Donor
from models.volunteer     import Volunteer
from models.report        import Report

# ── Manager Modules ───────────────────────────────────────────────────────────
from modules.disaster_manager  import DisasterManager
from modules.area_manager      import AreaManager
from modules.camp_manager      import CampManager
from modules.resource_manager  import ResourceManager
from modules.volunteer_manager import VolunteerManager
from modules.donation_manager  import DonationManager
from modules.report_manager    import ReportManager

# ── Utilities ─────────────────────────────────────────────────────────────────
from utils.helpers import print_header, print_separator, get_emergency_helpline


# ══════════════════════════════════════════════════════════════════════════════
# DisasterManagementSystem — Composition Root
# ══════════════════════════════════════════════════════════════════════════════

class DisasterManagementSystem:
    """
    Central system class that owns all entity lists/dicts.
    Demonstrates COMPOSITION — contains disasters, camps, volunteers,
    resources (dict), donations, donors, areas, reports.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)      # os module — create data/ if missing

        # ── Data Structures ──────────────────────────────────────────────────
        self.disasters:           list  = []       # LIST  — Disaster objects
        self.camps:               list  = []       # LIST  — ReliefCamp objects
        self.volunteers:          list  = []       # LIST  — Volunteer objects
        self.areas:               list  = []       # LIST  — AffectedArea objects
        self.donations:           list  = []       # LIST  — Donation objects
        self.donors:              list  = []       # LIST  — Donor objects
        self.reports:             list  = []       # LIST  — Report objects
        self.resources:           dict  = {}       # DICT  — {resource_id: Resource}
        self.disaster_categories: set   = set()    # SET   — unique disaster types

        # ── Manager Modules (Composition) ────────────────────────────────────
        self.disaster_mgr  = DisasterManager(self)
        self.area_mgr      = AreaManager(self)
        self.camp_mgr      = CampManager(self)
        self.resource_mgr  = ResourceManager(self)
        self.volunteer_mgr = VolunteerManager(self)
        self.donation_mgr  = DonationManager(self)
        self.report_mgr    = ReportManager(self)

    # ─────────────────────────────────────────────
    # Save Data — JSON serialization
    # ─────────────────────────────────────────────
    def save_data(self) -> None:
        """Serialize all entity records to JSON files using to_dict()."""
        files = {
            "disasters.json":  [d.to_dict() for d in self.disasters],
            "camps.json":      [c.to_dict() for c in self.camps],
            "volunteers.json": [v.to_dict() for v in self.volunteers],
            "areas.json":      [a.to_dict() for a in self.areas],
            "donations.json":  [d.to_dict() for d in self.donations],
            "donors.json":     [d.to_dict() for d in self.donors],
            "reports.json":    [r.to_dict() for r in self.reports],
            "resources.json":  [r.to_dict() for r in self.resources.values()],
            "categories.json": list(self.disaster_categories),
        }
        for filename, data in files.items():
            path = os.path.join(self.data_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n  [✔] All data saved to '{self.data_dir}/' folder.")
        print(f"      Disasters: {len(self.disasters)}  |  Camps: {len(self.camps)}  |  "
              f"Volunteers: {len(self.volunteers)}")
        print(f"      Resources: {len(self.resources)}  |  Donations: {len(self.donations)}  |  "
              f"Areas: {len(self.areas)}")

    # ─────────────────────────────────────────────
    # Load Data — JSON deserialization
    # ─────────────────────────────────────────────
    def load_data(self) -> None:
        """Reconstruct entity objects from JSON files using from_dict()."""
        try:
            loaders = {
                "disasters.json":  (Disaster.from_dict,    self.disasters),
                "camps.json":      (ReliefCamp.from_dict,  self.camps),
                "volunteers.json": (Volunteer.from_dict,   self.volunteers),
                "areas.json":      (AffectedArea.from_dict, self.areas),
                "donations.json":  (Donation.from_dict,    self.donations),
                "donors.json":     (Donor.from_dict,       self.donors),
                "reports.json":    (Report.from_dict,      self.reports),
            }
            for filename, (factory, store) in loaders.items():
                path = os.path.join(self.data_dir, filename)
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        records = json.load(f)
                    store.extend(factory(rec) for rec in records)

            # Resources — stored in dict
            res_path = os.path.join(self.data_dir, "resources.json")
            if os.path.exists(res_path):
                with open(res_path, "r", encoding="utf-8") as f:
                    for rec in json.load(f):
                        r = Resource.from_dict(rec)
                        self.resources[r.resource_id] = r

            # Categories — SET
            cat_path = os.path.join(self.data_dir, "categories.json")
            if os.path.exists(cat_path):
                with open(cat_path, "r", encoding="utf-8") as f:
                    self.disaster_categories = set(json.load(f))

            print(f"\n  [✔] Data loaded successfully.")
            print(f"      Disasters: {len(self.disasters)}  |  Camps: {len(self.camps)}  |  "
                  f"Volunteers: {len(self.volunteers)}")

        except FileNotFoundError:
            print("  [!] No saved data found. Starting fresh.")
        except json.JSONDecodeError as e:
            print(f"  [!] Error reading saved data: {e}. Starting with empty records.")
        except Exception as e:
            print(f"  [!] Unexpected error during load: {e}. Starting with empty records.")

    # ─────────────────────────────────────────────
    # Quick Dashboard
    # ─────────────────────────────────────────────
    def show_dashboard(self) -> None:
        total_funds = sum(d.amount for d in self.donations)
        total_occ   = sum(c.occupied for c in self.camps)
        total_cap   = sum(c.capacity for c in self.camps)
        active_dis  = sum(1 for d in self.disasters if d.status == "Active")

        print("\n  ╔══════════ SYSTEM DASHBOARD ══════════╗")
        print(f"  ║  Active Disasters   : {active_dis:<14} ║")
        print(f"  ║  Affected Areas     : {len(self.areas):<14} ║")
        print(f"  ║  Relief Camps       : {len(self.camps):<14} ║")
        print(f"  ║  Camp Occupancy     : {total_occ}/{total_cap:<11} ║")
        print(f"  ║  Volunteers         : {len(self.volunteers):<14} ║")
        print(f"  ║  Resource Types     : {len(self.resources):<14} ║")
        print(f"  ║  Total Donations    : INR {total_funds:<10,.0f} ║")
        print(f"  ║  Disaster Categories: {len(self.disaster_categories):<14} ║")
        print("  ╚══════════════════════════════════════╝")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN MENU — 10-option while-True loop
# ══════════════════════════════════════════════════════════════════════════════

def print_main_menu() -> None:
    print("\n" + "═" * 60)
    print("   DISASTER RELIEF RESOURCE MANAGEMENT SYSTEM")
    print("   Noida Institute of Engineering and Technology")
    print("═" * 60)
    print("   1.  Disaster Management")
    print("   2.  Affected Area Management")
    print("   3.  Relief Camp Management")
    print("   4.  Resource Management")
    print("   5.  Volunteer Management")
    print("   6.  Donation Management")
    print("   7.  Report Generation")
    print("   8.  Save Data")
    print("   9.  Load Data")
    print("   10. Dashboard")
    print("   11. Emergency Helplines")
    print("   0.  Exit")
    print("═" * 60)


def main() -> None:
    print("\n" + "═" * 60)
    print("  Starting Disaster Relief Resource Management System...")
    print("═" * 60)

    system = DisasterManagementSystem(data_dir="data")

    # Auto-load on startup
    system.load_data()

    while True:
        try:
            print_main_menu()
            choice = input("   Select option: ").strip()

            if choice == "1":
                system.disaster_mgr.menu()

            elif choice == "2":
                system.area_mgr.menu()

            elif choice == "3":
                system.camp_mgr.menu()

            elif choice == "4":
                system.resource_mgr.menu()

            elif choice == "5":
                system.volunteer_mgr.menu()

            elif choice == "6":
                system.donation_mgr.menu()

            elif choice == "7":
                system.report_mgr.menu()

            elif choice == "8":
                system.save_data()

            elif choice == "9":
                system.load_data()

            elif choice == "10":
                system.show_dashboard()

            elif choice == "11":
                print(get_emergency_helpline())

            elif choice == "0":
                print("\n  Auto-saving data before exit...")
                system.save_data()
                print("\n  Thank you for using the Disaster Relief System.")
                print("  Stay safe. Every resource saved is a life saved.\n")
                sys.exit(0)

            else:
                print("  [!] Invalid option. Please enter a number from the menu.")

        except KeyboardInterrupt:
            print("\n\n  [!] Interrupted. Saving data...")
            system.save_data()
            sys.exit(0)
        except Exception as e:
            print(f"\n  [ERROR] An unexpected error occurred: {e}")
            print("  Returning to main menu...\n")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
