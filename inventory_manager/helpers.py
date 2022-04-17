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


def noneable_int(s: str | None) -> int | None:
    """
    Empty string is converted into None,
    else is converted into a int
    """
    return None if s in ("", None) else int(s)
