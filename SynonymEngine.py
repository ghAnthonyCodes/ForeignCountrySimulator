import numpy as np

english = [ ['greetings', 'hello'] ]

def Synonym(word):
    for cat in english:
        if word in cat:
            return np.random.choice(cat)