import numpy as np
import copy
import random
import json

from game import *

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
