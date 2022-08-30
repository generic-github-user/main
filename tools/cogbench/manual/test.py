import time

class Test:
    def __init__(self):
        self.created = time.time()

    def upgrade(self, *args, **kwargs):
        template = type(self)(*args, **kwargs)
        for k, v in vars(template).items():
            if not hasattr(self, k):
                setattr(self, k, v)
        return self
