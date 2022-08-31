
class IteratedFunction(Attractor):
    def __init__(self, a=0.5):
        super().__init__()
        self.a = a
#         self.points = [np.random.uniform(-1, 1, [2])]
        self.points = [np.ones([2])]
        self.p = self.points
        self.origin = Point([0, 0])
        self.f = [
#             np.sin, np.cos
            lambda x, y, z: x.rotate(z, y),
            lambda x, y, z: x.move([0.5, -0.5])
        ]
        
    def generate(self, x=100):
        coefficients = np.random.uniform(-2, 2, [2])
        exponents = np.array(list(range(2)))
        p = self.points[-1]
        for i in range(x):
#             p = np.sin(self.a * np.power(self.points[-1], 1))
#             p = np.sum([coefficients[j] * np.power(p, e) for j, e in enumerate(exponents)], axis=0)
#             p = p * self.a + (i / 10000)
#             p = abs(p) ** 0.3
#             p = random.choice(self.f)(p + (i * 0.001)) * 10
#             p = np.sin(self.points[-1] + np.product(self.points[-1])) * 100
            p = Point(p[:2])
#             c = np.random.uniform()
#             c = np.prod(p.pos) * 1
#             c = i / x * 5
            c = np.sin(i) + 1
            q = random.choice(self.f)
#             for j in range(5):
#                 p = q(p, c+np.random.uniform(), Point(np.random.uniform(-50, 50, [2])))
            p = q(p, c+np.random.uniform(), self.origin)
            p = p.pos
            
            self.points.append(p)
        return self
    
    def render(self, r=100):
        canvas = np.zeros([r, r])
        points_array = np.array(self.points)
        points_array = np.interp(points_array, [points_array.min(), points_array.max()], [0, r])
        points_array = points_array.astype(int).clip(0, r-1)
        for i, p in enumerate(points_array):
            canvas[tuple(p[:2].round())] += 0.01
        return np.flip(canvas.T)
    render.info = 'Convert the computed points to a displayable image'
    
f = IteratedFunction(a=0.01).generate(10000)
plt.figure(figsize=(6, 6))
plt.imshow(f.render(300), cmap='jet')
plt.axis('off')
