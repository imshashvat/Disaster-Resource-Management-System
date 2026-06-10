# models/report.py
# Report model

from datetime import datetime
import random


class Report:
    """Represents a generated report record."""

    REPORT_TYPES = {
        "disaster_summary",
        "resource_utilization",
        "camp_occupancy",
        "volunteer_activity",
        "donation_summary",
    }

    def __init__(self, report_id: str, report_type: str,
                 generated_date: str = None, content: str = ""):
        self.report_id      = report_id
        self.report_type    = report_type
        self.generated_date = generated_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.content        = content

    # ── Instance Methods ──────────────────────────────────────────────────────
    def generate_report(self) -> str:
        """Return report content."""
        return self.content or f"[Empty report: {self.report_type}]"

    def export_report(self, filepath: str) -> None:
        """Export report content to a text file."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Report ID   : {self.report_id}\n")
            f.write(f"Type        : {self.report_type}\n")
            f.write(f"Generated   : {self.generated_date}\n")
            f.write("─" * 60 + "\n")
            f.write(self.content)
        print(f"  Report exported to: {filepath}")

    def display_report(self) -> None:
        print(f"  ┌─ Report ─────────────────────────────────────")
        print(f"  │  Report ID   : {self.report_id}")
        print(f"  │  Type        : {self.report_type}")
        print(f"  │  Generated   : {self.generated_date}")
        print(f"  └─────────────────────────────────────────────")

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "report_id":      self.report_id,
            "report_type":    self.report_type,
            "generated_date": self.generated_date,
            "content":        self.content,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Report":
        return cls(
            report_id      = data["report_id"],
            report_type    = data["report_type"],
            generated_date = data.get("generated_date", ""),
            content        = data.get("content", ""),
        )

    # ── Magic Methods ─────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return f"Report[{self.report_id}] Type: {self.report_type} | {self.generated_date}"

    def __repr__(self) -> str:
        return (f"Report(id={self.report_id!r}, type={self.report_type!r}, "
                f"date={self.generated_date!r})")
