
class Point:
    def __init__(self, pos, p=8):
        self.pos = np.array(pos, dtype=float)
        self.precision = p
        
    def move(self, delta):
        self.pos += np.array(delta)
        return self
    
    def rotate(self, a, theta, rad=False):
        theta = float(theta)
        if not rad:
            theta = theta * math.pi / 180
        rotation_matrix = [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ]
#         print(rotation_matrix)
#         self.pos *= rotation_matrix
        self.move(-a.pos)
        self.pos = np.dot(self.pos, rotation_matrix)
        self.move(a.pos)
        self.pos = self.pos.round(self.precision)
        return self
    
    def __call__(self):
        return self.pos
    
    def print(self):
        print(self)
        return self
        
    def __str__(self):
        return 'Point ' + str(self.pos)

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def move(self, delta):
        for p in [self.a, self.b]:
            p.move(delta)
        return self
            
    def rotate(self, *args, **kwargs):
        for p in [self.a, self.b]:
            p.rotate(*args, **kwargs)
        return self
    
    def divide(self, n=1):
#         return [Line(Point(np.average([self.a, self.b], weights=[]))) for i in range(n)]
        sections = []
        for i in range(n):
            a_ = np.average([self.a(), self.b()], weights=[i, n-i], axis=0)
            b_ = np.average([self.a(), self.b()], weights=[i+1, n-i-1], axis=0)
            s = Line(
                Point(a_),
                Point(b_)
            )
            sections.append(s)
        return sections
        
    def __str__(self):
        return 'Line\n\t' + '\n\t'.join(str(v) for v in [self.a, self.b])


class Polygon:
    def __init__(self, vertices=None):
        if not vertices:
            vertices = []
        self.vertices = vertices
        self.v = self.vertices
        
    def __str__(self):
        return 'Polygon\n\t' + '\n\t'.join(str(v) for v in self.v)


# In[5]:


class RegularPolygon(Polygon):
    def __init__(self, r=1, n=4, c=None):
        super().__init__()
        self.v.append(Point([0, r]))
        if not c:
            c = Point([0, 0])
        self.center = c
        for i in range(n-1):
            self.v.append(Point(self.v[-1].pos).rotate(c, 360 / n))
