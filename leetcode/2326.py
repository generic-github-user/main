# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        # current position
        x, y = 0, 0
        # direction of motion
        dx, dy = 1, 0
        result = [[-1] * n for i in range(m)]
        #while head.next:
        while head:
            # update matrix at current position
            result[y][x] = head.val

            # turn by 90 degrees if the next step would collide with the matrix
            # boundary or a previously visited position
            if (not 0 <= x + dx < n) or\
                (not 0 <= y + dy < m) or\
                result[y + dy][x + dx] != -1:
                dx, dy = -dy, dx

            # move to next pos and update current LL node
            x += dx; y += dy
            head = head.next
        return result
