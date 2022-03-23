import numpy as np
import matplotlib.pyplot as plt
class Collection:
    def __init__(self, members=None):
        if members is None:
            members = []
        self.members = members
