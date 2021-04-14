class Settings:
    markers = {
        'dates': '<>',
        'durations': '[]'
    }
    task_properties = ['name', 'content', 'created', 'modified', 'datestring', 'dateparse', 'dateparams', 'datesummary', 'next', 'id', 'importance', 'durationstring', 'duration']
    task_props_short = ['n', 'c', 'tc', 'tm', 'ds', 'dp', 'dr', 'dv', 'nx', 'i', 'im', 'ds_', 'dp_']
    tag_properties = ['name', 'description', 'created', 'modified', 'color', 'parent']
    tag_props_short = ['n', 'd', 'cr', 'm', 'co', 'p']
    command_buffer_size = 20
