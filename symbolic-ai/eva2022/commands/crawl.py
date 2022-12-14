from commandhandler import command
from globals import Eva

import os
from helpers.filehandling import scanDir

from helpers.timefunc import timeFunc
from say import say

@command('crawl')
def crawlCommand(newInput):
    database = Eva.database
    def crawlWrapper():
        p = newInput[6:]
        say(database, f'Scanning {p}')
        scan = database.addNode('file_scan', [], True)
        c = 0
        for d in os.scandir(p):
            scanDir(database, None, d, c, scan)
        say(database, 'Done')
        # !
        return scan
    timeFunc(database, crawlWrapper)()

# TODO: assess database characteristics using statistical tests on sampls of nodes
# TODO: line numbering
