@nb.njit
def rotation_matrix(a):
    sin = np.sin(a)
    cos = np.cos(a)
    R = [
        [cos, -sin],
        [sin, cos]
    ]
    return np.array(R)

@nb.njit
def rotate(a, b, t):
#         if type(t) in [int, float]:
#         if isinstance(t, (int, float)):
    t = rotation_matrix(t)

#         return (rMatrix @ (a - b)) + b
    return (t @ (a - b)) + b
