import numpy as np
import copy

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class RowGame:
    def __init__(self, m=3, k=3, n=3, r=1):
        self.m = m
        self.k = k
        self.n = n
        self.r = r
        self.board = np.zeros([m, k])
        self.players = []
        self.defaultChar = ' '

    def clone(self):
        return copy.deepcopy(self)

    def cellSym(self, n):
        if n != 0:
            return self.players[int(n)-1].symbol
        else:
            return self.defaultChar

    def print(self, type='normal'):
        if type == 'normal':
            for row in self.board:
                row_string = ' '.join([self.cellSym(col) for col in row])
                print(row_string)
        elif type == 'raw':
            print(self.board)

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
        return 0

    def diagonalize(self, grid):
        x, y = grid.shape
        result = []
        for d in range(-y, x):
            result.append(grid.diagonal(d))
        return result

    def check(self):
        d_ = self.diagonalize
        for g in [self.board, self.board.transpose(), d_(self.board), d_(self.board.transpose())]:
            winner = self.checkArray(g)
            if winner != 0:
                return winner
        return 0

class DecisionTree:
    def __init__(self):
        self.nodes = []


game = RowGame()
game.print()
print(game.check())
