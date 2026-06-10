# models/person.py
# Abstract Base Class — Person

from abc import ABC, abstractmethod


class Person(ABC):
    """
    Abstract base class representing any person in the system.
    Inherited by Volunteer and Donor.
    """

    def __init__(self, person_id: str, name: str, contact_number: str, address: str):
        self.person_id      = person_id
        self.name           = name
        self.contact_number = contact_number
        self.address        = address

    # ── Abstract method — must be implemented by subclasses ─────────────────
    @abstractmethod
    def display_details(self) -> None:
        """Display formatted details of the person."""
        pass

    # ── Concrete method shared by all subclasses ─────────────────────────────
    def update_details(self, name: str = None, contact: str = None, address: str = None) -> None:
        """Update one or more fields; None means 'keep existing value'."""
        if name:
            self.name = name
        if contact:
            self.contact_number = contact
        if address:
            self.address = address

    # ── Magic Methods ────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return f"Person[{self.person_id}] {self.name} | {self.contact_number}"

    def __repr__(self) -> str:
        return (f"Person(person_id={self.person_id!r}, name={self.name!r}, "
                f"contact={self.contact_number!r}, address={self.address!r})")
