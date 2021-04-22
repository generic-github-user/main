import numpy as np
import copy
import random
import json

from game import *
from node import *
from tree import *

z = 4
game = RowGame(m=z, k=z, n=z, f=2)
game.move(1, 1)
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

tree = DecisionTree(RowGame(m=z, k=z, n=z, f=2))

tree.root.state.players.append(Player('P1', 'X'))
tree.root.state.players.append(Player('Computer', 'C'))
# tree.root.state.center()

tree.simulate()
tree.backpropagate()
# print(tree.root.children[0].children[0].children[0].children[0])
g = tree.root
for i in range(tree.root.max_depth):
    try:
        # print(g.state.board)
        g.state.print()
        print(g.score)
        # print([v.score for v in g.children])
        # print(type(g))
        # g = g.children[0]

        g = g.best()
        # g = g.max()
    except:
        pass

# tree.print_tree()

print(tree.root.count_subnodes())
print(len(tree.root.term_nodes()))
print(tree.root)

# random.choice(tree.root.term_nodes()).state.print()

print(len(tree.all_nodes()))
# print(tree.match(game))
# game.print()
# tree.match(game).state.print()


game3D = RowGame(dims=[5, 5, 5], n=4)
game3D.randomGame()
print(game3D.board)
game3D.print()

ndim = 3
game_ndim = RowGame(dims=[7]*ndim, n=4)
game_ndim.randomGame()
print(game_ndim.board)
game_ndim.print()
