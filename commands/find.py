from commandhandler import command
from globals import Eva
database = Eva.database

import functools
from helpers.timefunc import timeFunc
timeFunc = functools.partial(timeFunc, database)

from say import say

@command('find')
@timeFunc
def findCommand(newInput):
    # def findInner():
    # TODO: clean this up
    searchNode = database.addNode('search_cmd', [], True)
    database.addNode('source', [searchNode, inputId])
    results = list(filter(lambda x: isinstance(x.value, str) and (newInput[5:] in x.value), database.nodes))
    for n in results:
        print(n)
        database.addNode('origin', [n.id, database.addNode('eva_output', [], False)])
    return searchNode
