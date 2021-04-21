import numpy as np
import copy
import random
import json

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
        # return self
        return self.check()

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

class Node:
    def __init__(self, state=None, depth=1):
        self.parent_nodes = []
        self.child_nodes = []
        self.score = 0
        self.state = state
        self.max_depth = 9
        self.depth = depth
        self.turn = 2
        self.terminate = False
        self.outcome = 0

    def generate_branches(self, mutator=None, num=3, recursive=True):
        for n in range(num):
            if self.depth <= self.max_depth:
                branch = Node(state=self.state.clone(), depth=self.depth+1)
                # if branch.state.currentTurn == self.turn:
                move_result = branch.state.playRandom()
                # print(move_result)
                if move_result != 0:
                    branch.terminate = True
                    branch.outcome = int(move_result)

                branch.parent_nodes.append(self)
                if recursive and not branch.terminate:
                    branch.generate_branches()
                self.child_nodes.append(branch)

    def term_nodes(self):
        results = []
        for c in self.child_nodes:
            if c.terminate:
                results.append(c)
            else:
                results.extend(c.term_nodes())
        return results

    def count_subnodes(self):
        total = len(self.child_nodes)
        for n in self.child_nodes:
            total += n.count_subnodes()
        return total

    def backpropagate(self, q=0, direction='down'):
        if direction == 'up':
            if self.terminate:
                if self.outcome == 2:
                    self.score += 1
                elif self.outcome == 1:
                    self.score -= 1
            else:
                self.score += (q / len(self.child_nodes))
                # self.score += q / self.count_subnodes()

            for p in self.parent_nodes:
                p.backpropagate(q=self.score)
        elif direction == 'down':
            if self.terminate:
                if self.outcome == 2:
                    self.score += 1
                elif self.outcome == 1:
                    self.score -= 1
            else:
                num_children = len(self.child_nodes)
                for c in self.child_nodes:
                    self.score += c.backpropagate() / num_children

            return self.score
        else:
            raise ValueError('Invalid value propagation direction')

    def __str__(self):
        # return json.dumps(self.__dict__, indent=2)
        node_dict = {}
        for a in ['score', 'depth', 'max_depth']:
            node_dict[a] = getattr(self, a)
        node_string = json.dumps(node_dict, indent=2)
        return node_string

    def subnodes(self):
        node_list = []
        for n in self.child_nodes:
            node_list.append(n)
            node_list.extend(n.subnodes())
        return node_list

class DecisionTree:
    def __init__(self):
        # self.nodes = []
        self.initial_state = RowGame()
        self.root = Node(state=self.initial_state, depth=1)

    def simulate(self):
        self.root.generate_branches()

    def backpropagate(self):
        # for u in self.root.term_nodes():
        #     u.backpropagate()
        self.root.backpropagate()

    def print_tree(self, r=None, l=0):
        if r is None:
            r = self.root

        print((' '*l*2) + '({}) '.format(l) + str(r.score) + ' / ' + str(len(r.child_nodes)) + ' / ' + str(len(r.parent_nodes)))
        for n in r.child_nodes:
            self.print_tree(r=n, l=l+1)

    def all_nodes(self):
        return self.root.subnodes()

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
print(game.board)
print(game.check())
print(game.diagonalize(game.board))
# print(game.diagonalize(game.board.transpose()))
# print(game.diagonalize(np.transpose(game.board)))
print(game.diagonalize(np.fliplr(game.board)))

tree = DecisionTree()

tree.root.state.players.append(Player('P1', 'X'))
tree.root.state.players.append(Player('Computer', 'O'))

tree.simulate()
# print(tree.root.child_nodes[0].child_nodes[0].child_nodes[0].child_nodes[0])
g = tree.root
for i in range(tree.root.max_depth):
    try:
        # print(g.state.board)
        g.state.print()
        g = g.child_nodes[0]
    except:
        pass

tree.backpropagate()
# tree.print_tree()

print(tree.root.count_subnodes())
print(len(tree.root.term_nodes()))
print(tree.root)
