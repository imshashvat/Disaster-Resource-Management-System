# modules/report_manager.py
# ReportManager — Generator-based report engine, CSV export

import csv
import os
import random
from datetime import datetime
from models.report import Report
from utils.decorators import log_report
from utils.helpers import print_header, print_separator


class ReportManager:
    """
    Report generation engine.
    Uses Python generators (yield) to stream records one by one.
    Exports CSV files for disaster relief, donations, and camp occupancy.
    """

    def __init__(self, system):
        self.system = system

    def _new_id(self) -> str:
        return f"RPT{random.randint(10000, 99999)}"

    # ─────────────────────────────────────────────
    # GENERATORS — yield records one by one
    # ─────────────────────────────────────────────
    def generate_disaster_report(self):
        """GENERATOR — yields one disaster record string at a time."""
        for d in self.system.disasters:
            yield (f"ID={d.disaster_id} | Type={d.disaster_type} | "
                   f"Location={d.location} | Severity={d.severity_level} | "
                   f"Status={d.status} | Registered={d.registered_on}")

    def generate_resource_report(self):
        """GENERATOR — yields one resource record at a time."""
        for r in self.system.resources.values():
            yield (f"ID={r.resource_id} | Name={r.resource_name} | "
                   f"Category={r.category} | Qty={r.quantity} {r.unit}")

    def generate_camp_report(self):
        """GENERATOR — yields one camp record at a time."""
        for c in self.system.camps:
            pct = c.occupancy_pct()
            yield (f"ID={c.camp_id} | Name={c.camp_name} | "
                   f"Capacity={c.capacity} | Occupied={c.occupied} | "
                   f"Pct={pct:.1f}% | Location={c.location}")

    def generate_volunteer_report(self):
        """GENERATOR — yields one volunteer record at a time."""
        for v in self.system.volunteers:
            task = v.assigned_task or "Available"
            yield (f"ID={v.volunteer_id} | Name={v.name} | "
                   f"Skill={v.skill} | Task={task}")

    def generate_donation_report(self):
        """GENERATOR — yields one donation record at a time."""
        for d in self.system.donations:
            yield (f"ID={d.donation_id} | Donor={d.donor_name} | "
                   f"Amount=INR{d.amount:.2f} | Type={d.donation_type} | "
                   f"Date={d.donation_date}")

    # ─────────────────────────────────────────────
    # Print Report (consumes generator)
    # ─────────────────────────────────────────────
    def _print_generator(self, gen) -> int:
        count = 0
        for line in gen:
            print(f"  {line}")
            count += 1
        return count

    # ─────────────────────────────────────────────
    # Full Reports — decorated with @log_report
    # ─────────────────────────────────────────────
    @log_report
    def disaster_summary_report(self) -> None:
        print_header("Disaster Summary Report")
        count = self._print_generator(self.generate_disaster_report())
        if count == 0:
            print("  No disaster records.")
        print_separator()
        active = sum(1 for d in self.system.disasters if d.status == "Active")
        print(f"  Total: {count}  |  Active: {active}")

        # Save report record
        rid = self._new_id()
        content = "\n".join(self.generate_disaster_report())
        r = Report(rid, "disaster_summary", content=content)
        self.system.reports.append(r)

    @log_report
    def resource_utilization_report(self) -> None:
        print_header("Resource Utilization Report")
        count = self._print_generator(self.generate_resource_report())
        if count == 0:
            print("  No resource records.")
        print_separator()
        total_qty = sum(r.quantity for r in self.system.resources.values())
        print(f"  Resource Types: {count}  |  Total Units: {total_qty:,}")

    @log_report
    def camp_occupancy_report(self) -> None:
        print_header("Camp Occupancy Report")
        count = self._print_generator(self.generate_camp_report())
        if count == 0:
            print("  No camp records.")
        print_separator()
        total_cap = sum(c.capacity for c in self.system.camps)
        total_occ = sum(c.occupied for c in self.system.camps)
        print(f"  Camps: {count}  |  Total Capacity: {total_cap}  |  Total Occupied: {total_occ}")

    @log_report
    def volunteer_activity_report(self) -> None:
        print_header("Volunteer Activity Report")
        count = self._print_generator(self.generate_volunteer_report())
        if count == 0:
            print("  No volunteer records.")

    # ─────────────────────────────────────────────
    # CSV Exports
    # ─────────────────────────────────────────────
    def export_relief_distribution_csv(self) -> None:
        """Export resource allocations to CSV."""
        path = os.path.join(self.system.data_dir, "relief_distribution.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Resource ID", "Resource Name", "Category", "Quantity", "Unit"])
            for r in self.system.resources.values():
                writer.writerow([r.resource_id, r.resource_name,
                                 r.category, r.quantity, r.unit])
        print(f"  CSV exported: {path}")

    def export_donation_report_csv(self) -> None:
        """Export donation records to CSV."""
        path = os.path.join(self.system.data_dir, "donation_report.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Donation ID", "Donor Name", "Amount (INR)",
                             "Type", "Date", "Note"])
            for d in self.system.donations:
                writer.writerow([d.donation_id, d.donor_name,
                                 f"{d.amount:.2f}", d.donation_type,
                                 d.donation_date, d.note])
        print(f"  CSV exported: {path}")

    def export_camp_occupancy_csv(self) -> None:
        """Export camp occupancy data to CSV."""
        path = os.path.join(self.system.data_dir, "camp_occupancy.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Camp ID", "Camp Name", "Location",
                             "Capacity", "Occupied", "Percentage (%)"])
            for c in self.system.camps:
                writer.writerow([c.camp_id, c.camp_name, c.location,
                                 c.capacity, c.occupied,
                                 f"{c.occupancy_pct():.1f}"])
        print(f"  CSV exported: {path}")

    # ─────────────────────────────────────────────
    # CLI Sub-Menu
    # ─────────────────────────────────────────────
    def menu(self) -> None:
        while True:
            print_header("Report Generation")
            print("  1. Disaster Summary Report")
            print("  2. Resource Utilization Report")
            print("  3. Camp Occupancy Report")
            print("  4. Volunteer Activity Report")
            print("  5. Donation Report")
            print("  ─── CSV Exports ─────────────────────────")
            print("  6. Export Relief Distribution (CSV)")
            print("  7. Export Donation Report (CSV)")
            print("  8. Export Camp Occupancy (CSV)")
            print("  9. Export ALL CSV Reports")
            print("  0. Back to Main Menu")
            print_separator()
            choice = input("  Enter choice: ").strip()

            if choice == "1":
                self.disaster_summary_report()
            elif choice == "2":
                self.resource_utilization_report()
            elif choice == "3":
                self.camp_occupancy_report()
            elif choice == "4":
                self.volunteer_activity_report()
            elif choice == "5":
                print_header("Donation Report")
                self._print_generator(self.generate_donation_report())
                print_separator()
                total = sum(d.amount for d in self.system.donations)
                print(f"  Total Donations: {len(self.system.donations)}  |  "
                      f"Total Funds: INR {total:,.2f}")
            elif choice == "6":
                self.export_relief_distribution_csv()
            elif choice == "7":
                self.export_donation_report_csv()
            elif choice == "8":
                self.export_camp_occupancy_csv()
            elif choice == "9":
                self.export_relief_distribution_csv()
                self.export_donation_report_csv()
                self.export_camp_occupancy_csv()
                print("  All CSV reports exported successfully.")
            elif choice == "0":
                break
            else:
                print("  [!] Invalid choice.")
