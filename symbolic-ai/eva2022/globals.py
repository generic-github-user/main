import spacy

import graphbrain
from graphbrain import hgraph
from graphbrain.parsers import create_parser

class Eva:
    genericFunctions = dict(
        sum=sum,
        mul=lambda a, b: a*b
    )
    modelName = 'en_core_web_sm'
    nlp = spacy.load(modelName)
    gbParser = create_parser(lang='en')
    selection = None
    loglevel = 0    
    database = None
