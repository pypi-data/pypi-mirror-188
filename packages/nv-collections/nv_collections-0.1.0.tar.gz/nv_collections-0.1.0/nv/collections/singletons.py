# Singletons that are intended to work where None is a possible value


__ALL__ = (
    'Singleton',
    'Missing',
    'Empty',
    'UnSet',
    'Raise',
    'MISSING',
    'EMPTY',
    'RAISE',
    'UNSET',
)


class Singleton:
    _singleton = None
    _as_bool = None

    def __init_subclass__(cls, as_bool=None, **kwargs):
        super().__init_subclass__()
        cls._as_bool = as_bool
        cls._singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls, *args, **kwargs)
        return cls._singleton

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return f"<{self.__class__.__name__}>"

    def __bool__(self):
        if self._as_bool is None:
            raise TypeError(f"improper boolean conversion for {self.__class__.__name__}. "
                            f"Perhaps you may want to set 'cast_bool' type property of your Singleton.")
        return self._as_bool

    def __eq__(self, other):
        return self is other

    def __match_args__(self):
        return ()


# Semantic singletons for places where None or bool have other meanings
class Missing(Singleton, as_bool=False):
    pass


class Empty(Singleton, as_bool=False):
    pass


class UnSet(Singleton, as_bool=False):
    pass


class Raise(Singleton):
    pass


MISSING = Missing()
EMPTY = Empty()
UNSET = UnSet()
RAISE = Raise()
