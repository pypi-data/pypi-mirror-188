from __future__ import annotations

from collections import deque
from collections.abc import Sequence, MutableSequence
from copy import copy
from dataclasses import dataclass
from functools import total_ordering
from typing import TypeVar, List, Tuple, Iterator

from ..singletons import Empty, EMPTY
from ..utils import slice_sequence


__ALL__ = (
    'ChainSequence',
    'MutableChainSequence'
)


V = TypeVar('V')


@dataclass(frozen=True, eq=True)
class ItemPosition:
    seq_index: int
    item_index: int
    item: Empty | V


@total_ordering
class ChainSequence(Sequence[V]):
    """Extends the `Sequence` implementation to work as a chain of sequences.

    This is used in order to allow general order between sequences to be preserved,
    while allowing mutation to occur inside each sequence,
    in a similar way that `ChainMap` from `collections` works with mappings.

    Differently from the native `ChainMap` implementation,
    `ChainSequence` has to handle order under mutation,
    which is a bit tricky when you are dealing with positions
    that are both the end of a sequence or the start of another internal sequence.

    """

    def __init__(self, *seqs: Sequence[V], non_mutable_chain=False):
        seqs = ([], ) if seqs == () else seqs
        self.sequences = tuple(seqs) if non_mutable_chain else list(seqs)

    def _iter_possible_positions(self, index: int) -> Iterator[ItemPosition]:
        # The iterator below will return all possible positions
        # for an index to exist in a sequence of lists
        total_length = self.__len__()
        num_seqs = len(self.sequences)

        # Deals with negative indices transforming them into their positive equivalent
        adj_index = (total_length + index) if index < 0 else index

        # This will not perform any boundaries check,
        # but cap to the extreme insert points
        adj_index = min(max(adj_index, 0), total_length)

        acc_len = 0
        for seq_index, seq in enumerate(self.sequences):
            acc_len = acc_len + len(seq)
            if acc_len >= adj_index:
                rel_pos = (adj_index - acc_len + len(seq)) if len(seq) else 0
                elm = seq[rel_pos] if rel_pos < len(seq) else EMPTY

                if acc_len == adj_index:
                    # Those will be valid prepend positions
                    yield ItemPosition(seq_index, rel_pos, elm)
                else:
                    # This will yield at least the next busy position
                    yield ItemPosition(seq_index, rel_pos, elm)

                    # And continue only if the position is the appending point of the sequence
                    # and there are more empty sequences on the row
                    if rel_pos < len(seq) or (seq_index < num_seqs - 1 and self.sequences[seq_index + 1]):
                        break

    def _get_item_position(self, index: int) -> ItemPosition:
        total_length = len(self)

        # Deals with negative indices transforming them into their positive equivalent
        adj_index = (total_length + index) if index < 0 else index

        # Has to handle error cases, as _iter_possible_positions will not
        if adj_index < 0 or adj_index > len(self):
            raise IndexError(f'{index} is out of bounds for {self!r}')

        busy_position = next(pos for pos in (self._iter_possible_positions(adj_index)) if pos.item is not EMPTY)

        return busy_position

    def flatten(self):
        return list(iter(self))

    # Sequence implementation
    def __getitem__(self, index: int | slice) -> V | List[V]:
        if isinstance(index, slice):
            return slice_sequence(self, index.start, index.stop, index.step)\

        return self._get_item_position(index).item

    def __len__(self) -> int:
        return sum(len(seq) for seq in self.sequences)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.sequences)[1:-1]})"

    def __iter__(self) -> Iterator[V]:
        for seq in self.sequences:
            yield from iter(seq)

    # Additional methods to replicate list behaviour
    def _build(self, seqs):
        return self.__class__(*seqs, non_mutable_chain=isinstance(self.sequences, tuple))

    def copy(self):
        return self._build([copy(seq) for seq in self.sequences])

    def __add__(self, other):
        if isinstance(other, ChainSequence):
            return self._build([*self.sequences, *other.sequences])

        if isinstance(other, Sequence):
            return self._build([*self.sequences, other])

        return NotImplemented

    def __radd__(self, other):
        # This will be called if the left side does not know how to add the right side
        return other + self.flatten()

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return self._build(self.sequences * other)

    def __rmul__(self, other):
        if isinstance(other, int):
            return self * other

        return other * self.flatten()

    def __eq__(self, other):
        # Matches ChainMap behaviour
        if self is other:
            return True

        if isinstance(other, self.__class__):
            other = other.flatten()

        return self.flatten() == other

    def __lt__(self, other):
        # Matches list behaviour
        if self is other:
            return False

        if isinstance(other, self.__class__):
            other = other.flatten()

        return self.flatten() < other


