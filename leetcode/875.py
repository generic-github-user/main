class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        found = False
        # k = 1
        low, high = 1, max(piles)
        while low != high:
            k = low + (high - low) // 2
            valid = sum(ceil(x / k) for x in piles) <= h
            if valid:
                high = k
            else:
                low = k+1
            # k += 1
        return low
