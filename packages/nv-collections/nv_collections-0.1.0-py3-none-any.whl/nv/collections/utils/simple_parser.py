from collections.abc import Sequence, MutableSequence, MutableMapping, MutableSet, Set
from typing import Mapping, Any

from ..types import BASIC_ELEMENTS, BASIC_SEQUENCES


__ALL__ = (
     "SimpleParser"
)


class SimpleParser:
    def parse_default(self, obj: Any, parser, **kwargs):
        print('parse_default: ', obj)
        return obj

    def parse_element(self, obj: Any, parser, **kwargs):
        print('parse_element: ', obj)
        return obj

    def parse_mut_mapping(self, obj: MutableMapping, parser, **kwargs):
        print('parse_mut_mapping: ', obj)
        for k, v in obj.items():
            obj[k] = parser(v, parser, **kwargs)
        return obj

    def parse_mapping(self, obj: Mapping, parser, **kwargs):
        print('parse_mapping: ', obj)
        return {k: parser(v, parser, **kwargs) for k, v in obj.items()}

    def parse_mut_sequence(self, obj: MutableSequence, parser, **kwargs):
        print('parse_mut_sequence: ', obj)
        for i, v in enumerate(obj):
            obj[i] = parser(v, parser, **kwargs)
        return obj

    def parse_sequence(self, obj: MutableSequence, parser, **kwargs):
        print('parse_sequence: ', obj)
        return tuple(parser(v, parser, **kwargs) for v in obj)

    def parse_mut_set(self, obj: MutableSet, parser, **kwargs):
        print('parse_mut_set: ', obj)
        return obj

    def parse_set(self, obj: MutableSet, parser, **kwargs):
        print('parse_set: ', obj)
        return obj

    _PARSERS = (
        (BASIC_SEQUENCES, parse_element),
        (MutableSequence, parse_mut_sequence),
        (Sequence, parse_sequence),
        (MutableSet, parse_mut_set),
        (Set, parse_set),
        (MutableMapping, parse_mut_mapping),
        (Mapping, parse_mapping),
        (BASIC_ELEMENTS, parse_element),
        (object, parse_default),
    )

    def _select_parser(self, obj: Any):
        selected_parser = next(
            (_parser for _type, _parser in self._PARSERS if isinstance(obj, _type)),
            self.parse_default
        )
        return getattr(self, selected_parser.__name__)

    def _parse(self, obj: Any, parser, **kwargs):
        selected_parser = self._select_parser(obj)
        print('selected_parser: ', selected_parser)
        return selected_parser(obj, parser, **kwargs)

    def parse(self, obj: Any, **kwargs):
        return self._parse(obj, self._parse, **kwargs)

    def __call__(self, obj: Any, **kwargs):
        return self.parse(obj, **kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}()"
