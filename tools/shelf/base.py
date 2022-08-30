import uuid
import time
import datetime

from stringb import String

class Base:
    def __init__(self, log=False):
        self.uuid = uuid.uuid4().hex
        now = time.time()
        self.created = now
        self.timestamp = datetime.datetime.fromtimestamp(self.created).strftime('%b. %d, %Y')
        self.timestamp = String(self.timestamp)
        self.modified = time.time()
        self.accessed = time.time()
        if log:
            print(f'Created {type(self).__name__} instance at {now}')

    def upgrade(self, *args, **kwargs):
        template = type(self)(*args, **kwargs)
        for k, v in vars(template).items():
            if not hasattr(self, k):
                setattr(self, k, v)
        self.timestamp = datetime.datetime.fromtimestamp(self.created).strftime('%b. %d, %Y')
        if isinstance(self.timestamp, str):
            self.timestamp = String(self.timestamp)
        return self

    def changed(self):
        self.modified = time.time()
        return self
