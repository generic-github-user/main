from base import Base
from stringb import String

class Values:
    def __init__(self):
        self.importance = 100

class Note(Base):
    def __init__(self, content, container=None):
        super().__init__()
        assert isinstance(content, (str, String))
        self.content = String(content)
        self.container = container
        self.hash = hash(self.content)
        self.ratings = Values()
        self.importance = self.ratings.importance
        self.terms = []
        self.tags = []

    def changed(self):
        super().changed()
        self.importance = self.ratings.importance
        self.length = self.content.length
        self.words = self.content.tokens
        return self

    def upgrade(self):
        super().upgrade(self.content)
        self.importance = self.ratings.importance
        if isinstance(self.content, str):
            self.content = String(self.content)
        self.changed()
        return self

    def similar(self, **kwargs):
        return self.container.similar(self, **kwargs)

    def __str__(self):
        return f'{self.content.truncate()} [{self.timestamp.color("cyan")}]'
