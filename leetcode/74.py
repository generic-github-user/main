class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # loop over rows in matrix
        for i in range(len(matrix)):
            # tests if the current matrix row *could* contain `target`
            if (i == len(matrix)-1) or (matrix[i][0] <= target < matrix[i+1][0]):
                for j in range(len(matrix[i])):
                    # check for match etc
                    if matrix[i][j] == target: return True
        return False
