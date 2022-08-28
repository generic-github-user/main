class Randomizer:
    def __init__(self, lower=0, upper=1, distribution='uniform', form='continuous'):
        self.lower = lower
        self.upper = upper
        self.distribution = distribution

    def sample(self):
        return getattr(random, self.distribution)(self.lower, self.upper)

    def __call__(self):
        return self.sample()

for cls in [Graph, Node]:
    if hasattr(cls, 'init'):
        setattr(cls, '__init__', getattr(cls, 'init'))
