class List:
    """Creates a new list containing the elements from the Python list `items`
    (i.e., wrapping it)"""
    def __init__(self, items=None):
        if items is None:
            items = []
        self.items = items

    """Applies `f` to each element in this list, returning a new list"""
    def map(self, f):
        return List(map(f, self.items))

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

    """Returns a new list sorted using the comparison function `f`, which
    should take as input two elements of the input list"""
    def sorted(self, f):
        return List(list(sorted(self.items, key=f)))

    """Returns true if and only if the predicate `p` is true for every element
    in the list"""
    def all(self, p):
        return all(p(i) for i in self.items)

    """Returns true if and only if the predicate `p` is true for at least one
    element in the list"""
    def any(self, p):
        return any(p(i) for i in self.items)

    """Returns true if and only if the predicate `p` is false for every element
    in the list, or (equivalently) true for no elements"""
    def none(self, p):
        return not self.any(p)

    """Returns an integer representing the length of this list"""
    def len(self):
        return len(self.items)

    """Adds a new element to this list (modifying it in place)"""
    def append(self, x):
        return self.items.append(x)

    """Combine the elements of the list in order, returning a string; if the
    given delimiter has length m and this list has length n, the resulting
    string will be m*(n-1) characters longer than the concatenation of the
    string representations of all the elements in the list"""
    def join(self, s):
        return s.join(self.items)

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return self.len()

    def __getitem__(self, i):
        return self.items[i]
