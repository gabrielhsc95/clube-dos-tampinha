from typing import Any


def convert_lists(obj: object, attribute: str) -> Any:
    value = getattr(obj, attribute)
    if value is None:
        return []
    elif isinstance(value, list):
        return [str(v) for v in value]
    return value
