from base import Base

class Term(Base):
    def __init__(self, content, frequency=None):
        super().__init__()
        self.content = content
        self.frequency = frequency

    def __str__(self):
        return self.content
