from tkinter import *
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from colour import Color
from scipy import signal
from copy import deepcopy
import math

class Automata:
    """A generic cellular automaton world"""

    def __init__(self, size=None, birth=[3], live=[2, 3], neighborhood=1, edges='wrap', cell_width=5, initial=0.5, initial_size=0.25, generations=30, record=True, **kwargs):
        """
        Create a new cellular automaton
        @params
            size
                [int]: Both width and height of world
                [[int], l2]: Width and height of world
            neighborhood
                [int, r>=1]: Size of neighborhood in cells from center; `2` would produce a 5x5 neighborhood
                [int][2]: Width and height of neighborhood {planned}
        if size is None:
            size = [64, 64]
        elif type(size) is int:
            size = [size] * 2
        self.size = np.array(size)
        self.cell_width = cell_width
        # self.world = np.random.randint(0, 2, self.size)
        # self.world = np.round(np.random.uniform(*initial, self.size)+0.41)
        self.world = np.zeros(self.size)

        if type(generations) in [tuple, list]:
            generations = random.randint(*generations)
        self.generations = generations
        self.args = kwargs

        self.initial_size = initial_size
        """
        Size of initial random cells; one of:
        - float from 0 to 1 dictating what fraction of width/height should be filled at the start
        - integer from 0 to `size` describing the width/height (in cells) of the random noise
        - a list or tuple containing two of the above, the first for the width and the second for the height
        """
        if type(initial_size) is float:
            initial_size *= self.size
        x1, y1 = (self.size // 2) - (initial_size // 2)
        x2, y2 = (x1, y1) + initial_size

        if type(initial) is float:
            initial = [1-initial, initial]
        print(x1, y1, x2, y2)
        c = [x1, y1, x2, y2]
        x1, y1, x2, y2 = [math.floor(m) for m in c]
        self.world[x1:x2, y1:y2] = np.random.choice([0, 1], initial_size.astype(int), p=self.initial)
        # self.world[10:12,10:12]=1
        self.zoom = 1
        self.edges = edges

        if type(birth[0]) in [tuple, list]:
            birth = [random.randint(*b) for b in birth]
        self.birth = birth
        self.live = live

        self.activity = np.zeros(self.size)
        self.population = []
        self.generation = 0
        self.age = np.zeros(self.size)
        self.neighbors = np.zeros(self.size)
        self.age_history = []
        self.neighbor_history = []

        if type(neighborhood) in [tuple, list]:
            neighborhood = random.randint(*neighborhood)
        self.neighborhood = neighborhood

        self.kernel = np.ones([self.neighborhood*2+1]*2)
        # np.put(self.conv, self.neighborhood**2//2, 0)
        np.put(self.kernel, self.kernel.size//2, 0)
        # print(self.conv)

        # self.history = self.world.copy()
        self.record = record
        self.history = np.expand_dims(self.age.copy(), axis=0)

    def evolve(self, steps=None, use_convolutions=True, return_value='world'):
        if steps is None:
            steps = self.generations
        # print(steps)
        for i_ in range(steps):
            # for i in range(n)
            if use_convolutions:
                # Make a copy of the current world so the previous state can be used to determine the next state without unwanted modification
                self.temp = self.world.copy()
                # Apply kernel to each cell in the world (and handle edges with specified method) to generate a matrix of neighbor counts
                n = signal.convolve2d(self.temp, self.kernel, boundary=self.edges)
                # Omit the edges
                n = n[1:-1, 1:-1]
                # print(n.shape)
                # print(np.isin(np.array([2, 3, 5]), self.live))
                birth_cond = np.logical_and(self.temp == 0, np.isin(n, self.birth))
                survival_cond = np.logical_and(self.temp == 1, np.isin(n, self.live))
                # Apply rules to every cell and output 1 where true, 0 where false
                # np.where is preferable to looping through each cell in the world since NumPy can vectorize some operations, dramatically improving efficiency
                indices = np.where(np.logical_or(survival_cond, birth_cond), 1, 0)
                # self.world = np.where(indices == 1)
                # self.world = indices
                self.world = indices.copy()
                # Add indices matrix to age
                self.age += indices
                # Multiply by indices matrix to reset age of dead cells (where value is 0)
                self.age *= indices
                # print(indices, n)
            else:
                self.temp = np.pad(self.world.copy(), self.neighborhood, constant_values=0)
                for ix, iy in np.ndindex(self.world.shape):
                    # :/
                    current = self.world[ix, iy]
                    neighbors = np.sum(self.temp[ix:ix+2+self.neighborhood, iy:iy+2+self.neighborhood]) - self.temp[ix+self.neighborhood, iy+self.neighborhood]
                    self.neighbors[ix, iy] = neighbors
                    # print(temp[ix-1:ix+2, iy-1:iy+2])
                    # print(temp[ix:ix+3, iy:iy+3])
                    # print(ix-1, ix, ix+1, iy-1, iy, iy+1)
                    # print(neighbors)
                    if neighbors in self.birth:
                        self.world[ix, iy] = 1
                    # elif?
                    if neighbors not in self.live:
                        self.world[ix, iy] = 0
                        self.age[ix, iy] = 0
                    else:
                        self.age[ix, iy] += 1

            self.population.append(self.world.sum())
            self.age_history.append(self.age.mean())
            self.activity += self.world
            self.neighbor_history.append(n.mean())
            self.generation += 1
            self.compute = self.generation * np.product(self.world.shape)
            if self.record:
                self.history = np.append(self.history, np.expand_dims(self.world, axis=0), axis=0)
        # print(self.population[-1])

        if return_value == 'self':
            return self
        elif return_value == 'world':
            return self.world
        # print(temp.shape)

    def clone(self):
        return deepcopy(self)

    def display(self, source='world', renderer='pyplot', norm=None, history=False):
        if history:
            ax = plt.figure().add_subplot(projection='3d')
            print(self.history.shape)
            ax.voxels(self.history, alpha=0.5)
            plt.show()
        else:
            processed = getattr(self, source)
            if norm:
                processed = norm(processed.copy())
            if renderer == 'pyplot':
                plt.imshow(processed, interpolation='none', cmap='plasma')
                plt.show()

class Aggregator:
    """A set of cellular automata worlds generated according to a provided space of initial conditions; simulates worlds sampled from this space and collects the results for analysis (for example, analyzing the relationship between the initial density of living cells in Conway's Game of Life and the population after 1000 generations)"""
    def __init__(self, hyperparameters=None, metrics=None, selection='random', randomizer=random.uniform, trials=20):
        """Create a new Aggregator instance"""
        self.simulations = []
        default_params = {
            'initial': (0.05, 0.95),
            'initial_size': (0.25, 0.75),
            # 'size': 32,
            'generations': 30,
        }
        if hyperparameters is None:
            hyperparameters = default_params
        elif type(hyperparameters) is dict:
            hyperparameters = hyperparameters | default_params

        if metrics is None:
            metrics = [
                # Each metric is formatted as [title, temporal_reduction, population_reduction]
                # title describes the metric assigned to that axis
                # temporal_reduction is how the time axis of each trial is eliminated with respect to the corresponding metric; if 'none', each data point will be displayed
                # population_reduction is how metrics are summarized across trials; for example, creating a line graph of the average population trajectory across 500 simulations
                # note: spacial reduction is handled by the Automata class, which averages metrics for every cell
                ['population', 'none', 'rand'],
                # ['age_history', 'none', 'none'],
                # ['neighbor_history', 'none', 'none']
            ]

        self.hyperparameters = hyperparameters
        self.hp = self.hyperparameters
        self.metrics = metrics
        self.results = []
        self.trials: int = trials
        """The number of trials to run"""
        self.axes = []

    def run(self, trials=None):
        """Run the specified number of trials with set hyperparameters"""
        if trials is None:
            trials = self.trials
        print('Running {} trials'.format(trials))
        self.axes = [m[0] for m in self.metrics] + [h for h in self.hyperparameters]#[:2]

        for t in range(trials):
            # trial_params = deepcopy(hyperparameters)
            # trial_params = {}
            # for k, v in self.hyperparameters.items():
            #     if type(v) in [int, float]:
            #         trial_params[k] = v
            #     elif type(v) in [tuple, list]:
            #         if type(v[0]) is float:
            #             trial_params[k] = random.uniform(*v)
            #         elif type(v[0]) is int:
            #             trial_params[k] = random.randint(*v)
            # TODO: delegate random parameter value generation to cellular automata constructor
            trial_params = self.hyperparameters

            trial = Automata(**trial_params)
            for g in range(self.hp['generations']):
                trial.evolve(use_convolutions=True)

            trial_data = []
            for m in self.metrics:
                data_slice = getattr(trial, m[0])
                trial_data.append(data_slice)
                # self.axes.append(m[0])
            for h in self.hyperparameters:
                data_slice = getattr(trial, h)
                if type(data_slice) not in [int, float]:
                    data_slice = data_slice[0]
                data_slice = [data_slice] * self.hp['generations']
                trial_data.append(data_slice)
                # self.axes.append(h)
                # print(h, data_slice)
            self.results.append(trial_data)

            if (t+1) % 10 == 0:
                print('{} trials ({}%) complete'.format(t+1, round((t+1)/trials*100, 2)))

        def rand_slice(array, axis=0):
            return random.choice(array)

        np_functions = {
            'mean': np.mean,
            'average': np.mean,
            'max': np.max,
            'min': np.min,
            'rand': rand_slice,
            'random': rand_slice
        }

        self.results = np.array(self.results)
        for i, m in enumerate(self.metrics):
            # if m[2] in ['mean', 'average']:
            if m[2] in np_functions:
                reduction_func = np_functions[m[2]]
                self.results = reduction_func(self.results, axis=0)
            if m[1] in ['last']:
                self.results = self.results[-1]
        print(self.results.shape)
        self.results = self.results.squeeze()
        print('Simulation complete')
        return self.results

    def display(self):
        """Display collected results in a graph"""
        # print(list(zip(*self.results)))
        print('Displaying results ({} trials)'.format(len(self.results)))
        # data = np.array(list(zip(*self.results)))
        data = self.results.swapaxes(0,-1)
        print(data)
        # dims = len(data.shape)
        dims = len(self.metrics)
        if dims == 1:
            plt.plot(data, color='blue', alpha=0.2)
            plt.show()
        elif dims == 2:
            plt.scatter(*data)
            plt.show()
        elif dims == 3:
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            print(*data[:3])
            ax.scatter(*data[:3])

            ax.set_xlabel(self.axes[0])
            ax.set_ylabel(self.axes[1])
            ax.set_zlabel(self.axes[2])
            plt.show()

class Search:
    """A search for starting values in a particular automata that produce a specific pattern or condition"""

    def __init__(self, pattern=None, goal=None):
        self.pattern = pattern
        if pattern:
            self.max_score = pattern.sum()
            self.pattern = np.where(pattern, 1, -1)
        self.best = None
        self.best_score = None
        self.goal = goal

    def update_best(self, trial, score):
        self.best = trial.clone()
        self.best_score = score

    def assess(self, trial):
        if self.goal:
            score = self.goal(trial)
        elif self.pattern:
            score = signal.convolve2d(trial.world, self.pattern, boundary='wrap').max()

        if self.best_score is None:
            self.update_best(trial, score)
        elif score > self.best_score:
            self.update_best(trial, score)
        return score

    def run(self, n=50, gens=100, search_all_gens=True, stop_if_found=True):
        for i in range(n):
            trial = Automata()
            
            if search_all_gens:
                for j in range(gens):
                    trial.evolve(steps=1)
                    score = self.assess(trial)
            else:
                trial.evolve(steps=gens)
                score = self.assess(trial)

            if stop_if_found and score == self.max_score:
                break

        return self.best


class CGOL(Automata):
    """Convenience class that produces a cellular automata based on Conway's Game of Life"""

    def __init__(self, **kwargs):
        super(CGOL, self).__init__(**kwargs)


class Scene:
    def __init__(self, content=None):
        self.root = Tk()
        # root.title()
        # root.resizable(False, False)
        if content is None:
            content = Automata()
        self.content = content
        self.dimensions = self.content.size * self.content.cell_width
        w, h = self.dimensions
        self.canvas = Canvas(self.root, width = w, height = h)
        self.canvas.pack()
        self.m = []
        self.paused = False
        self.pen_size = 1
        # self.canvas.mainloop()

    # self.canvas.bind("<B1-Motion>", click_callback)
    def click_callback(self, event):
        # print(event.x, event.y)
        print(event)
        coords = event.x, event.y
        coords = np.array(coords)
        cw = self.content.cell_width
        coords = np.round(coords / cw).astype(int)
        print(coords)
        x, y = tuple(coords)
        p = self.pen_size
        x_, y_ = x+p, y+p
        self.content.world[x:x_, y:y_] = 1
        self.content.temp[x:x_, y:y_] = 1
        x, y = coords * cw
        print(x, y)
        self.m.append(event)
        # self.canvas.create_rectangle(x, y, x+cw, y+cw, fill='green')
        # self.root.update_idletasks()
        # self.canvas.update_idletasks()
        # self.canvas.draw_idle()

    def right_click(self, event):
        coords = event.x, event.y
        coords = np.array(coords)
        cw = self.content.cell_width
        coords = np.round(coords / cw).astype(int)
        self.content.world[tuple(coords)] = 0
        self.content.temp[tuple(coords)] = 0

    def toggle_pause(self, event):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def key_press(self, event):
        char = event.char
        # print(char)
        if char == '-' and self.pen_size > 1:
            self.pen_size -= 1
        elif char == '=' and self.pen_size < 100:
            self.pen_size += 1
        print('Changed pen size to {}'.format(self.pen_size))
        # self.canvas.update_idletasks()

    def step(self, i=0, n=20, render=True, cell_colors='age'):
        # Get the attribute that should be used to color cells in the visualization
        color_source = getattr(self.content, cell_colors)
        if i < n:
            # new_frame = self.content.evolve()
            if not self.paused:
                self.content.evolve()
            # print(new_frame.mean())
            # self.canvas.create_rectangle(20, 20, 50, 50, fill='red')
            world = self.content.world
            new_frame = world
            # Clear the canvas
            self.canvas.delete('all')
            # print(len(self.m))
            # print(np.where(world == 1))
            width = self.content.cell_width
            for ix, iy in zip(*np.where(new_frame)):
                x, y = ix * width, iy * width
                intensity = color_source[ix, iy] / color_source.max()
                c = Color(hue=intensity, saturation=1, luminance=0.5)
                hex = c.hex
                self.canvas.create_rectangle(x, y, x+width, y+width, fill=hex)
            self.canvas.after(1, lambda: self.step(i=i+1, n=n, render=render))
            self.canvas.bind("<B1-Motion>", self.click_callback)
            self.canvas.bind("<B3-Motion>", self.right_click)
            self.canvas.bind("<Double-Button-1>", self.toggle_pause)
            self.root.bind("<Key>", self.key_press)
        else:
            self.end_time = time.time()
            elapsed = round(self.end_time-self.start_time, 1)
            print('Simulated {} frames in {} seconds ({} cells processed)'.format(n, elapsed, self.content.compute))
    def simulate(self, frames=10, render=True):
        self.start_time = time.time()
        self.step(n=frames, render=render)

live_rule = [random.randint(3, 10) for v in range(2)]
# automata = Automata(birth=[(2,4)], live=live_rule, neighborhood=(1,2))

# automata = CGOL(size=128)
# main_scene = Scene(content=automata)
# main_scene.simulate(frames=5000, render=False)
# main_scene.root.mainloop()

# test_analysis = Aggregator(trials=200)
# test_analysis.run()
# test_analysis.display()

test_pattern = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0]
])

test_pattern = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
])

test_goals = [
    lambda x: x.population[-1],
    lambda x: -x.population[-1],
    lambda x: x.age_history[-1],
]
# test_search = Search(goal=test_goals[0], goal_score=100)
# result = test_search.run(n=100, gens=200, search_all_gens=True)
# print(test_search.best_score)
# plt.imshow(result.world, interpolation=None, cmap='plasma')
# plt.show()

CGOL(size=128).evolve(steps=500, return_value='self').display('activity', norm=np.sqrt)
# CGOL(size=16).evolve(steps=50, return_value='self').display(norm=np.sqrt, history=True)


# print(result.world)
# plt.imshow(result.activity, interpolation=None, cmap='plasma')

# plt.plot(main_scene.content.population)
# plt.plot(main_scene.content.age_history)
# plt.show()

# TODO: cube visualization, pattern search
