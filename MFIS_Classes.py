#!/usr/bin/env python3
class FuzzySetsDict(dict):
    def printFuzzySetsDict(self):
        for elem in self:
            print("setid:     ", elem)
            self[elem].printSet()


class FuzzySet:
    def __init__(self):
        self.var = ""	        # variable of the fuzzy set (ex.: Age)
        self.label = ""		    # label of the specific fuzzy set (ex.: Young)
        self.x = []		        # list of abscissas, from xmin to xmax, 1 by 1
        self.y = []		        # list of ordinates (float)
        self.memDegree = 0.0    # membership degree for the current application

    def printSet(self):
        print("var:       ", self.var)
        print("label:     ", self.label)
        # print("x coord:   ", self.x)
        # print("y coord:   ", self.y)
        print("memDegree: ", self.memDegree)
        print()


class RuleList(list):
    def printRuleList(self):
        for elem in self:
            elem.printRule()


class Rule:
    def __init__(self):
        self.ruleName = ""	    # name of the rule (str)
        self.antecedent = []    # list of setids
        self.consequent = ""    # just one setid
        self.strength = 0.0     # float
        self.consequentX = []   # output fuzzySet, abscissas
        self.consequentY = []   # output fuzzySet, ordinates

    def printRule(self):
        print("ruleName: ", self.ruleName)
        print("IF        ", self.antecedent)
        print("THEN      ", self.consequent)
        print("strength: ", self.strength)
        print()

class Application:
    def __init__(self):
        self.appId = ""     # application identifier (str)
        self.data = []		# list of ValVarPair

    def printApplication(self):
        print("App ID: ", self.appId)
        for elem in self.data:
            print(elem[0], " is ", elem[1])
        print()


