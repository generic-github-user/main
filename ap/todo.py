import pickle
import datetime
import re
import time

dbpath = '~/Desktop/todo.pickle'
todopath = '~/Desktop/.todo'

try:
    with open(dbpath, 'rb') as f:
        data = pickle.load(f)


class todo:
    def __init__(self, content) -> todo:
        self.content = content
        self.done = False
        self.donetime = None
        self.snapshots = []
        self.tags = []
        self.created = time.time()
        self.importance = 0
        self.location = ''
        self.sub = []
        self.parent = None
