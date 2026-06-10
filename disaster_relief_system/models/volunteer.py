# models/volunteer.py
# Volunteer — inherits Person

from models.person import Person
from datetime import datetime


class Volunteer(Person):
    """
    Represents a registered volunteer in the disaster relief system.
    Inherits from abstract Person class.
    """

    def __init__(self, person_id: str, name: str, contact_number: str,
                 address: str, volunteer_id: str, skill: str, assigned_task: str = None):
        super().__init__(person_id, name, contact_number, address)
        self.volunteer_id  = volunteer_id
        self.skill         = skill
        self.assigned_task = assigned_task   # None = available

    # ── Task Methods ─────────────────────────────────────────────────────────
    def assign_task(self, task: str) -> None:
        """Assign a rescue task to this volunteer."""
        self.assigned_task = task
        print(f"  Task '{task}' assigned to volunteer {self.name}.")

    def view_task(self) -> str:
        """Return the current task or 'Available' if none."""
        if self.assigned_task:
            return f"Current Task: {self.assigned_task}"
        return "Status: Available (no task assigned)"

    def complete_task(self) -> None:
        """Mark the current task as complete, freeing the volunteer."""
        self.assigned_task = None

    # ── Polymorphic display_details (overrides abstract) ─────────────────────
    def display_details(self) -> None:
        print(f"  ┌─ Volunteer ─────────────────────────────────")
        print(f"  │  ID          : {self.volunteer_id}")
        print(f"  │  Name        : {self.name}")
        print(f"  │  Contact     : {self.contact_number}")
        print(f"  │  Address     : {self.address}")
        print(f"  │  Skill       : {self.skill}")
        print(f"  │  Task        : {self.assigned_task or 'Available'}")
        print(f"  └─────────────────────────────────────────────")

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "person_id":      self.person_id,
            "name":           self.name,
            "contact_number": self.contact_number,
            "address":        self.address,
            "volunteer_id":   self.volunteer_id,
            "skill":          self.skill,
            "assigned_task":  self.assigned_task,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Volunteer":
        return cls(
            person_id      = data["person_id"],
            name           = data["name"],
            contact_number = data["contact_number"],
            address        = data["address"],
            volunteer_id   = data["volunteer_id"],
            skill          = data["skill"],
            assigned_task  = data.get("assigned_task"),
        )

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        task = self.assigned_task or "Available"
        return f"Volunteer[{self.volunteer_id}] {self.name} | Skill: {self.skill} | Task: {task}"

    def __repr__(self) -> str:
        return (f"Volunteer(volunteer_id={self.volunteer_id!r}, name={self.name!r}, "
                f"skill={self.skill!r}, task={self.assigned_task!r})")
