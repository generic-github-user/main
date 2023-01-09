from __future__ import annotations
from typing import TypeVar, Generic
T = TypeVar('T')


class Option(Generic[T]):
    def __init__(self, value: T, some: bool):
        self.value = value
        self.is_some = some

    @staticmethod
    def some(v):
        return Option(v, True)

    @staticmethod
    def none():
        return Option(None, False)

    def then(self, f) -> Option[T]:
        if not self.is_some:
            return self
        return Option.some(f(self.unwrap()))

    def else_(self, f, *args) -> Option[T]:
        if self.is_some:
            return self
        # TODO
        return Option.some(f(*args))

    def unwrap(self) -> T:
        if self.is_some:
            return self.value
        else:
            raise OptionError


class OptionError(Exception):
    pass
