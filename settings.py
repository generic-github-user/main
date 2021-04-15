class Settings:
    markers = {
        'dates': '<>',
        'durations': '[]'
    }
    task_properties = ['name', 'content', 'created', 'modified', 'datestring', 'dateparse', 'dateparams', 'datesummary', 'next', 'id', 'importance', 'durationstring', 'duration', 'efficiency_ratio', 'archived']
    task_props_short = ['n', 'c', 'tc', 'tm', 'ds', 'dp', 'dr', 'dv', 'nx', 'i', 'im', 'ds_', 'dp_', 'er', 'a']
    tag_properties = ['name', 'description', 'created', 'modified', 'color', 'parent']
    tag_props_short = ['n', 'd', 'cr', 'm', 'co', 'p']
    command_buffer_size = 20

class Aliases:
    add = ['a', '.', 'add', 'create', 'make', 'new']
    find = ['f', 'list', 'find', 'show', 'search', 'print']
    all = ['e', '*', 'all', 'any', 'everything']
    rank = ['r', 'order', 'sort', 'vote', 'arrange', 'rank']
    exit = ['q', 'exit', 'quit', 'leave', 'stop', 'goodbye', 'shutdown', 'end', 'close', 'bye']
    undo = ['u', 'undo', 'reverse', 'rollback']
    select = ['s', 'sel', 'select', 'selection']
    deselect = ['d', 'deselect']
    archive = ['z', 'archive', 'store', 'arch']
    remove = ['remove', 'delete']
    backup = ['b', 'save', 'backup']

    task = ['t', 'task', 'todo']
    tag = ['@', 'tag', 'label']
