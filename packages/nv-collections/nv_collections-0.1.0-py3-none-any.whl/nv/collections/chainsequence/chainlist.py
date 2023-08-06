from typing import Sequence

from . import MutableChainSequence, V
from ..utils import repr_sequence


class ChainList(list[V]):
    """
    ChainList is a 'dumb' proxy to a MutableSequenceChain
    that passes as a list for Django settings test.

    Please notice that it has to be initialized as a ChainSequence to work properly.
    It also exposes their internal sequences with the 'sequences' property
    and has a proper __repr__ implemented.

    Other than that, it re-implements the documented list methods
    and the most relevant __methods__
    as a blind *args, **kwargs call to the proxied ChainSequence equivalent.

    It should behave as a list in most of the scenarios,
    except when sorted (see ChainSequence behaviour for that purpose).
    """

    def __init__(self, *seqs: Sequence[V]):
        # Call on super().__init__ is avoided on purpose here
        self._chain_seq = MutableChainSequence(*seqs)

    @property
    def sequences(self):
        return self._chain_seq.sequences

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.sequences)[1:-1]})"

    def __str__(self):
        return repr_sequence(self._chain_seq)

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        clone = ChainList.__new__(ChainList)
        clone._chain_seq = self._chain_seq.copy()
        return clone

    def __eq__(self, other):
        return self._chain_seq.__eq__(other)

    def __lt__(self, other):
        return self._chain_seq.__lt__(other)

    def __gt__(self, other):
        return self._chain_seq.__gt__(other)

    def __le__(self, other):
        return self._chain_seq.__le__(other)

    def __ge__(self, other):
        return self._chain_seq.__ge__(other)

    # Dumb proxy
    def append(self, *args, **kwargs):
        return self._chain_seq.append(*args, **kwargs)

    def extend(self, *args, **kwargs):
        return self._chain_seq.extend(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self._chain_seq.insert(*args, **kwargs)

    def remove(self, *args, **kwargs):
        return self._chain_seq.remove(*args, **kwargs)

    def pop(self, *args, **kwargs):
        return self._chain_seq.pop(*args, **kwargs)

    def clear(self):
        return self._chain_seq.clear()

    def index(self, *args, **kwargs):
        return self._chain_seq.index(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self._chain_seq.count(*args, **kwargs)

    def sort(self, *args, **kwargs):
        return self._chain_seq.sort(*args, **kwargs)

    def reverse(self):
        return self._chain_seq.reverse()

    def __len__(self):
        return self._chain_seq.__len__()

    def __iter__(self):
        return self._chain_seq.__iter__()

    def __getitem__(self, *args):
        return self._chain_seq.__getitem__(*args)

    def __setitem__(self, *args):
        return self._chain_seq.__setitem__(*args)

    def __delitem__(self, *args):
        return self._chain_seq.__delitem__(*args)

    def __add__(self, *args, **kwargs):
        return self._chain_seq.__add__(*args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self._chain_seq.__mul__(*args, **kwargs)

    def __imul__(self, *args, **kwargs):
        return self._chain_seq.__imul__(*args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        return self._chain_seq.__iadd__(*args, **kwargs)

    def __radd__(self, *args, **kwargs):
        return self._chain_seq.__radd__(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return self._chain_seq.__rmul__(*args, **kwargs)

    def __hash__(self):
        return self._chain_seq.__hash__()
