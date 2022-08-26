import nltk
#nltk.download('gutenberg')
#nltk.download('punkt')
from nltk.corpus import gutenberg
from nltk.tokenize.treebank import TreebankWordDetokenizer

import random
from termcolor import colored

source = list(filter(lambda x: 60 > len(x) > 20, gutenberg.sents('shakespeare-hamlet.txt')))
#x = ' '.join(random.choice(source))
x = TreebankWordDetokenizer().detokenize(random.choice(source))

#print(x)
while True:
    g = input()
    for i, c in enumerate(g):
        if x[i] == c: print(colored(c, 'green'), end='')
        elif c in x: print(colored(c, 'yellow'), end='')
        else: print(c, end='')
    print()
