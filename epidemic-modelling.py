#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# modelling response/policy


# In[122]:


get_ipython().run_line_magic('matplotlib', 'widget')
import matplotlib.pyplot as plt
import numpy as np
import random
import base64


# In[449]:


class Pathogen:
    def __init__(self, **kwargs):
        defaults = dict(
            infectiousness=0.01,
            virulence=0.1,
            symptomaticity=0.8,
            incubation_period=14/365,
            disease_period=7/365,
        )
#         period of communicability
        defaults |= kwargs
        for k, v in defaults.items():
            setattr(self, k, v)
    
    def __str__(self):
        return f'Pathogen ({self.infectiousness})'
    
    def __repr__(self):
        return str(self)

# In[536]:


def clipped_normal(a, b, c, d, s=None):
    return np.clip(np.random.normal(a, b, s), c, d)
def display(text):
    if isinstance(text, (float, np.float)):
        text = round(text, 2)
    return str(text)

# In[551]:


class History:
    def __init__(self):
        self.number_infected = []
        self.number_killed = []
        self.number_ever_infected = []
class Population:
    def __init__(self, members=None, size=10, step_duration=1/365):
        self.size = size
        self.step_duration = step_duration
        self.age = 0
        if members is None:
            self.members = []
            for n in range(self.size):
                self.add()
        else:
            self.members = members
        self.history = History()
        self.cache = {}
#         self.memoized = {}
        self.compute_used = 0
