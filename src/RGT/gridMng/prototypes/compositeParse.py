import itertools


class CompositeParse():
    def __init__(self, initialString):
        self.initialString = initialString
        self.listOfCompositions = []

    def getCountItems(self):
        return self.initialString.count('&') + 1

    def getCompositions(self):
        if len(self.initialString) == 0:
            raise Exception("Invalid composite string")
        if len(self.initialString) < 2:
            raise Exception("Invalid composite string")

        words = self.initialString.split("*")
        listOfLists = []

        for w in words:
            if '|' in w:
                listOfLists.append(w.replace('(','').replace(')','').split("|"))
            else:
                listOfLists.append([w.replace('(','').replace(')','')])

        self.listOfCompositions = list(itertools.product(*listOfLists))
        return self.listOfCompositions

    def getNumberOfCompositions(self):
        return len(self.getCompositions())
