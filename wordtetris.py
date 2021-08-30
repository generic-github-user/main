# import keyboard
import curses
import os
import numpy as np
import string
import random
import time

import nltk
from nltk import FreqDist
from nltk.corpus import brown
nltk.download('brown')

word_limit = 20000
word_frequencies = FreqDist(i.lower() for i in brown.words()).most_common()
# print(word_frequencies.most_common()[:10])# words = word_frequencies.keys()[:10000]
words = [a for a, b in word_frequencies[:word_limit]]
words = [word.translate(str.maketrans('', '', string.punctuation)) for word in words]