from __future__ import annotations

from collections.abc import MutableSequence

__ALL__ = (
    'repr_sequence',
    'repr_dict',
)


def _repr_iter(it, max_length=255, abbrev='...', closings='[]', sep=', '):
    output = []
    combined_length = len(closings)         # counts for closings
    extras_length = len(sep) + len(abbrev)

    for repr_v in it:
        if combined_length + len(repr_v) + extras_length > max_length:
            output.append(abbrev)
            break

        output.append(repr_v)
        combined_length += len(repr_v) + len(sep)

    opening = closings[0]
    closing = closings[-1]

    return f"{opening}{sep.join(output)}{closing}"


def repr_sequence(seq, max_length=255, abbrev='...', closings: str | None = None, sep=', '):
    closings = closings or ('[]' if isinstance(seq, MutableSequence) else '()')
    return _repr_iter(
        (repr(v) for v in seq),
        max_length=max_length,
        abbrev=abbrev,
        closings=closings,
        sep=sep,
    )


def repr_dict(d, max_length=255, abbrev='...', closings='{}', sep=', '):
    return _repr_iter(
        (f"{k!r}: {v!r}" for k, v in d.items()),
        max_length=max_length,
        abbrev=abbrev,
        closings=closings,
        sep=sep,
    )
