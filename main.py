import numpy as np
import copy
import random

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
        return be(x,x_) and be(y,y_) and self.board[x, y] == 0

    def move(self, x, y):
        if self.legal(x, y):
            self.board[x, y] = self.currentTurn
            # Go to next player
            self.nextTurn()
        else:
            print('Not a legal move')

    def getFree(self):
        # Get a list of coordinates (2D array indices) where the board state is 0 (no move played yet)
        empty = np.argwhere(self.board == 0)
        if len(empty) > 0:
            return empty
        else:
            print('No free spaces')

    def playRandom(self):
        free_spaces = self.getFree()
        self.move(*random.choice(free_spaces))

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
            # Return the winner if it is a player
            if winner != 0:
                return winner
        return 0

class Node:
    def __init__(self, state=None, depth=1):
        self.parent_nodes = []
        self.child_nodes = []
        self.score = 0
        self.state = state
        self.max_depth = 6
        self.depth = depth
        self.turn = 2

    def generate_branches(self, mutator=None, num=4, recursive=True):
        for n in range(num):
            if self.depth <= self.max_depth:
                branch = Node(state=self.state.clone(), depth=self.depth+1)
                # if branch.state.currentTurn == self.turn:
                branch.state.playRandom()
                branch.parent_nodes.append(self)
                if recursive:
                    branch.generate_branches()
                self.child_nodes.append(branch)

class DecisionTree:
    def __init__(self):
        self.nodes = []


game = RowGame()
# game.board[0,0] = 2
# game.board[1,1] = 2
# game.board[2,2] = 1
# game.board[1,2] = 1
game.players.append(Player('P1', 'X'))
game.players.append(Player('Computer', 'O'))
for i in range(9):
    game.playRandom()
game.print()
print(game.check())
