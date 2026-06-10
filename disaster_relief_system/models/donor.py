# models/donor.py
# Donor — inherits Person (with ENCAPSULATION via name mangling)

from models.person import Person
from datetime import datetime


class Donor(Person):
    """
    Represents a donor in the system.
    Sensitive attributes (donor_id, donation_amount) are name-mangled
    to enforce encapsulation — accessible only via getter/setter methods.
    """

    def __init__(self, person_id: str, name: str, contact_number: str,
                 address: str, donor_id: str, donation_type: str = "Cash"):
        super().__init__(person_id, name, contact_number, address)
        self.__donor_id        = donor_id          # name-mangled
        self.__donation_amount = 0.0               # name-mangled
        self.donation_type     = donation_type
        self.__donation_history: list = []

    # ── Getters / Setters (Encapsulation) ────────────────────────────────────
    def get_donor_id(self) -> str:
        return self.__donor_id

    def get_donation_amount(self) -> float:
        return self.__donation_amount

    def set_donation_type(self, dtype: str) -> None:
        self.donation_type = dtype

    # ── Donation Methods ──────────────────────────────────────────────────────
    def donate(self, amount: float, note: str = "") -> None:
        """Record a new donation and add to history."""
        if amount <= 0:
            raise ValueError("Donation amount must be positive.")
        self.__donation_amount += amount
        entry = {
            "amount":    amount,
            "type":      self.donation_type,
            "note":      note,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.__donation_history.append(entry)
        print(f"  Donation of ₹{amount:.2f} recorded for {self.name}. Total: ₹{self.__donation_amount:.2f}")

    def view_donation_history(self) -> None:
        """Display full donation history for this donor."""
        print(f"\n  Donation History for {self.name} [{self.__donor_id}]")
        if not self.__donation_history:
            print("  No donations on record.")
            return
        for i, entry in enumerate(self.__donation_history, 1):
            print(f"  {i}. ₹{entry['amount']:.2f} ({entry['type']}) "
                  f"on {entry['timestamp']}  {entry.get('note', '')}")
        print(f"  ─────────────────────────────────────────────")
        print(f"  Total Donated: ₹{self.__donation_amount:.2f}")

    # ── Polymorphic display_details (overrides abstract) ─────────────────────
    def display_details(self) -> None:
        print(f"  ┌─ Donor ──────────────────────────────────────")
        print(f"  │  Donor ID    : {self.__donor_id}")
        print(f"  │  Name        : {self.name}")
        print(f"  │  Contact     : {self.contact_number}")
        print(f"  │  Address     : {self.address}")
        print(f"  │  Type        : {self.donation_type}")
        print(f"  │  Total Given : ₹{self.__donation_amount:.2f}")
        print(f"  └──────────────────────────────────────────────")

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "person_id":        self.person_id,
            "name":             self.name,
            "contact_number":   self.contact_number,
            "address":          self.address,
            "donor_id":         self.__donor_id,
            "donation_type":    self.donation_type,
            "donation_amount":  self.__donation_amount,
            "donation_history": self.__donation_history,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Donor":
        obj = cls(
            person_id      = data["person_id"],
            name           = data["name"],
            contact_number = data["contact_number"],
            address        = data["address"],
            donor_id       = data["donor_id"],
            donation_type  = data.get("donation_type", "Cash"),
        )
        obj._Donor__donation_amount  = data.get("donation_amount", 0.0)
        obj._Donor__donation_history = data.get("donation_history", [])
        return obj

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (f"Donor[{self.__donor_id}] {self.name} | "
                f"Type: {self.donation_type} | Total: ₹{self.__donation_amount:.2f}")

    def __repr__(self) -> str:
        return (f"Donor(donor_id={self.__donor_id!r}, name={self.name!r}, "
                f"total={self.__donation_amount!r})")
