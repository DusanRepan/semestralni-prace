from storage import nacti_vse
from collections import Counter

def pocet_podle_druhu():
    data = nacti_vse()
    druhy = [z["druh"] for z in data]
    return Counter(druhy)


def pocet_podle_pohlavi():
    data = nacti_vse()
    pohlavi = [z["pohlavi"] for z in data]
    return Counter(pohlavi)
