import json

class Node:
    def __init__(self, state=None, depth=1):
        self.parent_nodes = []
        self.child_nodes = []
        self.score = 0
        self.state = state
        self.max_depth = 8
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

    def backpropagate(self, q=0, direction='down', aggregator='minimax'):
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
                if aggregator == 'minimax':
                    # current_turn = None
                    cs = self.child_nodes
                    # print(cs)
                    cscores = [c.backpropagate() for c in cs]
                    # It is the algorithm's turn
                    if self.state.currentTurn == self.turn:
                        self.score = max(cscores) if cscores else 0
                    # It is the other player's turn
                    else:
                        self.score = min(cscores) if cscores else 0
                elif aggregator == 'average':
                    num_children = len(self.child_nodes)
                    for c in self.child_nodes:
                        self.score += c.backpropagate() / num_children
                else:
                    raise ValueError('Invalid aggregation function')

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
