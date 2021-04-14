time_info = [
    [1, 'second', 'sec', 's'],
    [60, 'minute', 'min', 'm'],
    [3600, 'hour', 'hr', 'h'],
    [3600*24, 'day', 'dy', 'd'],
    [3600*24*7, 'week', 'wk', 'w'],
    [3600*24*30, 'month', 'mon', 'mn'],
    [3600*24*365.25, 'year', 'yr', 'y']
]

def parse_duration(duration):
    result = 0
    if ':' in duration:
        parts = duration.split(':')
        for i, p in enumerate(parts.reverse()):
            result += float(p) * time_info[i][0]
