class Solution:
    def areOccurrencesEqual(self, s: str) -> bool:
        return len(set(s.count(c) for c in set(s))) == 1
