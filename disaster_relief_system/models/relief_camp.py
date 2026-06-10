# models/relief_camp.py
# ReliefCamp class with static class-level tracking

from datetime import datetime
from utils.validators import CampCapacityExceeded


class ReliefCamp:
    """Represents a relief camp for displaced persons."""

    _total_capacity: int = 0     # class-level aggregate

    def __init__(self, camp_id: str, camp_name: str, location: str,
                 capacity: int, occupied: int = 0, created_on: str = None):
        self.camp_id    = camp_id
        self.camp_name  = camp_name
        self.location   = location
        self.capacity   = capacity
        self.occupied   = occupied
        self.created_on = created_on or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ReliefCamp._total_capacity += capacity

    # ── Instance Methods ──────────────────────────────────────────────────────
    def add_camp(self) -> None:
        print(f"  Relief camp '{self.camp_name}' [{self.camp_id}] added. Capacity: {self.capacity}.")

    def allocate_people(self, count: int) -> None:
        """Admit 'count' people; raises CampCapacityExceeded if over limit."""
        if self.occupied + count > self.capacity:
            available = self.capacity - self.occupied
            raise CampCapacityExceeded(
                f"Cannot add {count} people. Only {available} spots available in '{self.camp_name}'."
            )
        self.occupied += count
        print(f"  {count} people admitted to '{self.camp_name}'. "
              f"Occupancy: {self.occupied}/{self.capacity} "
              f"({self.occupancy_pct():.1f}%)")

    def release_people(self, count: int) -> None:
        """Release count people from the camp."""
        self.occupied = max(0, self.occupied - count)
        print(f"  {count} people released from '{self.camp_name}'. "
              f"Occupancy now: {self.occupied}/{self.capacity}")

    def occupancy_pct(self) -> float:
        return (self.occupied / self.capacity * 100) if self.capacity > 0 else 0.0

    def available_spots(self) -> int:
        return self.capacity - self.occupied

    def display_camp_details(self) -> None:
        pct = self.occupancy_pct()
        print(f"  ┌─ Relief Camp ────────────────────────────────")
        print(f"  │  Camp ID     : {self.camp_id}")
        print(f"  │  Name        : {self.camp_name}")
        print(f"  │  Location    : {self.location}")
        print(f"  │  Capacity    : {self.capacity}")
        print(f"  │  Occupied    : {self.occupied} ({pct:.1f}%)")
        print(f"  │  Available   : {self.available_spots()}")
        print(f"  │  Created On  : {self.created_on}")
        print(f"  └─────────────────────────────────────────────")

    # ── Class Method ──────────────────────────────────────────────────────────
    @classmethod
    def get_total_capacity(cls) -> int:
        """Return aggregate capacity of all camps ever created."""
        return cls._total_capacity

    # ── Static Method ─────────────────────────────────────────────────────────
    @staticmethod
    def minimum_camp_size() -> int:
        """Return the minimum recommended camp capacity per policy."""
        return 50

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "camp_id":    self.camp_id,
            "camp_name":  self.camp_name,
            "location":   self.location,
            "capacity":   self.capacity,
            "occupied":   self.occupied,
            "created_on": self.created_on,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ReliefCamp":
        obj = cls.__new__(cls)      # skip _total_capacity increment on load
        obj.camp_id    = data["camp_id"]
        obj.camp_name  = data["camp_name"]
        obj.location   = data["location"]
        obj.capacity   = data["capacity"]
        obj.occupied   = data.get("occupied", 0)
        obj.created_on = data.get("created_on", "")
        return obj

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (f"Camp[{self.camp_id}] {self.camp_name} @ {self.location} "
                f"| {self.occupied}/{self.capacity} ({self.occupancy_pct():.1f}%)")

    def __repr__(self) -> str:
        return (f"ReliefCamp(id={self.camp_id!r}, name={self.camp_name!r}, "
                f"capacity={self.capacity}, occupied={self.occupied})")
