class APIError(ValueError):
    """A safe, user-facing input validation error."""

def bounded_text(value, name="input", limit=300):
    if not isinstance(value, str):
        raise ValueError(f"{name} must be text.")
    if len(value) > limit:
        raise ValueError(f"{name} is too long (maximum {limit} characters).")
    return value
