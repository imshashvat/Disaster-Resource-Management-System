# utils/helpers.py
# Lambda sorts, recursive search, and static utility helpers

from typing import List, Optional


# ─────────────────────────────────────────────
# Recursive Disaster Search
# ─────────────────────────────────────────────

def search_disaster(records: list, search_id: str, index: int = 0) -> Optional[object]:
    """
    Recursively search disaster records by disaster_id.
    Returns the Disaster object if found, else None.
    """
    if index >= len(records):
        return None
    if records[index].disaster_id == search_id:
        return records[index]
    return search_disaster(records, search_id, index + 1)


# ─────────────────────────────────────────────
# Lambda Sort Helpers
# ─────────────────────────────────────────────

def sort_disasters_by_severity(disasters: list) -> list:
    """Sort disasters in descending order of severity (5 = most severe)."""
    return sorted(disasters, key=lambda d: d.severity_level, reverse=True)


def sort_camps_by_occupancy(camps: list) -> list:
    """Sort camps by occupancy percentage (most full first)."""
    return sorted(
        camps,
        key=lambda c: (c.occupied / c.capacity) if c.capacity > 0 else 0,
        reverse=True
    )


def sort_donations_by_amount(donations: list) -> list:
    """Sort donations from largest to smallest."""
    return sorted(donations, key=lambda d: d.amount, reverse=True)


# ─────────────────────────────────────────────
# Static Utility Functions
# ─────────────────────────────────────────────

def get_emergency_helpline() -> str:
    """Return standard emergency helpline information (static utility)."""
    return (
        "\n  ════════ EMERGENCY HELPLINES ════════\n"
        "  National Disaster Management: 1078\n"
        "  Police Emergency:             100\n"
        "  Fire Brigade:                 101\n"
        "  Ambulance:                    102\n"
        "  Flood Helpline:               1800-180-5999\n"
        "  ════════════════════════════════════\n"
    )


def calculate_resources_needed(population: int) -> dict:
    """
    Estimate daily resource requirements for a given population.
    Returns a dictionary with resource type → quantity estimates.
    """
    return {
        "Food Packets":    population * 3,       # 3 meals/day
        "Water (litres)":  population * 4,       # 4 L/day
        "Medicine Kits":   max(1, population // 10),
        "Blankets":        population,
        "Emergency Kits":  max(1, population // 20),
    }


def print_separator(char: str = "─", width: int = 60) -> None:
    """Print a visual separator line."""
    print(char * width)


def print_header(title: str, width: int = 60) -> None:
    """Print a formatted section header."""
    print("\n" + "═" * width)
    print(f"  {title.upper()}")
    print("═" * width)
