class Solution:
    def restoreString(self, s: str, indices: List[int]) -> str:
        # this can probably be refactored
        x = [''] * len(s)
        for c, i in zip(s, indices): x[i] = c
        return ''.join(x)
