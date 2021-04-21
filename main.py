import numpy as np
import copy
import random
import json

from game import *
from node import *

class DecisionTree:
    def __init__(self, start):
        # self.nodes = []
        self.initial_state = start
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

tree = DecisionTree(RowGame(m=4, k=4, f=2))

tree.root.state.players.append(Player('P1', 'X'))
tree.root.state.players.append(Player('Computer', 'O'))
tree.root.state.center()

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

random.choice(tree.root.term_nodes()).state.print()

print(len(tree.all_nodes()))
# print(tree.match(game))
game.print()
tree.match(game).state.print()
