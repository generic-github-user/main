class Solution:
    def maximumDifference(self, nums: List[int]) -> int:
        # result = max(nums[i+1]-nums[i] for i in range(len(nums) - 1))
        ni = nums[0]
        m = 0
        for nj in nums[1:]:
            d = nj - ni
            if nj < ni: ni = nj
            if d > m: m = d
        return -1 if m <= 0 else m
