import numpy as np
import nltk
from nltk.corpus import words

class SpellChecker:
    def __init__(self, word_list = words.words()):
        self.word_list = word_list

    def minimum_edit_distance(self, source, target):
        m, n = len(source), len(target)
        D = np.zeros((m + 1, n + 1))
        for i in range(1, m + 1):
            D[i, 0] = i
        for j in range(1, n + 1):
            D[0, j] = j
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                if source[i - 1] == target[j - 1]:
                    cost = 0
                else:
                    cost = 1
                D[i, j] = min(D[i - 1, j] + 1, D[i, j - 1] + 1, D[i - 1, j - 1] + cost)
        return D[m, n]

    def suggest(self, word):
        suggestions = []
        for candidate in self.word_list:
            if abs(len(candidate) - len(word)) > 2:
                continue
            if len(set(candidate) & set(word)) < len(candidate) / 2:
                continue
            distance = self.minimum_edit_distance(word, candidate)
            suggestions.append((candidate, distance))
        suggestions.sort(key=lambda x: x[1])
        return [word for word, distance in suggestions[:5]]

word_list = (word.lower() for word in words.words())
spell_checker = SpellChecker(word_list)
# print(spell_checker.suggest("spwlling"))