class MutableChainSequence(ChainSequence, MutableSequence[V]):
    # Mutable ChainList introduces lots of conflicting borderline cases to be dealt with
    # when insert occurs at non-unique positions

    # We will adopt the "least mutation" principle, which tends to preserve the middle sequence if
    # only prepends and appends are made

    # Mid-point insertion is no-brainer
    # Prepend of the middle list will become append of a previous sequence if it exists
    # Append of the middle list will become prepend of a subsequent sequence if it exists

    sequences: List[MutableSequence[V]] | Tuple[MutableSequence[V]]

    def __init__(self, *seqs: MutableSequence[V], non_mutable_chain=False):
        super().__init__(*seqs, non_mutable_chain=non_mutable_chain)

    def _get_possible_positions(self, index: int) -> list[ItemPosition]:
        return list(self._iter_possible_positions(index))

    def _append(self, value: V):
        # If the sequence is empty, we will append to the last sequence possible
        if len(self) == 0:
            return self.sequences[-1].append(value)

        # Append points
        append_points = self._get_possible_positions(index=len(self))

        # Get the two innermost append points
        innermost_append_points = deque(reversed(append_points), maxlen=2)

        # If there is a sequence of free positions, this will ensure that we get
        # the first outermost empty point available
        append_point = innermost_append_points[0]

        self.sequences[append_point.seq_index].insert(append_point.item_index, value)

    def _prepend(self, value: V):
        # If the sequence is empty, we will prepend to the first sequence possible
        if len(self) == 0:
            return self.sequences[0].insert(0, value)

        # Get the two innermost prepend points
        innermost_prepend_points = deque(self._iter_possible_positions(0), maxlen=2)

        # If there is a sequence of free positions, this will ensure that we get
        # the first outermost empty point available
        prepend_point = innermost_prepend_points[0]

        self.sequences[prepend_point.seq_index].insert(prepend_point.item_index, value)

    def _insert(self, index, value):
        length = len(self)

        # This will deal with the extremes
        # First item will always be appended
        if index >= length:
            return self._append(value)
        elif index == 0:
            return self._prepend(value)

        # This will grab the innermost prepend point possible from left to right
        insert_points = deque(self._iter_possible_positions(index), maxlen=20)

        mid_list = (len(self.sequences) // 2 + 1) if len(self.sequences) > 1 else 1

        # Check in which extreme we are
        if insert_points[-1].seq_index < mid_list:
            # We are on the left side of the sequence
            insert_point = insert_points[0]
        else:
            insert_point = insert_points[-1]

        return self.sequences[insert_point.seq_index].insert(insert_point.item_index, value)

    # Mutable sequence implementations
    def insert(self, index: int, value: V):
        self._insert(index, value)

    def __setitem__(self, index: int, value: V):
        if isinstance(index, slice):
            raise NotImplementedError(f"'{self.__class__.__name__}' does not support set with slices")
        item_position = self._get_item_position(index)
        self.sequences[item_position.seq_index][item_position.item_index] = value

    def __delitem__(self, index: int):
        if isinstance(index, slice):
            raise NotImplementedError(f"'{self.__class__.__name__}' does not support delete with slices")

        item_position = self._get_item_position(index)
        del self.sequences[item_position.seq_index][item_position.item_index]

    # Additional methods to replicate full list functionalities
    def sort(self, /, *, key=None, reverse=False):
        # Sort will sort items inside their sequences
        sortable_sequences = (
            (seq if hasattr(seq, 'sort') else list(seq)) for seq in self.sequences
        )
        for seq in sortable_sequences:
            seq.sort(key=key, reverse=reverse)

    def __imul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        self.sequences *= other
        return self
