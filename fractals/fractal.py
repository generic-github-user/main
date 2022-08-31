
log = math.log
class Fractal:
    info = 'A generic fractal wrapper; describes a mathematical object with self-similar properties'
    
    def __init__(
            self,
            b=10e5,
            n=20,
            o=(0., 0.),
            m=4,
            r=(100, 200),
            frame=None,
            radius=2,
            point_spacing=0.1,
            randomizer=random.uniform,
            **kwargs
        ):
        if type(r) is int:
            r = [r] * 2
        if type(o) in [int, float]:
            o = [o] * 2
        
        self.r = np.array(r)
        self.o = np.array(o)
        self.randomizer = randomizer
        defaults = {
            'z': 0,
            'd': 2
        }
#         kwargs |= defaults
        for k, v in defaults.items():
            if k not in kwargs:
                kwargs[k] = v
        
        for param in ['z', 'd']:
            value = kwargs[param]
            if type(value) in [tuple, list]:
                if len(value) == 2:
                    standard_value = randomizer(*value)
                else:
                    standard_value = random.choice(value)
            else:
                standard_value = value
            
            setattr(self, param, standard_value)
#         self.z = z
#         self.d = d
        self.b = b
        self.m = m
        self.n = n
        
        self.radius = radius
        g = self.radius
        if not frame:
            frame = [[-g, g], [-g, g]]
        self.frame = np.array(frame)# + self.o
        self.f1, self.f2 = self.frame
#         m?

        self.point_spacing = point_spacing
        self.image_size = np.array(np.array([g*2, g*2]) / self.point_spacing, dtype=int)
        print(self.f1)
#         self.image_size = list(map(round, self.image_size))
        self.width, self.height = self.image_size
        
#         self.generate()
        
    def generate(self):
        imsize = self.image_size
        self.canvas = np.zeros(imsize)
        self.iterations = np.zeros(imsize)
#         for x, y in np.ndindex(self.canvas.shape):
        x1, x2, y1, y2 = *self.f1, *self.f2
        ps = self.point_spacing
        points = np.mgrid[x1:x2:ps, y1:y2:ps].reshape(2,-1).T
        for coordinate in points:
            z_ = self.z
#             c = (complex(y, x) / self.r[0] + complex(*self.o)) * self.m
            x, y = coordinate
            c = complex(y, x)
            for i in range(self.n):
                z_ = z_ ** self.d + c
                if abs(z_) > self.b:
#                     index = list(map(round, coordinate * 10))
                    coord_mapping = np.interp(coordinate, [x1, x2], [0, self.width-1])
#                     index = list(map(round, coord_mapping))
                    index = tuple(map(math.floor, coord_mapping))
    #                 canvas[x, y] += i
                    self.canvas[index] = self.norm(abs(z_), i)
#                     self.canvas[index] = i
                    self.iterations[index] = i
                    break
        it = self.iterations
        ca = self.canvas
#         self.canvas = self.scale(self.canvas, it.min(), it.max())
        self.canvas = np.interp(self.canvas, [ca.min(), ca.max()], [it.min(), it.max()])
        self.canvas = self.canvas ** (1/2)
#         print(self.canvas)
        return self.canvas

    def norm(self, x, i):
        norm.params = 7
    #     print(x)
        if x == 0:
            y = 0
        else:
            y = i + 1 - log(abs(log(x))) / log(2)
        return y
#     self.norm.params = 7
#     setattr(self.norm, 'params', 7)
#     norm.params = 7

    def scale(self, x, a, b):
        #return (x - a) / (b - a)
        pass
    scale.info = 'Map a value to a new range based on a minimum and maximum'
    scale.params = [
        ('x', [int, float, np.ndarray], 'The value to map'),
        ('a', [int, float], 'The minimum value of the target range'),
        ('b', [int, float], 'The maximum value of the target range')
    ]
    scale.returns = ('original')
    
    def render(self):
        points = self.generate()
        image = points
        return image
    
    def display(self, cmap=plt.colormaps()):
        if type(cmap) in [list, tuple]:
            cmap = random.choice(cmap)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot()
        image = self.render()
        ax.imshow(image, cmap=cmap)
        plt.axis('off')
        return fig, ax
    
    def find_regions(self, func=np.var, num=5):
        self.generate()
        blocks = []
        w, h = np.array(self.r / num, dtype=int)
        for a in range(num):
            for b in range(num):
                block = self.canvas[a*h: (a+1)*h, b*w: (b+1)*w]
                variance = func(block)
                blocks.append([a, b, w, h, variance])
        return blocks
    
    def autozoom(self):
        region = self.find_regions()
        region.sort(key=lambda x: x[-1], reverse=True)
        region = region[0]
        a, b, w, h, v = region
        region = self.canvas[a*h: (a+1)*h, b*w: (b+1)*w]
        return region
    autozoom.info = 'Automatically find a region of interest and pan/zoom the frame to this area'
    autozoom.params = []
    
    def __call__(self):
        return self.display()
