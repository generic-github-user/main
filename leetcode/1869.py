class Solution:
    def checkZeroOnes(self, s: str) -> bool:
        l0 = 0; l1 = 0
        c0 = 0; c1 = 0
        for i, c in enumerate(s):
            if c == '0':
                if c0 or i == 0: c0 += 1
                elif c1: c0 = 1; c1 = 0
            if c == '1':
                if c1 or i == 0: c1 += 1
                elif c0: c1 = 1; c0 = 0
            if c0 > l0: l0 = c0
            if c1 > l1: l1 = c1
        return l1 > l0
