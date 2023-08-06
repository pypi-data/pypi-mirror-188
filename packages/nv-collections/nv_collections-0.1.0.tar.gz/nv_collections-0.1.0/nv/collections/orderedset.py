from __future__ import annotations

import sys
from collections.abc import MutableSet, Set, Sequence
from collections import OrderedDict
from functools import total_ordering
from itertools import repeat
from typing import TypeVar, Iterable, Iterator


__ALL__ = ['OrderedSet']


_KEY_ONLY = object()

V = TypeVar('V')


@total_ordering
class OrderedSet(MutableSet[V]):
    """
    Since CPython 3.6, dictionaries are ordered at implementation and tend to be much faster than any pure
    Python implementation. For versions older than 3.6, OrderedDict is used instead.
    OrderedSet is a wrapper over an ordered dict. Set values are stored as keys. All values point to the same
    dummy object (_KEY_ONLY).
    """

    OrderedMapping = dict if sys.version_info >= (3, 6) else OrderedDict

    def __init__(self, items: Iterable[V] | None = None):
        self._mapping = self.OrderedMapping(zip(items, repeat(_KEY_ONLY))) if items else self.OrderedMapping()

    def __repr__(self):
        return f'{self.__class__.__name__}({list(self)!r})'

    def __hash__(self):
        return hash(tuple(self._mapping.keys()))

    # Set required methods
    # By implementing these, we gain all comparisons, booleans and isdisjoint
    def __contains__(self, x: object) -> bool:
        return x in self._mapping

    def __iter__(self) -> Iterator[V]:
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)

    # We need to reimplement comparisons, as sets do not compare with sequences
    # but OrderedSet does
    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            # When comparing to other OrderedSet, order matters
            return (other is self) or (tuple(self._mapping) == tuple(other._mapping))
        elif isinstance(other, Sequence):
            return tuple(self._mapping) == tuple(other)
        elif isinstance(other, Set):
            return set(self._mapping) == other
        return super().__eq__(other)

    def __lt__(self, other):
        if isinstance(other, OrderedSet):
            return (other is not self) and (tuple(self._mapping) < tuple(other._mapping))
        elif isinstance(other, Sequence):
            return tuple(self._mapping) < tuple(other)
        elif isinstance(other, Set):
            return set(self._mapping) < other
        return super().__lt__(other)

    # MutableSet required methods
    # By implementing these, we gain all clear, pop and i-ops

    def add(self, value: V):
        self._mapping.update({value: _KEY_ONLY})

    def discard(self, value: V):
        del self._mapping[value]

    # Additional methods to complement sets
    def __copy__(self):
        return OrderedSet(self._mapping.copy())

    def copy(self):
        return self.__copy__()

    # Additional Sequence methods that work here
    def __reversed__(self):
        return iter(reversed(self._mapping))
