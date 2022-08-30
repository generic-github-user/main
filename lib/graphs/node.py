class Node:
    def init(self, value, grouped=None, graph=None, metadata=None, **kwargs):
        self.value = value
        if grouped is None:
            grouped = []
#         self.grouped = [g if type(g) is Node else Node(g, graph=graph) for g in grouped]
        self.graph = graph
        if metadata:
            M = metadata[1:]
        else:
            M = None
        self.grouped = [g if type(g) is Node else self.graph.add_node(g, metadata=M, **kwargs) for g in grouped]
        self.unique = True#not (type(self.value) is int)
#         print(self.graph, self.value)
#         if self.graph:
        if self.graph is not None:
            self.graph.add_node(self, duplicate=True)#, **kwargs)

        if metadata:
            for k, v in metadata[0].items():
                setattr(self, k, v)

    def degree(self):
        self.deg = None
        if self.graph:
#             self.deg = sum(int(self in x.grouped) for x in self.graph.nodes)
#             self.deg = sum(map(bool, self.graph.find(self.value)))
            self.deg = sum(self in x.grouped for x in self.graph.nodes)
#             print(self.deg)
        return self.deg

    def adjacent(self, exclude=None):
        grouping_nodes = [x for x in self.graph.nodes if (self in x.grouped)]
        return Graph(nodes=[n for gn in grouping_nodes for n in gn.grouped if (n is not self and (not exclude or n not in exclude.nodes))])

    def extend(self, z, w, return_new=False, return_node=False, **kwargs):
        n = self.graph.add_node([w, self, z], return_node=return_node, **kwargs)
        if return_new:
            return n
        else:
            return self

    def __str__(self):
        return str(self.value)
