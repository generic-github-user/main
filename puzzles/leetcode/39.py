class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        groups = {(x,): x for x in candidates}
        while True:
            f = False
            for k, v in list(groups.items()):
                for c in candidates:
                    #G = k + (c,)
                    G = tuple(sorted(list(k) + [c]))
                    gsum = v + c
                    if G not in groups and gsum <= target:
                        groups[G] = gsum
                        f = True
            if not f: break
        return [y for y, z in groups.items() if z == target]
