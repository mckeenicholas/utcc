"""Utility functions for backend API request handling."""

TRUTHY_PARAM_VALUES = {"true", "1", "t", "yes", "y"}
FALSY_PARAM_VALUES = {"false", "0", "f", "no", "n"}


def is_truthy_param(val: object) -> bool:
    """Check if a query parameter or value represents a truthy boolean."""
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val == 1
    if isinstance(val, str):
        return val.strip().lower() in TRUTHY_PARAM_VALUES
    return False


def is_falsy_param(val: object) -> bool:
    """Check if a query parameter or value represents a falsy boolean."""
    if val is None:
        return False
    if isinstance(val, bool):
        return not val
    if isinstance(val, (int, float)):
        return val == 0
    if isinstance(val, str):
        return val.strip().lower() in FALSY_PARAM_VALUES
    return False
