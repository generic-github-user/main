class Solution:
    def checkIfExist(self, arr: List[int]) -> bool:
        # the naive approach is O(n^2)
        targets = set()
        for x in arr:
            if x in targets: return True
            targets.update([x * 2, x / 2])
        return False
