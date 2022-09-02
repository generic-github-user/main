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
    else:
        parts = duration.replace(',', '').replace('and', '').split(' ')
        for i, p in enumerate(parts):
            if p.isnumeric():
                for v in time_info:
                    unit = parts[i+1]
                    # if (unit in v) or (unit+'s' in v):
                    if (unit in v) or (unit[-1] == 's' and unit[:-1] in v):
                        result += float(p) * v[0]
                        break
    return result
