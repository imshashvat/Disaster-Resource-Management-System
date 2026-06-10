# models/donation.py
# Donation — represents a single donation transaction

from datetime import datetime
import random
import string


class Donation:
    """Represents a single donation transaction."""

    def __init__(self, donation_id: str, donor_name: str, amount: float,
                 donation_type: str = "Cash", note: str = "",
                 donation_date: str = None):
        self.donation_id   = donation_id
        self.donor_name    = donor_name
        self.amount        = amount
        self.donation_type = donation_type
        self.note          = note
        self.donation_date = donation_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Instance Methods ──────────────────────────────────────────────────────
    def add_donation(self) -> None:
        print(f"  Donation [{self.donation_id}] of ₹{self.amount:.2f} "
              f"from '{self.donor_name}' recorded.")

    def generate_receipt(self) -> str:
        """Return a formatted donation receipt string."""
        receipt = (
            f"\n  ╔══════════ DONATION RECEIPT ══════════╗\n"
            f"  ║  Receipt ID   : {self.donation_id:<20} ║\n"
            f"  ║  Donor Name   : {self.donor_name:<20} ║\n"
            f"  ║  Amount       : ₹{self.amount:<19.2f} ║\n"
            f"  ║  Type         : {self.donation_type:<20} ║\n"
            f"  ║  Date         : {self.donation_date:<20} ║\n"
            f"  ║  Note         : {(self.note or 'N/A'):<20} ║\n"
            f"  ╚══════════════════════════════════════╝"
        )
        return receipt

    def display_donation(self) -> None:
        print(f"  ┌─ Donation ───────────────────────────────────")
        print(f"  │  ID          : {self.donation_id}")
        print(f"  │  Donor       : {self.donor_name}")
        print(f"  │  Amount      : ₹{self.amount:.2f}")
        print(f"  │  Type        : {self.donation_type}")
        print(f"  │  Date        : {self.donation_date}")
        print(f"  │  Note        : {self.note or 'N/A'}")
        print(f"  └─────────────────────────────────────────────")

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "donation_id":   self.donation_id,
            "donor_name":    self.donor_name,
            "amount":        self.amount,
            "donation_type": self.donation_type,
            "note":          self.note,
            "donation_date": self.donation_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Donation":
        return cls(
            donation_id   = data["donation_id"],
            donor_name    = data["donor_name"],
            amount        = data["amount"],
            donation_type = data.get("donation_type", "Cash"),
            note          = data.get("note", ""),
            donation_date = data.get("donation_date", ""),
        )

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (f"Donation[{self.donation_id}] {self.donor_name} — "
                f"₹{self.amount:.2f} ({self.donation_type}) on {self.donation_date}")

    def __repr__(self) -> str:
        return (f"Donation(id={self.donation_id!r}, donor={self.donor_name!r}, "
                f"amount={self.amount}, type={self.donation_type!r})")
