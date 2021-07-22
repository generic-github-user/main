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
        plot_params = dict(zip(
            params,
            [Plot.rescale(d, *ranges[i]) if (ranges[i] is not None) else d for (i, d) in enumerate(self.data)]
        ))
        self.axis = ax.scatter(**plot_params, cmap='hsv')
        return self.axis

    def get_scale(A):
        gamma = np.log10(A.max()-A.min())
        print(gamma)
        return gamma > 1.2
    def rescale(a, n, m):
        return np.interp(a, (a.min(), a.max()), (n, m))
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

