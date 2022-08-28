class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for i in range(len(matrix)):
            if (i == len(matrix)-1) or (matrix[i][0] <= target < matrix[i+1][0]):
                for j in range(len(matrix[i])):
                    if matrix[i][j] == target: return True
        return False
