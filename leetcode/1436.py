class Solution:
    def destCity(self, paths: List[List[str]]) -> str:
        # find the city that does not occur as a source (first item in pair) in
        # any of the edges in the graph representation
        return list(filter(lambda p: not any(p[-1] == x[0] for x in paths), paths))[0][-1]
