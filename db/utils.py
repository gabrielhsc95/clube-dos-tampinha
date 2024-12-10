from typing import Any


def convert_none_to_empty_list(obj: object, attribute: str) -> Any:
    value = getattr(obj, attribute)
    if value is None:
        return []
    return value
