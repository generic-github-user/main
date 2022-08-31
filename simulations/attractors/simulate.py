@nb.njit
def simulate_accelerated(speeds, pivots, center, angles, start, points, steps=100, clip=True):
    """
    Efficiently simulate a system of rotating segments joined by pivots using
    Numba to JIT-compile operations on NumPy arrays.

    - `steps`: integer >=1; the number of timesteps to simulate
    - `clip`: `boolean`; whether to limit the maximum angle of each section (if
      `True`, the values will wrap around to 0; defaults to `True`)

    Returns an `ndarray` of the generated points
    """
#     todo: reuse code across this function and the other simulate function

#     assert type(steps) is int
#     assert isinstance(steps, int)
#     assert steps >= 1
#     assert len(speeds) > 0
#     assert len(pivots) > 0

    rMatrices = []
    for s in speeds:
        rMatrices.append(rotation_matrix(s))
    num_pivots = len(pivots)
    for s in range(steps):
        for l in list(range(num_pivots)):
            rMatrix = rMatrices[l]
            offsets = center if l == 0 else pivots[l-1]
            angles[l:] += speeds[l]
            if clip:
                angles[l:] %= 2 * math.pi
        prev = rotate(start[0], center, angles[0])
        for p in range(1, num_pivots):
            pivots[p] = rotate(start[p], center, angles[p]) + prev
            prev = pivots[p]
#         if self.live_rendering:
#             self.draw_point(self.pivots[-1].copy(), 'pixel')
#         else:
        points = np.append(points, np.expand_dims(pivots[-1], axis=0), axis=0)
    return points
# dynamic wrappers for Numba functions
