from datetime import datetime
from helpers.getsize import getsize

import zlib
import pickle

from say import say

def backup(database):
    date_format = '%m_%d_%Y, %H_%M_%S'
    backupPath = f'./eva_{datetime.now().strftime(date_format)}.evab'
    with open(backupPath, 'wb') as fileRef:
        nodeList = list(map(list, database.nodes))
        B = zlib.compress(pickle.dumps(nodeList))
        fileRef.write(B)
        say(database, f'Backup saved to {backupPath} [{getsize(B)} bytes]')
    # return backupPath

    callNode = database.addNode('backup', [], True)
    return callNode
