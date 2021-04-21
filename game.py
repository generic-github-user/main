import numpy as np
import random
import copy


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class RowGame:
    def __init__(self, m=3, k=3, n=3, r=1, f=1):
        self.m = m
        self.k = k
        self.n = n
        self.r = r
        self.board = np.zeros([m, k])
        self.players = []
        self.defaultChar = ' '
        self.currentTurn = f

    def clone(self):
        return copy.deepcopy(self)

    def nextTurn(self):
        self.currentTurn += 1
        # If maximum turn number is exceeded, go back to first player
        if self.currentTurn > len(self.players):
            self.currentTurn = 1

        return self

    def between(self, n, b, a=0):
        return a <= n <= b

    def legal(self, x, y):
        be = self.between
        x_, y_ = self.board.shape
        # For a space to be a legal move:
        # x must be in the range [0, m)
        # y must be in the range [0, k)
        # board_{x,y} must be 0
        conditions = [be(x,x_), be(y,y_), self.board[x, y] == 0]
        return all(conditions)

    def move(self, x, y):
        if self.legal(x, y):
            self.board[x, y] = self.currentTurn
            # Go to next player
            self.nextTurn()
        else:
            print('Not a legal move')
        # return self
        return self.check()

    def center(self):
        x, y = np.round(np.array(self.board.shape) / 2)
        x, y = int(x)-1, int(y)-1
        self.move(x, y)

    def getFree(self):
        # Get a list of coordinates (2D array indices) where the board state is 0 (no move played yet)
        empty = np.argwhere(self.board == 0)
        if len(empty) > 0:
            return empty
        else:
            print('No free spaces')
            return empty

    def playRandom(self):
        free_spaces = self.getFree()
        if len(free_spaces) > 0:
            return self.move(*random.choice(free_spaces))
        else:
            return 0

    def cellSym(self, n):
        if n != 0:
            return self.players[int(n)-1].symbol
        else:
            return self.defaultChar

    def print(self, type='normal', grid=True):
        # print('players', self.players)
        if type == 'normal':
            # Loop through rows
            for i, row in enumerate(self.board):
                if grid:
                    divider = '|'
                else:
                    divider = self.defaultChar
                # Generate and print string representing row of game board
                row_string = divider.join([self.cellSym(col) for col in row])
                print(row_string)

                if grid and i < len(self.board) - 1:
                    print('-'.join(['-'] * len(row)))
        elif type == 'raw':
            # Print plain NumPy array
            print(self.board)
        print()

    # def checkDim(self):

    def checkArray(self, grid):
        for row in grid:
            # Track the player who made the current move(s)
            player_streak = 0
            streak_len = 0
            # print(row)
            # Loop through each mark in row (after transformation; so the "row" might actually be a column or diagonal)
            for x in row:
                if x == player_streak:
                    streak_len += 1
                else:
                    streak_len = 1
                    player_streak = x

                # print(streak_len)
                # print(2. == 2)
                if streak_len >= self.n and player_streak != 0:
                    return player_streak
        # If no player won in any of the checked rows, return 0
        return 0

    def diagonalize(self, grid):
        x, y = grid.shape
        result = []
        # Loop through diagonal offsets; a [3, 5] array will have offsets from -5 to 3
        for d in range(-y+1, x):
            result.append(grid.diagonal(d))
        return result

    def check(self):
        # tr = np.transpose
        tr = np.fliplr
        d_ = self.diagonalize
        # Loop through rows, columns, and both diagonals
        for g in [self.board, np.transpose(self.board), d_(self.board), d_(tr(self.board))]:
            winner = self.checkArray(g)
            # print(winner)
            # Return the winner if it is a player
            if winner != 0:
                return winner
        return 0

    def __sub__(self, b):
        return self.board - b.board
