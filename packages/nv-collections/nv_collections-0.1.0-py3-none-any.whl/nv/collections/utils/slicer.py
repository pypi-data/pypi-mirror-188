from typing import Sequence, Optional, TypeVar, List


V = TypeVar('V')


__ALL__ = (
    'slice_sequence',
)


def slice_sequence(
        seq: Sequence[V],
        start: Optional[int] = None,
        stop: Optional[int] = None,
        step: Optional[int] = None
        ) -> List[V]:

    length = len(seq)

    # Default parameters for slices
    start, stop, step = start or 0, stop or length, step or 1

    # Deal with negative numbers
    start = start if start >= 0 else length + start
    stop = stop if stop >= 0 else length + stop

    if step < 0 and start < stop:
        start, stop = stop - 1, start - 1

    return [seq.__getitem__(i) for i in range(start, stop, step)]
