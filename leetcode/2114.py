class Solution:
    def mostWordsFound(self, sentences: List[str]) -> int:
        # split sentence, count words, find max
        return max(len(s.split()) for s in sentences)
