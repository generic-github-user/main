# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        x, y = 0, 0
        dx, dy = 1, 0
        result = [[-1] * n for i in range(m)]
        #while head.next:
        while head:
            result[y][x] = head.val
            if (not 0 <= x + dx < n) or\
                (not 0 <= y + dy < m) or\
                result[y + dy][x + dx] != -1:
                dx, dy = -dy, dx
            x += dx; y += dy
            head = head.next
        return result
