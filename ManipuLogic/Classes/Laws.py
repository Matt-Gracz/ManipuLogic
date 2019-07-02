#!/usr/bin/python
#< ----------- Encodes the laws of Propositional Logic ----------- >
from BaseClasses import *
from Operators import *
from Propositions import *

class Law(LogicalConstruct):
    mapping = {}
    
    def __init__(self, *args, **kwargs):
        mapping = {}

    def createMapping(self, dict):
        self.mapping = dict

class ImplicationReplacement(Law):
    def __init__(self, *args, **kwargs):
        toDisjunction = ["~ant", BinaryOperators.DISJUNCTION, "con"]
        toImplication = ["~ant", BinaryOperators.IMPLICATION, "con"]
        mapping = {
                BinaryOperators.IMPLICATION : toDisjunction,
                BinaryOperators.DISJUNCTION : toImplication,
            }
    
    def applyReplacement(self, proposition):
        firstProp = proposition.rawData
        operator = proposition.operator
        secondProp = proposition.secondProp
        cp = ComplexProp(firstProp, operator, secondProp)
        if(operator in [BinaryOperators.IMPLICATION, BinaryOperators.DISJUNCTION]):
            result = self.mapping[operator]
            ant = result[0].replace("ant", proposition.rawData)
            operator = result[1]
            cons = result[2].replace("con", proposition.secondProp)
            cp = ComplexProp(ant, operator, cons)
        return cp

class DemorgansLaw(Law):
    def __init__(self, *args, **kwargs):
        conjunction = ["~ant", BinaryOperators.DISJUNCTION, "~con)"]
        disjunction = ["~ant", BinaryOperators.CONJUNCTION, "~con)"]
        implication = ["ant", BinaryOperators.CONJUNCTION, "~con)"]
        self.mapping = {
            BinaryOperators.CONJUNCTION : conjunction,
            BinaryOperators.DISJUNCTION : disjunction,
            BinaryOperators.IMPLICATION : implication
            }    

    def applyDemorgansLaw(self, proposition):
        operator = proposition.operator
        result = self.mapping[operator]
        ant = result[0].replace("ant", proposition.rawData)
        operator = result[1]
        cons = result[2].replace("con", proposition.secondProp)
        cp = ComplexProp(ant, operator, cons)
        return cp


    

""" END CLASS """

