from __future__ import annotations
import lark

from node import Node


class Token:
    def __init__(self, source: lark.Token = None, parent: Node = None,
                 type_: str = None, value: str = None, line: int = None,
                 column: int = None):
        self.parent = parent
        self.source = source
        self.type = type_
        self.value = value

        self.vtype = None

        self.line = line
        self.column = column
        if self.source is not None:
            for attr in 'type value line column'.split():
                setattr(self, attr, getattr(self.source, attr))
                self.length = len(self.source)
        self.data_attrs = set()

    def text(self) -> str:
        return self.value

    def __str__(self) -> str:
        return f'Token <{self.type}, {self.line}:{self.column}> {self.value}'

    def resolve_names(self, namespace):
        return resolve_names(self, namespace)

    def infer_types(self):
        match self.type:
            case 'INT':
                self.vtype = 'int'
            case 'FLOAT':
                self.vtype = 'float'

    def emit_code(self) -> str:
        return self.value

    def map(self, f) -> Token:
        return f(self)

    def with_attr(self, k, v) -> Token:
        return self

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.value == other
        return self.value == other.value

    __repr__ = __str__
