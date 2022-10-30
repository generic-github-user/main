class Solution:
    def makeGood(self, s: str) -> str:
        good = False
        c = list(s)
        while not good:
            indices = [i for i in range(len(c)-1) if
                       c[i] != c[i+1] and c[i].lower() == c[i+1].lower()]
            #for i in indices:
            print(indices)
            if indices:
                i = indices[0]
                c[i:i+2] = [None] * 2
            c = list(filter(None, c))
            good = not indices
        return ''.join(c)
