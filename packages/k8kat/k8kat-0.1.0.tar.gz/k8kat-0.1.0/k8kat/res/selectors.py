"""
Modules contains set of helpers to work with resource selector.

Copyright 2022 nMachine.io
"""
from __future__ import annotations

from typing import Any, List, Optional, Tuple


def _convert_kv_to_exp(
    kv_list: List[Tuple[str, str]], incl: Optional[bool] = True
) -> str:
    """Converts list of tuples to string in format
    k=v or k!=v separated with comma.

    TODO: use operator in or notin for the same "k"
    """
    rets = []
    sep = "=" if incl else "!="
    for name, value in kv_list:
        rets.append(f"{name}{sep}{value}")
    return ",".join(rets)


def join_not_empty(list_to_join: List[str]) -> str:
    """Joins list of string and ignores empty items."""
    return ",".join(item for item in list_to_join if item)


def convert_selectors(query: Any) -> None:
    """Converts fields/not_fields and labels/not_labels
    to field_selector and label_selector."""

    field_selector = [query.get("field_selector", "")]
    if query.get("fields"):
        field_selector.append(_convert_kv_to_exp(query["fields"]))
        del query["fields"]
    if query.get("not_fields"):
        field_selector.append(_convert_kv_to_exp(query["not_fields"], False))
        del query["not_fields"]
    if field_selector:
        field_selector_txt = join_not_empty(field_selector)
        if field_selector_txt:
            query["field_selector"] = field_selector_txt

    label_selector = [query.get("label_selector", "")]
    if query.get("labels"):
        label_selector.append(_convert_kv_to_exp(query["labels"]))
        del query["labels"]
    if query.get("not_labels"):
        label_selector.append(_convert_kv_to_exp(query["not_labels"], False))
        del query["not_labels"]
    if label_selector:
        label_selector_txt = join_not_empty(label_selector)
        if label_selector_txt:
            query["label_selector"] = label_selector_txt
