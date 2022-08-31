# @nb.jit
def line(start, stop, bg, width=1., quality=5.):
    """
    Draw a line onto an array using NumPy.

    -`start`: `ndarray`; the start point
    -`stop`: `ndarray`; the end point
    -`bg` (background): `ndarray`; the array to draw the line onto
    -`width`: `int` or `float` >= 1; the thickness of the line
    -`quality`: `int` or `float` >= 1; the number of points to draw for each
    unit of distance between the points

    Returns the modified `bg` array with the line drawn
    """

#     if bg is None:
#         bg = np.zeros((50, 50))
#     start = np.array(start, dtype=float)
#     stop = np.array(stop, dtype=float)
    assert quality >= 1
    assert width > 0

    quality *= np.linalg.norm(np.subtract(stop, start))
    lin = np.linspace(0, 1, round(quality))
#     coords = np.stack([[np.interp(lin, [0,1], [0, p[i]]) for p in [start, stop]] for i in range(0, 2)]).T
#     j = []
#     for i in range(0, 2):
#         j.append(np.interp(lin, [0,1], [start[i], stop[i]]))
    j = [np.interp(lin, [0,1], [start[i], stop[i]]) for i in [0, 1]]
    coords = np.stack(j).T
    for pos in coords:
        x, y = pos#.astype(int)
        w = width/2
        bg[round(x-w):round(x+w), round(y-w):round(y+w)] += 1

    return bg
