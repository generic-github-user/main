from graph import Graph

class CompleteGraph(Graph):
    def __init__(self, n, weighted=False, weights=1):
        super().__init__()
        self.add_nodes(list(range(1,n+1)))
        metadata = [{}]
        for i in range(n):
            for j in range(n):
                if i != j:
#                     print(i, j)
                    ni = self.nodes[i]
                    nj = self.nodes[j]

                    if weighted:
                        if type(weights) in [int, float]:
                            metadata[0]['weight'] = weights
                        elif type(weights) in [Randomizer]:
                            metadata[0]['weight'] = weights.sample()
                    self.add_node([f'E{ni.value+nj.value}', ni, nj], duplicate=True, metadata=metadata)
