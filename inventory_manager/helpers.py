def empty_to_none(s: str | None) -> str | None:
    """
    If string is empty returns None
    """
    return None if s == "" else s
