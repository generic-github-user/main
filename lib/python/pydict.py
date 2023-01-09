from __future__ import annotations
from result import Result
from pylist import List
from typing import TypeVar, Generic
T = TypeVar('T')
V = TypeVar('V')


class Dict(Generic[T, V]):
    """A simple `dict` wrapper class that provides method chaining and other
    QOL features; typed generically over two parameters and integrates the
    `Result` type for lookups."""

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data: dict[T, V] = data

    def contains(self, key: T) -> bool:
        # print('canary')
        return key in self.data

    def keys(self) -> List[T]:
        return List(self.data.keys())

    def values(self) -> List[V]:
        return List(self.data.values())

    def items(self) -> List[tuple[T, V]]:
        return List(self.data.items())

    def __getitem__(self, key: T) -> Result[V]:
        if self.contains(key):
            return Result.Ok(self.data[key])
        return Result.Err(None)

    def __setitem__(self, key: T, value: V) -> Dict[T, V]:
        self.data[key] = value
        return self
