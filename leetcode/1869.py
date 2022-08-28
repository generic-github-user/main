class Solution:
    def checkZeroOnes(self, s: str) -> bool:
        # highest number of consecutive 0s/1s yet encountered
        l0 = 0; l1 = 0
        # lengths of current runs of 0s and 1s, respectively
        c0 = 0; c1 = 0
        for i, c in enumerate(s):
            # update both counters for a "0"
            if c == '0':
                if c0 or i == 0: c0 += 1
                elif c1: c0 = 1; c1 = 0
            # update both counters for a "1"
            if c == '1':
                if c1 or i == 0: c1 += 1
                elif c0: c1 = 1; c0 = 0
            # update maximum length counters
            if c0 > l0: l0 = c0
            if c1 > l1: l1 = c1
        return l1 > l0
