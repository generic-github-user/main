class Solution:
    def areOccurrencesEqual(self, s: str) -> bool:
        # fun trick borrowed from https://stackoverflow.com/questions/3787908/python-determine-if-all-items-of-a-list-are-the-same-item#comment4013488_3787948
        return len(set(s.count(c) for c in set(s))) == 1
