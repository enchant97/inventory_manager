def empty_to_none(s: str | None) -> str | None:
    """
    If string is empty returns None
    """
    return None if s == "" else s


def none_to_empty(s: str | None) -> str:
    """
    None is converted into an empty string
    """
    return "" if s is None else s
