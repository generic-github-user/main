class Solution:
    def restoreString(self, s: str, indices: List[int]) -> str:
        x = [''] * len(s)
        for c, i in zip(s, indices): x[i] = c
        return ''.join(x)
