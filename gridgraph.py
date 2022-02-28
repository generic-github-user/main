from graph import Graph

class GridGraph(Graph):
    def __init__(self, dims):
        super().__init__([], False, False)
        last = Graph(['x'], True, True)
        for d in dims:
            L = Graph(['x'], True, True)
#             print(list(map(str,L.nodes)), list(map(str,last.nodes)))
            for n in range(d-1):
                L = L.join(last, str(n))
            last.nodes = [q for q in L.nodes]
        self.nodes = last.nodes
