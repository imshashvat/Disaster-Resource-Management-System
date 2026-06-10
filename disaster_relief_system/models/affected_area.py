# models/affected_area.py
# AffectedArea class — stores fixed geographical coordinates as a Tuple

from datetime import datetime


class AffectedArea:
    """
    Represents an area affected by a disaster.
    location_coords is stored as a fixed Tuple (lat, lng) — immutable.
    """

    DAMAGE_LEVELS = {"Low", "Medium", "High", "Critical"}

    def __init__(self, area_id: str, area_name: str, affected_population: int,
                 damage_level: str, disaster_id: str = None,
                 location_coords: tuple = (0.0, 0.0),
                 added_on: str = None):
        self.area_id              = area_id
        self.area_name            = area_name
        self.affected_population  = affected_population
        self.damage_level         = damage_level
        self.disaster_id          = disaster_id
        self.location_coords      = tuple(location_coords)   # TUPLE — fixed geo coords
        self.added_on             = added_on or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Instance Methods ──────────────────────────────────────────────────────
    def add_area(self) -> None:
        print(f"  Area '{self.area_name}' [{self.area_id}] added successfully.")

    def update_area(self, population: int = None, damage: str = None) -> None:
        """Update population count or damage level."""
        if population is not None and population >= 0:
            self.affected_population = population
        if damage and damage in self.DAMAGE_LEVELS:
            self.damage_level = damage
        print(f"  Area '{self.area_name}' updated.")

    def display_area(self) -> None:
        print(f"  ┌─ Affected Area ─────────────────────────────")
        print(f"  │  Area ID     : {self.area_id}")
        print(f"  │  Name        : {self.area_name}")
        print(f"  │  Population  : {self.affected_population:,}")
        print(f"  │  Damage      : {self.damage_level}")
        print(f"  │  Disaster ID : {self.disaster_id or 'N/A'}")
        print(f"  │  Coordinates : {self.location_coords}")
        print(f"  │  Added On    : {self.added_on}")
        print(f"  └─────────────────────────────────────────────")

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "area_id":             self.area_id,
            "area_name":           self.area_name,
            "affected_population": self.affected_population,
            "damage_level":        self.damage_level,
            "disaster_id":         self.disaster_id,
            "location_coords":     list(self.location_coords),   # JSON-serializable
            "added_on":            self.added_on,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AffectedArea":
        return cls(
            area_id              = data["area_id"],
            area_name            = data["area_name"],
            affected_population  = data["affected_population"],
            damage_level         = data["damage_level"],
            disaster_id          = data.get("disaster_id"),
            location_coords      = tuple(data.get("location_coords", [0.0, 0.0])),
            added_on             = data.get("added_on", ""),
        )

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (f"Area[{self.area_id}] {self.area_name} | "
                f"Pop: {self.affected_population:,} | Damage: {self.damage_level}")

    def __repr__(self) -> str:
        return (f"AffectedArea(id={self.area_id!r}, name={self.area_name!r}, "
                f"pop={self.affected_population}, damage={self.damage_level!r})")
