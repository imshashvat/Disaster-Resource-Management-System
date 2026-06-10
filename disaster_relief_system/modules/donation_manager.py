# modules/donation_manager.py
# DonationManager — Register donations, track donors, manage funds

import random
from datetime import datetime
from models.donation import Donation
from models.donor import Donor
from utils.validators import InvalidDonationEntry
from utils.decorators import log_donation
from utils.helpers import sort_donations_by_amount, print_header, print_separator


class DonationManager:
    """Manages donations and donor records."""

    def __init__(self, system):
        self.system = system

    def _new_donation_id(self) -> str:
        return f"DON{random.randint(10000, 99999)}"

    def _new_donor_ids(self) -> tuple:
        n = random.randint(1000, 9999)
        return f"PER{n}", f"DNR{n}"

    # ─────────────────────────────────────────────
    # Add Donation  — decorated with @log_donation
    # ─────────────────────────────────────────────
    @log_donation
    def add_donation(self, donor_name: str, amount: float,
                     donation_type: str = "Cash", note: str = "") -> Donation:
        """Record a donation transaction; auto-generates receipt."""
        if amount <= 0:
            raise InvalidDonationEntry("Donation amount must be greater than zero.")

        did = self._new_donation_id()
        while any(d.donation_id == did for d in self.system.donations):
            did = self._new_donation_id()

        donation = Donation(did, donor_name, amount, donation_type, note)
        self.system.donations.append(donation)
        donation.add_donation()
        print(donation.generate_receipt())
        return donation

    # ─────────────────────────────────────────────
    # Register Donor (Donor object with full history)
    # ─────────────────────────────────────────────
    def register_donor(self, name: str, contact: str, address: str,
                       donation_type: str = "Cash") -> Donor:
        pid, drid = self._new_donor_ids()
        donor = Donor(pid, name, contact, address, drid, donation_type)
        self.system.donors.append(donor)
        print(f"  Donor registered: {drid} — {name}")
        return donor

    # ─────────────────────────────────────────────
    # View
    # ─────────────────────────────────────────────
    def view_all_donations(self, sort_by_amount: bool = False) -> None:
        if not self.system.donations:
            print("  No donations recorded.")
            return
        records = (sort_donations_by_amount(self.system.donations)
                   if sort_by_amount else self.system.donations)
        for d in records:
            d.display_donation()

    def view_donors(self) -> None:
        if not self.system.donors:
            print("  No donors registered.")
            return
        for d in self.system.donors:
            d.display_details()

    def fund_summary(self) -> None:
        """Show total funds collected."""
        total = sum(d.amount for d in self.system.donations)
        by_type: dict = {}
        for d in self.system.donations:
            by_type[d.donation_type] = by_type.get(d.donation_type, 0) + d.amount

        print(f"  Total Donations : {len(self.system.donations)}")
        print(f"  Total Funds     : INR {total:,.2f}")
        print_separator()
        for dtype, amt in by_type.items():
            print(f"  {dtype:<20}: INR {amt:,.2f}")

    def generate_donation_report(self) -> None:
        """Display sorted donation report."""
        print_header("Donation Report")
        self.view_all_donations(sort_by_amount=True)
        print_separator()
        self.fund_summary()

    # ─────────────────────────────────────────────
    # CLI Sub-Menu
    # ─────────────────────────────────────────────
    def menu(self) -> None:
        while True:
            print_header("Donation Management")
            print("  1. Register New Donation")
            print("  2. Register New Donor")
            print("  3. View Donor History")
            print("  4. View All Donations")
            print("  5. View Donations (by Amount)")
            print("  6. Fund Summary")
            print("  7. Donation Report")
            print("  0. Back to Main Menu")
            print_separator()
            choice = input("  Enter choice: ").strip()

            if choice == "1":
                self._add_donation_ui()
            elif choice == "2":
                self._register_donor_ui()
            elif choice == "3":
                self._donor_history_ui()
            elif choice == "4":
                print_header("All Donations")
                self.view_all_donations()
            elif choice == "5":
                print_header("Donations by Amount")
                self.view_all_donations(sort_by_amount=True)
            elif choice == "6":
                print_header("Fund Summary")
                self.fund_summary()
            elif choice == "7":
                self.generate_donation_report()
            elif choice == "0":
                break
            else:
                print("  [!] Invalid choice.")

    def _add_donation_ui(self) -> None:
        print_header("Register Donation")
        name = input("  Donor Name: ").strip() or "Anonymous"
        amt_raw = input("  Amount (INR): ").strip()
        try:
            amount = float(amt_raw)
            if amount <= 0:
                raise InvalidDonationEntry("Amount must be positive.")
        except ValueError:
            print("  [!] Invalid amount.")
            return
        print("  Types: Cash, Kind, Online, Food, Clothing, Medicine")
        dtype = input("  Donation Type (default: Cash): ").strip().title() or "Cash"
        note  = input("  Note (optional): ").strip()
        try:
            self.add_donation(name, amount, dtype, note)
        except InvalidDonationEntry as e:
            print(f"  [!] {e}")

    def _register_donor_ui(self) -> None:
        print_header("Register Donor")
        name    = input("  Full Name: ").strip() or "Anonymous"
        contact = input("  Contact: ").strip() or "N/A"
        address = input("  Address: ").strip() or "N/A"
        dtype   = input("  Preferred Donation Type: ").strip().title() or "Cash"
        self.register_donor(name, contact, address, dtype)

    def _donor_history_ui(self) -> None:
        self.view_donors()
        # Display donation history for a specific donor object
        # (uses Donor.view_donation_history which uses encapsulated private attribute)
        dname = input("  Enter Donor Name to view history (or press Enter to skip): ").strip()
        if dname:
            found = [d for d in self.system.donors
                     if d.name.lower() == dname.lower()]
            if found:
                found[0].view_donation_history()
            else:
                print(f"  [!] Donor '{dname}' not found.")
