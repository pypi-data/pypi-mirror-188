from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from typing import TypeVar, Iterable, Tuple, Iterator, Any, Union

from ..utils import SimpleParser


__ALL__ = (
    'FrozenDictWrapper',
    'DictWrapper',
)


K = TypeVar('K')
V = TypeVar('V')
EK = TypeVar('EK')
T = TypeVar('T', bound=Union[Mapping, MutableMapping])


class RecursiveDictWrapper(SimpleParser):
    def __init__(self, dict_wrapper):
        print('dict_wrapper: ', dict_wrapper)
        self.dict_wrapper = dict_wrapper

    def parse_mapping(self, obj: Mapping, parser, **kwargs):
        print('rdw parse_mapping: ', obj)
        return self.dict_wrapper(super().parse_mapping(obj, parser, **kwargs))

    def parse_mut_mapping(self, obj: MutableMapping, parser, **kwargs):
        print('rdw parse_mut_mapping: ', obj)
        return self.dict_wrapper(super().parse_mut_mapping(obj, parser, **kwargs))


class DictWrapperBase(Mapping[K, V]):
    def __init__(self, m: T | Iterable[Tuple[K, V]] | None = None, **dict_kwargs):

        if isinstance(m, DictWrapperBase):
            mapping = m.wrapped
        elif isinstance(m, Mapping):
            mapping = m
        else:
            mapping = dict(m or (), **dict_kwargs)

        self._mapping = mapping

    @property
    def wrapped(self) -> T:
        return self._mapping

    @classmethod
    def wrap(cls, m: Mapping[K, V]):
        print('wrap: ', m)
        return m if isinstance(m, cls) else cls(m)

    @classmethod
    def convert(cls, obj: Any):
        return RecursiveDictWrapper(cls.wrap)(obj)

    def __getitem__(self, key: K) -> V:
        return self._mapping[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._mapping!r})"


class FrozenDictWrapper(DictWrapperBase):
    pass


class DictWrapper(DictWrapperBase):
    def __setitem__(self, key: K, value: V):
        self._mapping[key] = value

    def __delitem__(self, key: K):
        del self._mapping[key]
