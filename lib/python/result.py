from typing import TypeVar, Generic
T = TypeVar('T')


class Result(Generic[T]):
    def __init__(self, value: T, ok: bool):
        self.value = value
        self.ok = ok

    @staticmethod
    def Ok(v):
        return Result(v, True)

    @staticmethod
    def Err(e):
        return Result(e, False)

    def unwrap(self) -> T:
        if self.ok:
            return self.value
        else:
            raise ResultError


class ResultError(Exception):
    pass
