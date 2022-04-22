import time

from settings import Settings

def timeFunc(database, F, level=0):
    def timed(*args, **kwargs):
        start = time.time()

        if Settings.debugInfo:
            say('Executing function', level=level+1)

        fOut = F(*args, **kwargs)
        end = time.time()
        elapsed = end - start

        assert(fOut is not None)
        src = [fOut] if (fOut is not None) else []
        database.addNode('start_time', src + [database.addNode(start, [], False)], False, True, level=level+1)
        database.addNode('end_time', src + [database.addNode(end, [], False)], False, True, level=level+1)
        database.addNode('duration', src + [database.addNode(elapsed, [], False)], False, True, level=level+1)

        if Settings.debugInfo:
            say(f'Finished execution in {elapsed} seconds', level=level)

        return fOut
    return timed
