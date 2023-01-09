from typing import TypeVar, Generic
T = TypeVar('T')


class List(Generic[T]):
    """A simple wrapper class for several built-in Python sequence types
    designed to facilitate method chaining and functional programming patterns.
    In many cases, this class' methods simply pass calls to standard global
    functions on iterators included in Python (e.g., `map` and `filter`). There
    are currently some efficiency concerns, namely in cases where I have
    temporarily avoided headaches by converting iterators directly to lists; I
    plan to refactor these later to improve style and efficiency at the
    potential cost of a slightly more complicated interface (and more involved
    internals)."""

    def __init__(self, items=None):
        """Creates a new list containing the elements from the Python list
        `items` (i.e., wrapping it)"""

        if items is None:
            items = []
        self.items = items

    def for_each(self, f):
        for x in self:
            f(x)

    """Applies `f` to each element in this list, returning a new list"""
    def map(self, f):
        return List(list(map(f, self.items)))

    """Returns a new list containing only the elements in this list for which
    the predicate `p` is true"""
    def filter(self, p):
        return List(list(filter(p, self.items)))

    """Returns a new list containing elements for which the attribute `attr` is
    equal to `value`"""
    def filter_by(self, attr, value):
        return self.filter(lambda x: getattr(x, attr) == value)

    """Removes items equal to any of the arguments, returning a new list"""
    def remove(self, *args):
        return self.filter(lambda x: x not in args)

    """Returns a new list constructed by accessing the `attr` attribute of each
    item in this list"""
    def get(self, attr):
        return self.map(lambda x: getattr(x, attr))

    def set(self, attr, value):
        for x in self.items:
            setattr(x, attr, value)
        return self

    """Returns a new list sorted using the comparison function `f`, which
    should take as input two elements of the input list"""
    def sorted(self, f):
        return List(list(sorted(self.items, key=f)))

    """Returns true if and only if the predicate `p` is true for every element
    in the list"""
    def all(self, p=None):
        if p is None:
            return all(self.items)
        else:
            return all(p(i) for i in self.items)

    """Returns true if and only if the predicate `p` is true for at least one
    element in the list"""
    def any(self, p=None):
        if p is None:
            return any(self.items)
        else:
            return any(p(i) for i in self.items)

    """Returns true if and only if the predicate `p` is false for every element
    in the list, or (equivalently) true for no elements"""
    def none(self, p=None):
        return not self.any(p)

    """Returns an integer representing the length of this list"""
    def len(self):
        return len(self.items)

    """Adds a new element to this list (modifying it in place)"""
    def append(self, x):
        return self.items.append(x)

    def extend(self, x):
        self.items.extend(x)
        return self

    """Combine the elements of the list in order, returning a string; if the
    given delimiter has length m and this list has length n, the resulting
    string will be m*(n-1) characters longer than the concatenation of the
    string representations of all the elements in the list"""
    def join(self, s):
        return s.join(self.map(str).items)

    def partition(self, attr):
        return {value: self.filter(lambda x: getattr(x, attr) == value) for
                value in set(getattr(y, attr) for y in self.items)}

    def length(self):
        return len(self)

    def to_string(self, **kwargs):
        return self.map(lambda x: x.to_string(**kwargs)).join(', ')

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return self.len()

    def __getitem__(self, i):
        return self.items[i]

    def __eq__(self, other):
        return self.items == other.items

    def __repr__(self):
        return repr(self.items)
