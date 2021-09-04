import numpy as np
import matplotlib.pyplot as plt
import string
import random
from fuzzywuzzy import fuzz, process
import time
class Device:
    def __init__(self, name, device_type=None, screen_width=None, screen_height=None):
        self.name = name
        self.device_type = device_type
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.created = time.time()
