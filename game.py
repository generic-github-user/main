import numpy as np
import random
import copy


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class RowGame:
    def __init__(self, dims=None, m=3, k=3, n=3, r=1, f=1, players=None):
        """Create a new game instance"""

        self.m = m
        self.k = k

        if dims is None:
            self.dimensions = [m, k]
        else:
            self.dimensions = dims
        self.dims = self.dimensions

        self.n = n
        self.r = r
        self.board = np.zeros(self.dims)
        self.defaultChar = ' '
        self.currentTurn = f

        if players is None:
            self.players = []
            self.players.append(Player('Player 1', 'X'))
            self.players.append(Player('Computer', 'C'))
        else:
            self.players = players

    def clone(self):
        """Make a deep copy of this game object and all nested objects"""
        return copy.deepcopy(self)

    def nextTurn(self):
        """Switch to the next player"""
        self.currentTurn += 1
        # If maximum turn number is exceeded, go back to first player
        if self.currentTurn > len(self.players):
            self.currentTurn = 1

        return self

    def between(self, n, b, a=0):
        """Shorthand function for checking if a given value is between two other values"""
        return a <= n <= b

    def legal(self, pos=None, x=0, y=0):
        """Check if a given move is allowed"""
        be = self.between
        if pos is None:
            pos = [x, y, 0]
        x, y, z = pos
        x_, y_, z_ = self.board.shape
        # For a space to be a legal move:
        # x must be in the range [0, m)
        # y must be in the range [0, k)
        # board_{x,y} must be 0
        print(pos)
        pos = tuple(pos)
        conditions = [be(x,x_), be(y,y_), self.board[pos] == 0]
        print(conditions)
        return all(conditions)

    def move(self, pos=None, x=0, y=0):
        """Place a player marker at the provided location and go to the next player"""
        if pos is None:
            pos = [x, y, 0]
        pos = tuple(pos)

        if self.legal(pos):
            self.board[pos] = self.currentTurn
            # Go to next player
            self.nextTurn()
        else:
            print('Not a legal move')
        # return self
        return self.check()

    def center(self):
        """Take the current player's turn at the center of the board (or nearest available)"""
        x, y = np.round(np.array(self.board.shape) / 2)
        x, y = int(x)-1, int(y)-1
        self.move(x, y)

    def getFree(self):
        """Get a list of coordinates (2D array indices) where the board state is 0 (no move played yet)"""
        empty = np.argwhere(self.board == 0)
        if len(empty) > 0:
            return empty
        else:
            print('No free spaces')
            return empty

    def playRandom(self):
        """Play a move in a randomly selected available space"""
        free_spaces = self.getFree()
        if len(free_spaces) > 0:
            return self.move(*random.choice(free_spaces))
        else:
            return 0

    def cellSym(self, n):
        """Get the symbol representing a cell in the game board"""
        if n != 0:
            return self.players[int(n)-1].symbol
        else:
            return self.defaultChar

    def print(self, type='normal', grid=True):
        """Display the game board in the console"""
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
        """Check a list of strides for winning rows"""
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
        """Create a list of diagonal strides through the game board"""
        x, y = grid.shape
        result = []
        # Loop through diagonal offsets; a [3, 5] array will have offsets from -5 to 3
        for d in range(-y+1, x):
            result.append(grid.diagonal(d))
        return result

    def check(self):
        """Check the game state for any winners"""
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
