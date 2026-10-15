"""Encoding that preserves the API's wire representation."""
from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Mapping
from urllib.parse import quote

from ._types import Unset


def endpoint_path(template: str, values: Mapping[str, Any]) -> str:
    for name, value in values.items():
        text = str(value)
        if text in {"", ".", ".."}:
            raise ValueError(f"Invalid path parameter {name}")
        template = template.replace("{" + name + "}", quote(text, safe=""))
    return template


def json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: json_value(v) for k, v in value.items() if not isinstance(v, Unset)}
    if isinstance(value, (list, tuple)):
        return [json_value(v) for v in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    return value


def query_pairs(params: Mapping[str, Any] | None) -> list[tuple[str, str]]:
    pairs = []
    for key, value in (params or {}).items():
        if isinstance(value, Unset) or value is None:
            continue
        for item in value if isinstance(value, (list, tuple)) else [value]:
            item = json_value(item)
            pairs.append((key, str(item).lower() if isinstance(item, bool) else str(item)))
    return pairs

