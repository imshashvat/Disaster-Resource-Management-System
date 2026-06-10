 # utils/validators.py
# Custom Exceptions and Input Validation

# ─────────────────────────────────────────────
# Custom Exception Classes
# ─────────────────────────────────────────────

class InvalidDisasterID(Exception):
    """Raised when a disaster ID does not exist in the registry."""
    pass

class InvalidResourceQuantity(ValueError):
    """Raised when resource quantity is zero, negative, or non-numeric."""
    pass

class CampCapacityExceeded(Exception):
    """Raised when trying to add more people than camp capacity allows."""
    pass

class InvalidDonationEntry(ValueError):
    """Raised when donation amount is invalid (<=0 or non-numeric)."""
    pass

class ResourceNotFound(Exception):
    """Raised when a resource ID is not found in inventory."""
    pass

class InvalidAreaID(Exception):
    """Raised when an area ID does not exist."""
    pass

class InvalidVolunteerID(Exception):
    """Raised when a volunteer ID does not exist."""
    pass

class InvalidCampID(Exception):
    """Raised when a camp ID does not exist."""
    pass


# ─────────────────────────────────────────────
# Input Validation Functions
# ─────────────────────────────────────────────

def validate_non_empty(value: str, field_name: str = "Field") -> str:
    """Ensure a string input is not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_positive_int(value: str, field_name: str = "Value") -> int:
    """Parse and validate that input is a positive integer."""
    try:
        num = int(value)
    except ValueError:
        raise ValueError(f"{field_name} must be an integer, got '{value}'.")
    if num <= 0:
        raise ValueError(f"{field_name} must be greater than 0, got {num}.")
    return num


def validate_positive_float(value: str, field_name: str = "Amount") -> float:
    """Parse and validate that input is a positive float (for donations, etc.)."""
    try:
        num = float(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a number, got '{value}'.")
    if num <= 0:
        raise InvalidDonationEntry(f"{field_name} must be greater than 0, got {num}.")
    return num


def validate_severity(value: str) -> int:
    """Severity must be 1–5."""
    try:
        level = int(value)
    except ValueError:
        raise ValueError("Severity level must be an integer between 1 and 5.")
    if level < 1 or level > 5:
        raise ValueError(f"Severity level must be 1–5, got {level}.")
    return level


def get_input(prompt: str, validator=None, field_name: str = "Input"):
    """
    Prompt user for input, optionally running a validator.
    Retries on validation error.
    """
    while True:
        raw = input(prompt)
        try:
            if validator:
                return validator(raw, field_name)
            return raw.strip()
        except (ValueError, InvalidDonationEntry, InvalidResourceQuantity) as e:
            print(f"  [!] Invalid input — {e}  Try again.")
