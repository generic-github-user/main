class Attractor:
    def __init__(self):
        self.points = []
        self.canvas = np.zeros([500, 500])


class ChaosGame(Attractor):
    def __init__(self, n=3):
        super().__init__()
        
        if type(n) in [tuple, list]:
            n = random.randint(*n)
        self.shape = RegularPolygon(n=n)
        self.vertices = [0] * 10
        self.compute = 0
        self.n = n
        
    def dist(self, a, b):
        d = abs(a - b)
        return min(d, self.n-d)
    dist.info = 'Calculate the distance between elements of a ring; e.g., vertices of a polygon'
        
    def create_rule(self, n, m, q):
#         return lambda x, f: f(*n) not in m
        return lambda x, f: q(f(*[x[i] for i in n]) in m)
        
    def generate(self, x=10, y=0.5, e=0, rule=None, direct=True):
        dt = int if direct else float
        
        if type(y) in [tuple, list]:
            if len(y) == 3:
                y_ = y[-1]
            else:
                y_ = 1
#             y = random.uniform(*y)
            interpolation_factors = np.random.uniform(*y[:2], [y_])
        elif type(y) in [int, float]:
            interpolation_factors = np.array([y])
    
        if type(e) in [tuple, list]:
            if len(e) == 3:
                e_ = e[-1]
            else:
                e_ = 1
            shift_values = np.random.uniform(*e[:2], [e_, 2]).astype(dt)
        elif type(e) in [int, float]:
            shift_values = np.array([[e]*2])
        
        
        p = np.random.uniform(-5, 5, self.shape.center.pos.shape).astype(dtype=dt)
#         if rule:
#             self.vertices = [-1] * abs(min(rule))

        if rule == 'random':
            j = random.choices(list(range(-10, -1)), k=1) + [-1]
            k = random.choices(list(range(0, self.n // 2 + 1)), k=random.randint(0,3))
            q = random.choice([lambda l: not l, lambda l: l])
#             j, k = [-2, -1], [0]
#             rule_gen = lambda n, m: (lambda x, f: f(*n) not in m)
            rule = self.create_rule(j, k, q)
            print(j, k)
        self.rule = rule
            
        for i in range(x):
#             random.choice(self.shape.v)
            v = random.randint(0, len(self.shape.v)-1)
            rule_eval = False
            if rule:
                if type(rule) in [list, tuple]:
                    rule_eval = get_ipython().getoutput('(any(self.vertices[i] == v for i in rule)')
                elif callable(rule):
                    rule_eval = rule(self.vertices + [v], self.dist)
                    # TODO: optimized rule evaluation
#                     print(self.vertices + [v], rule_eval)
#                     try:
#                         rule_eval = rule(self.vertices + [v], self.dist)
#                     except:
#                         rule_eval = True
            else:
                rule_eval = True
            
            if rule_eval:
                val = np.random.choice(interpolation_factors)
                p += shift_values[np.random.randint(shift_values.shape[0]), :]
                p = np.average([p, self.shape.v[v].pos], axis=0, weights=[1-val, val])
                self.compute += 1
                
                if direct:
                    point_array = np.interp(p, [-2, 2], [0, 500])
                    point_array = point_array.astype(int).clip(0, 500-1)
                    x_, y_ = tuple(point_array)
                    self.canvas[x_-1:x_+1, y_-1:y_+1] += 0.01
                else:
                    self.points.append(p)
            self.vertices.append(v)
        print('complete')
        return self
    generate.info = 'Simulate the "chaos game", generating a series of points according to the given rules'
    
    def render(self, r=100, color=''):
        canvas = np.zeros([r, r])
        points_array = np.interp(np.array(self.points), [-1.5, 1.5], [0, r])
        points_array = points_array.astype(int).clip(0, r-1)
        for i, p in enumerate(points_array):
            if color == 'index':
                c = i
            elif color == 'vertex':
                c = self.vertices[i]
            else:
                c = 0.01
            x, y = p.round()
            canvas[x-1:x+1, y-1:y+1] += c
        return np.flip(canvas.T)
    render.info = 'Convert the computed points to a displayable image'
