import numpy as np
import matplotlib.pyplot as plt
class Collection:
    def __init__(self, members=None):
        if members is None:
            members = []
        self.members = members

class Polyomino:
    def __init__(self, size=100):
        self.data = np.ones((1, 1))
        self.indices = [(0, 0)]
        self.neighbors = [0]
        self.size = 1
