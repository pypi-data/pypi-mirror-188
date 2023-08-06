from __future__ import annotations

from typing import Any, MutableMapping, Mapping

from .core import DictWrapper, V
from ..utils import repr_dict


__ALL__ = (
    'ObjectDict',
    'ObjectDictWrapper'
    )


class ObjectDictBase:
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


class ObjectDict(ObjectDictBase, dict[str, V]):
    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return f"{self.__class__.__name__}({repr_dict(self)})"


class ObjectDictWrapper(ObjectDictBase, DictWrapper[str, V]):
    _mapping: Mapping[str, Any] | MutableMapping[str, Any] | None = None

    def __init__(self, obj: Any):
        super().__init__(obj if isinstance(obj, Mapping) else obj.__dict__)
        self._obj = obj

    @property
    def wrapped_obj(self):
        return self._obj

    def __getattr__(self, name):
        if self._mapping is None:
            raise AttributeError(name)

        return super().__getattr__(name)

    def __setattr__(self, name, attr):
        # Handles pre-wiring settings
        if self._mapping is not None:
            self._mapping[name] = attr

        super().__setattr__(name, attr)

    def __delattr__(self, name):
        # Handles pre-wiring settings
        if self._mapping is not None:
            del self._mapping[name]

        super().__delattr__(name)
