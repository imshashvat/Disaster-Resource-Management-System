# utils/decorators.py
# Logging Decorator Factory for Resource Allocation, Donation Processing, and Report Generation

from datetime import datetime
import functools


def log_action(action_name: str):
    """
    Decorator factory that wraps a function with timestamped log messages.
    Usage:
        @log_action('Resource Allocation')
        def allocate_resource(...):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n  [LOG {timestamp_start}] >> {action_name} initiated")
            result = func(*args, **kwargs)
            timestamp_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"  [LOG {timestamp_end}] OK {action_name} complete\n")
            return result
        return wrapper
    return decorator


# ── Named decorator instances for convenience ──────────────────────────────────
log_allocation = log_action("Resource Allocation")
log_donation   = log_action("Donation Processing")
log_report     = log_action("Report Generation")
