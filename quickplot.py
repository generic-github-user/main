#!/usr/bin/env python
# coding: utf-8

# QuickPlot contains cleaner and more coherent versions of some functions I commonly use for rapid multidimensional data visualization based on Matplotlib/Pyplot. The idea is to be able to display most types of data with 1-2 lines of code by handling boilerplate and automatically inferring which strategy is preferred for plotting a specific dataset; along with providing an interface to customize the generated plots at multiple levels of abstraction. The tools are mainly NumPy-focused and I am writing this mainly for my own use, so support/stability is not guaranteed.

# In[543]:


get_ipython().run_line_magic('matplotlib', 'widget')

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random


# In[542]:


plt.cm


# In[549]:


class ClassTemplate:
    pass

class Plot(ClassTemplate):
    def __init__(self, data, generate_plot=True, **kwargs):
        self.data = data
        if generate_plot:
            self.plot(**kwargs)
        
    def plot(self, use_density=True, use_latex=True, annotate=10, norm_annotate=True, **kwargs):
        plt.close('all')
        aliases = {
            'projection': ['p']
        }
        values = {
            '2d': None
        }
        varnames = list('xyzw')
        if use_latex:
            varnames = [f'${v}$' for v in varnames]
        
#         for paramset in [aliases, values]:
        for a in list(kwargs.keys()):
            for z in values.keys():
                if kwargs[a] == z:
                    kwargs[a] = values[z]
            for z in aliases.keys():
                if a in aliases[z]:
                    kwargs[z] = kwargs[a]
                    kwargs.pop(a)
                
        fig = plt.figure(figsize=(8, 8))
#         plt.style.use('fivethirtyeight')
        plt.style.use('seaborn-white')
        ax = fig.add_subplot(**kwargs)
        params = list('xysc')+['alpha']
        ranges = [None, None, [2, 10], None, [0,1]]
        projection = '2d'
        if 'projection' in kwargs:
            if kwargs['projection']:
                projection = kwargs['projection']
        else:
            projection = '2d'
        if use_density:
            si = params.index('s')
            print(self.data.shape)
            print(num_points)
            ranges[si] = np.array(ranges[si]) * (20 / (num_points ** (1/1.5)))
#         print(ax.set_xtitle)
        plot_params = dict(zip(
            params,
            [Plot.rescale(d, *ranges[i]) if (ranges[i] is not None) else d for (i, d) in enumerate(self.data)]
        ))
        spatial = list('xyz')
        numdims = int(projection[0])
        print(spatial[:numdims])
        
        for i, a in enumerate(spatial[:numdims]):
            label = varnames[i]
            print(f'Setting axis label: {label}')
            getattr(ax, f'set_{a}label')(label)
#             if np.log10(self.data.data[i].max()-self.data.data[i].min()) > 1.5:
            if Plot.get_scale(self.data.data[i]):
                getattr(ax, f'set_{a}scale')('log')
        self.axis = ax.scatter(**plot_params, cmap='hsv')
        return self.axis

    def get_scale(A):
        gamma = np.log10(A.max()-A.min())
        print(gamma)
        return gamma > 1.2
    
    def place_coords(self, points):
        for point in points:
            coordinate = ", ".join(map(str, point[:2].round(2)))
            text = f'$({coordinate})$'
#             text = '.'
            plt.text(*point[:2], text, size=12)
    
    def sample(A, n, weights=None):
        return A[np.random.choice(A.shape[0], n, replace=False, p=weights)]
    
#     scatterplot density estimation?
    def grid(shape):
        return np.stack(np.meshgrid(*[np.arange(0, dim, 1) for dim in shape]), axis=2)
    
    def grid_like(A):
        return Plot.grid(A.shape)
    
    def rescale(a, n, m):
        return np.interp(a, (a.min(), a.max()), (n, m))

    def pickle(self, include_imports=True):
#         source = ''
        lines = []
        if include_imports:
            lines.extend(f'import {m}' for m in ['matplotlib.pyplot as plt', 'numpy as np'])
        source = '\n'.join(lines)
        return source
    
# TODO: add methods for interactive plotting (and editing, saving, etc.)
# TODO: automatically choose scale(s)
# TODO: add NetworkX functions (and handling for other classes/datatypes)
# TODO: add automatic label overlap reduction/text spacing
# t-sne
# In[ ]:


plt.scatter()


# In[ ]:


np.random.


# In[23]:


import nltk


# In[ ]:


colors = np.stack(np.meshgrid(*[np.arange(0, dim, 1) for dim in canvas.shape[:2]]), axis=2)

