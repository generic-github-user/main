from commandhandler import command
from globals import Eva
database = Eva.database

import pickle
import zlib

@command('loadbackup')
def loadbackupCommand(newInput):
    with open('eva_03_17_2022, 11_41_04.evab', 'rb') as fileRef:
        database.nodes = pickle.loads(zlib.decompress(fileRef.read()))
        # TODO
        database.nodes = list(map(lambda n: database.nodeTemplate(*n), database.nodes))

        database.references = []
        print(f'Building reference lists for {len(database.nodes)} nodes')
        for i, n in enumerate(database.nodes):
            if (i % 1000 == 0):
                say(f'Processed {i} nodes')
            if n.value not in ['origin', 'accessed', 'source', 'type']:
                database.references.append([m.id for m in database.nodes if (n.id in m.members)])
            else:
                database.references.append([])
        print('Done')
    database.save()
