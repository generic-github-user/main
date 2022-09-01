from commandhandler import command
from globals import eva
database = Eva.database

import re
import dateparser

@command('todo')
def todoCommand(newInput):
    if not isinstance(newInput, str):
        raise TypeError
    #match = re.search('', newInput[5:])
    database.addNode('label', [
            database.addNode(newInput[5:], [], True),
            database.addNode('todo', [], False)
        ], True)

#@command('done')
