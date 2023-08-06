from __future__ import annotations

from typing import Mapping, Collection, Any

from ..singletons import EMPTY, Empty


__ALL__ = (
    'get_nested',
)


def _get_nested(
        m: Mapping[str, Any] | Collection[Any],
        path: list[int | str],
        default: Empty | Any = EMPTY,
        sentinel: Empty | Any = EMPTY,
        sentinel_level: int = 0,
        ):
    node, level = m, 0

    for level, node_key in enumerate(path):
        if sentinel is not EMPTY and level >= sentinel_level and node_key == sentinel:
            return sentinel, level

        try:
            node = node.__getitem__(node_key)
        except (IndexError, KeyError):
            return default, level

    return node, level


def get_nested(
        m: Mapping[str, Any],
        path: list[int | str],
        default=EMPTY,
        sentinel=EMPTY,
        sentinel_level: int = 0
        ):
    result, level = _get_nested(m, path, default=default, sentinel=sentinel, sentinel_level=sentinel_level)

    if result is EMPTY:
        path_msg = [f"[{p!r}]" for p in path]
        under_msg = [('^' if i is level else ' ') * len(p) for i, p in enumerate(path_msg)]
        raise KeyError(f"missing index or key: {path_msg!s}\n"
                       f"                      {under_msg!s}\n\n")

    return result
