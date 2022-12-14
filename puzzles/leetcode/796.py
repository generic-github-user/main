class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        # there are probably some interesting solutions with modulo, but i
        # can't imagine any of them are faster than this
        return any(s[i:] + s[:i] == goal for i in range(len(goal)))
