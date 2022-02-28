class RandomGraph(Graph):
    def __init__(self, n, m, weighted=False, weight_bounds=[0, 1]):
        super().__init__()
        self.add_nodes(list(range(1,n+1)))
        metadata = [{}]
        for im in range(m):
            if weighted:
                metadata[0]['weight'] = random.uniform(*weight_bounds)
            self.add_node([n+im]+random.sample(self.nodes[:n], k=2), metadata=metadata)
