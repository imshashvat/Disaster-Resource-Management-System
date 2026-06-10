# models/disaster.py
# Disaster class with static and class methods

import random
from datetime import datetime


class Disaster:
    """Represents a registered disaster incident."""

    _total_count: int = 0           # class-level counter
    _all_disasters: list = []       # class-level registry for class methods

    SEVERITY_LABELS = {1: "Minor", 2: "Moderate", 3: "Serious", 4: "Severe", 5: "Catastrophic"}
    VALID_STATUSES = {"Active", "Under Control", "Resolved", "Monitoring"}

    def __init__(self, disaster_id: str, disaster_type: str, location: str,
                 severity_level: int, status: str = "Active",
                 registered_on: str = None):
        self.disaster_id    = disaster_id
        self.disaster_type  = disaster_type
        self.location       = location
        self.severity_level = severity_level          # 1–5
        self.status         = status
        self.registered_on  = registered_on or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        Disaster._total_count += 1
        Disaster._all_disasters.append(self)

    # ── Instance Methods ──────────────────────────────────────────────────────
    def register_disaster(self) -> None:
        """Print confirmation of registration."""
        print(f"  Disaster '{self.disaster_id}' registered successfully.")

    def update_status(self, new_status: str) -> None:
        """Update the disaster status with validation."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose from: {self.VALID_STATUSES}")
        self.status = new_status
        print(f"  Disaster {self.disaster_id} status updated to '{new_status}'.")

    def display_disaster(self) -> None:
        severity_label = self.SEVERITY_LABELS.get(self.severity_level, "Unknown")
        print(f"  ┌─ Disaster ───────────────────────────────────")
        print(f"  │  ID           : {self.disaster_id}")
        print(f"  │  Type         : {self.disaster_type}")
        print(f"  │  Location     : {self.location}")
        print(f"  │  Severity     : {self.severity_level} – {severity_label}")
        print(f"  │  Status       : {self.status}")
        print(f"  │  Registered   : {self.registered_on}")
        print(f"  └──────────────────────────────────────────────")

    # ── Static Method ─────────────────────────────────────────────────────────
    @staticmethod
    def get_emergency_types() -> list:
        """Return a list of known disaster types (static utility)."""
        return ["Flood", "Earthquake", "Cyclone", "Pandemic",
                "Landslide", "Drought", "Tsunami", "Fire", "Other"]

    # ── Class Method ──────────────────────────────────────────────────────────
    @classmethod
    def get_total_count(cls) -> int:
        """Return total number of disaster objects ever created."""
        return cls._total_count

    @classmethod
    def get_active_count(cls) -> int:
        """Return count of disasters with status 'Active'."""
        return sum(1 for d in cls._all_disasters if d.status == "Active")

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "disaster_id":    self.disaster_id,
            "disaster_type":  self.disaster_type,
            "location":       self.location,
            "severity_level": self.severity_level,
            "status":         self.status,
            "registered_on":  self.registered_on,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Disaster":
        obj = cls.__new__(cls)                        # bypass __init__ counter
        obj.disaster_id    = data["disaster_id"]
        obj.disaster_type  = data["disaster_type"]
        obj.location       = data["location"]
        obj.severity_level = data["severity_level"]
        obj.status         = data.get("status", "Active")
        obj.registered_on  = data.get("registered_on", "")
        return obj

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (f"Disaster[{self.disaster_id}] {self.disaster_type} at {self.location} "
                f"| Severity: {self.severity_level} | Status: {self.status}")

    def __repr__(self) -> str:
        return (f"Disaster(id={self.disaster_id!r}, type={self.disaster_type!r}, "
                f"severity={self.severity_level}, status={self.status!r})")
