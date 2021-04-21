import numpy as np

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

    def search(self):
        pass

    def match(self, state):
        node_list = self.all_nodes()
        return min(node_list, key=lambda w: np.sum(np.abs(w.state - state)))

    def best(self):
        pass
