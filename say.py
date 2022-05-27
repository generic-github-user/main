from globals import Eva

def say(database, content, source=None, intent='information', record=False, level=0):
    assert(isinstance(content, str))
    assert(isinstance(source, int) or source is None)
    indents = ' ->*~='

    if record:
        newId = database.addNode('intent', [database.addNode(content, [], True), database.addNode(intent, [], False)])
        database.addNode('origin', [newId, database.addNode('eva_output', [], False)])
        if source is not None:
            database.addNode('source', [newId, source])
    print(('  ' * Eva.loglevel)+indents[Eva.loglevel]+' '+content)
    # return newId
