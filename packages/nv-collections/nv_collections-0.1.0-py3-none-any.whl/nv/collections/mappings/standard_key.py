from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sized
from typing import TypeVar, Iterable, Tuple, Iterator
from .core import DictWrapper, K, V


EK = TypeVar('EK')


__ALL__ = (
    'StandardKeyWrapperBase',
    'LowerCaseDict',
    'UpperCaseDict',
)


class StandardKeyMapping(DictWrapper):
    def __init__(self, m: Mapping[K, V] | Iterable[Tuple[K, V]] | None = None, ignore_loss=False):
        m = m.items() if isinstance(m, Mapping) else (m or ())
        super().__init__((self.to_standard_key(k), v) for k, v in m)

        if not ignore_loss and isinstance(m, Sized) and len(m) != len(self):
            raise TypeError(f"'to_standard_key' is not a 1:1 method and some items were lost from the original "
                            f"mapping during initialization. If that is the desired behaviour, you should explicitly "
                            f"set 'loss_check=False' at '{self.__class__.__name__ }' __init__ call.")

    @staticmethod
    def to_standard_key(external_key: EK) -> K:
        raise NotImplementedError

    @classmethod
    def detect_clashing_keys(cls, m: Mapping[K, V]):
        conversion = defaultdict(set)
        for k in m.keys():
            conversion[cls.to_standard_key(k)].add(k)
        return {k: v for k, v in conversion.items() if len(v) != 1}

    def clashes_with(self, external_key: K) -> bool:
        return external_key not in self._mapping and self.to_standard_key(external_key) in self

    @property
    def clashing_keys(self):
        return self.to_standard_key(self._mapping)

    @classmethod
    def wrap(cls, m: Mapping[K, V], conformity_check=True):
        if conformity_check and any(cls.to_standard_key(k) != k for k in m.keys()):
            raise KeyError(f"you are trying to wrap a mapping whose keys do not conform to the standard keys. "
                           f"Perhaps you may want to use __init__ to assure conformity, "
                           f"otherwise set explicitly 'conformity_check=False'")
        return super().wrap(m)

    def __getitem__(self, external_key: EK) -> V:
        return self._mapping[self.to_standard_key(external_key)]

    def __setitem__(self, external_key: EK, value: V):
        self._mapping[self.to_standard_key(external_key)] = value

    def __delitem__(self, external_key: EK):
        del self._mapping[self.to_standard_key(external_key)]

    def __iter__(self) -> Iterator[EK]:
        # Although this is technically not needed if no wrapping
        return (self.to_standard_key(k) for k in iter(self._mapping))


class LowerCaseDict(StandardKeyMapping[str, V]):
    @staticmethod
    def to_standard_key(external_key: str) -> str:
        return external_key.lower()


class UpperCaseDict(StandardKeyMapping[str, V]):
    @staticmethod
    def to_standard_key(external_key: str) -> str:
        return external_key.upper()
