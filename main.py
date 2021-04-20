import numpy as np
import copy

class Player:
    def __init__(self, name):
        self.name = name

class RowGame:
    def __init__(self, m=3, k=3, n=3, r=1):
        self.m = m
        self.k = k
        self.n = n
        self.r = r
        self.board = np.zeros([m, k])

    def clone(self):
        return copy.deepcopy(self)

    # def checkDim(self):

    def checkArray(self, grid):
        for row in grid:
            player_streak = 0
            streak_len = 0
            for x in row:
                if x == player_streak:
                    streak_len += 1
                else:
                    streak_len = 0
                    player_streak = x

                if streak_len >= self.n and player_streak != 0:
                    return player_streak
        return player_streak

    def check(self):
        for g in [self.board, self.board.transpose()]:
            winner = self.checkArray(g)
            if winner != 0:
                return winner
        return 0
