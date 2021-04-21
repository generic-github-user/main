import json

class Node:
    def __init__(self, state=None, depth=1):
        self.parents = []
        self.children = []
        self.score = 0
        self.state = state
        self.max_depth = 8
        self.depth = depth
        self.turn = 2
        self.terminate = False
        self.outcome = 0
        self.inf = 1000000

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

                branch.parents.append(self)
                if recursive and not branch.terminate:
                    branch.generate_branches()
                self.children.append(branch)

    def term_nodes(self):
        results = []
        for c in self.children:
            if c.terminate:
                results.append(c)
            else:
                results.extend(c.term_nodes())
        return results

    def count_subnodes(self):
        total = len(self.children)
        for n in self.children:
            total += n.count_subnodes()
        return total

    def backpropagate(self, q=0, direction='down', aggregator='minimax', use_inf=False):
        if direction == 'up':
            if self.terminate:
                if self.outcome == 2:
                    self.score += 1
                elif self.outcome == 1:
                    self.score -= 1
            else:
                self.score += (q / len(self.children))
                # self.score += q / self.count_subnodes()

            for p in self.parents:
                p.backpropagate(q=self.score)
        elif direction == 'down':
            if self.terminate:
                if use_inf:
                    delta = self.inf
                else:
                    delta = 1

                if self.outcome == 2:
                    self.score += self.inf
                elif self.outcome == 1:
                    self.score -= self.inf
            else:
                if aggregator == 'minimax':
                    # current_turn = None
                    cs = self.children
                    # print(cs)
                    cscores = [c.backpropagate() for c in cs]
                    # It is the algorithm's turn
                    if self.state.currentTurn == self.turn:
                        if use_inf:
                            max_score = -self.inf
                            for c in self.children:
                                if c.score > max_score:
                                    max_score = c.score
                            self.score = max_score
                        else:
                            self.score = max(cscores) if cscores else 0
                    # It is the other player's turn
                    else:
                        if use_inf:
                            min_score = +self.inf
                            for c in self.children:
                                if c.score < min_score:
                                    min_score = c.score
                            self.score = min_score
                        else:
                            self.score = min(cscores) if cscores else 0
                elif aggregator == 'sum':
                    pass
                elif aggregator == 'average':
                    num_children = len(self.children)

                    for c in self.children:
                        self.score += c.backpropagate() / num_children

                    # ?
                    # if self.state.currentTurn == self.turn:
                    #     for c in self.children:
                    #         self.score += c.backpropagate() / num_children
                    # else:
                    #     for c in self.children:
                    #         self.score -= c.backpropagate() / num_children
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
        for n in self.children:
            node_list.append(n)
            node_list.extend(n.subnodes())
        return node_list

    # def min(self):
    #     return max(self.children, key=lambda x: x.score)
    #
    # def max(self):
    #     return min(self.children, key=lambda x: x.score)

    def min(self):
        return min(self.children, key=lambda x: x.score)

    def max(self):
        return max(self.children, key=lambda x: x.score)

    def best(self):
        if self.state.currentTurn == self.turn:
            best_move = self.max()
        else:
            best_move = self.min()
        return best_move
