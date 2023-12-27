from nltk.corpus import words

with open("mydict.txt", "a") as f:
    for word in words.words():
        f.write(word.lower() + '\n')
        