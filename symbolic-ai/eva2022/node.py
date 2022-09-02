# from graph import Graph
# import graph

# An OOP-style interface for working with the graph database: The efficient
# array-based implementation is still used but this wrapper allows for method
# chaining and more literate code. This class is largely functional and tightly
# intertwined with the Graph class (i.e., not encapsulated). Instances of this
# class are not meant to be processed in large numbers - it is intended for
# convenient access to functions on graphs.
class Node:
    def __init__(self, nid, graph, rep):
        assert isinstance(nid, int)
        # assert(isinstance(graph, Graph))

        self.id = nid
        self.graph = graph
        self.rep = rep
        self.references = []

    def referrers(self, update=False):
        if not isinstance(update, bool):
            raise TypeError

        # Delayed import to avoid circular import issue - is there a cleaner
        # way to do this?
        from graph import Graph
        return Graph([self.graph.get(x, update) for x in self.graph.references[self.id]])

    def adjacent(self, value=None, directional=False, return_ids=True):
        assert isinstance(directional, bool)
        assert isinstance(return_ids, bool)

        adjacent = []
        # for i, m in self.referrers().hashmap.items():
        for m in self.referrers():
            for ref in m.members:
                if (ref != self.id) and (value is None or m.value == value) and ((not directional) or m.members.index(self.id) == 0):
                    adjacent.append(ref)
        if return_ids:
            return adjacent
        else:
            from graph import Graph
            return Graph([self.graph[x] for x in adjacent])

    def __getattr__(self, attr):
        # return getattr(self.graph.nodes[self.id], attr)
        return getattr(self.rep, attr)

    def __str__(self):
        return f'[{self.id}: {str(self.value)[:30]} ~ [{"; ".join([str(self.graph[i].value)[:30] if i else "[null]" for i in self.members])}]]'
