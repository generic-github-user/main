class Solution:
    def destCity(self, paths: List[List[str]]) -> str:
        return list(filter(lambda p: not any(p[-1] == x[0] for x in paths), paths))[0][-1]
