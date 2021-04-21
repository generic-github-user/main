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
        self.currentTurn = 1

    def clone(self):
        return copy.deepcopy(self)

    def nextTurn(self):
        self.currentTurn += 1
        if self.currentTurn > len(self.players):
            self.currentTurn = 1

        return self
    def cellSym(self, n):
        if n != 0:
            return self.players[int(n)-1].symbol
        else:
            return self.defaultChar

    def print(self, type='normal'):
        if type == 'normal':
            # Loop through rows
            for row in self.board:
                # Generate and print string representing row of game board
                row_string = ' '.join([self.cellSym(col) for col in row])
                print(row_string)
        elif type == 'raw':
            # Print plain NumPy array
            print(self.board)

    # def checkDim(self):

    def checkArray(self, grid):
        for row in grid:
            # Track the player who made the current move(s)
            player_streak = 0
            streak_len = 0
            # Loop through each mark in row (after transformation; so the "row" might actually be a column or diagonal)
            for x in row:
                if x == player_streak:
                    streak_len += 1
                else:
                    streak_len = 0
                    player_streak = x

                if streak_len >= self.n and player_streak != 0:
                    return player_streak
        # If no player won in any of the checked rows, return 0
        return 0

    def diagonalize(self, grid):
        x, y = grid.shape
        result = []
        # Loop through diagonal offsets; a [3, 5] array will have offsets from -5 to 3
        for d in range(-y, x):
            result.append(grid.diagonal(d))
        return result

    def check(self):
        d_ = self.diagonalize
        # Loop through rows, columns, and both diagonals
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
