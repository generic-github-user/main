class Solution:
    def checkIfExist(self, arr: List[int]) -> bool:
        # the naive approach is O(n^2)

        # hash maps are magical
        targets = set()
        for x in arr:
            if x in targets: return True
            # by treating the current value both as a potential input and
            # output we can avoid needing to backtrack at the cost of a mild
            # increase in space complexity
            targets.update([x * 2, x / 2])
        return False
