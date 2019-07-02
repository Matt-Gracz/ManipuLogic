#!/usr/bin/python
#< ----------- Encodes the laws of Propositional Logic ----------- >
from BaseClasses import *
from Operators import *
from Propositions import *
from enum import Enum

class LAWKWORDS:
    FIRSTPROP = "first"
    SECONDPROP = "second"
    NOTFIRST = "~first"
    NOTSECOND = "~second"


class Law(LogicalConstruct):
    """ An abstract law that replaces one set of symbols with another.  Individual laws of 
       replacement will inheret from this class 
    """
    mapping = {}
    
    def applyMapping(self, proposition, allowedOperators = []):
        """ Once a mapping is set up, this function does the work of actually replacing the symbols
           according to the logic encoded in the mapping.
        """
        ant = proposition.rawData
        operator = proposition.operator
        con = proposition.secondProp
        returnProp = ComplexProp(ant, operator, con)
        okToMap = not allowedOperators or operator in allowedOperators
        if(okToMap):
            result = self.mapping[operator]
            ant = result[0].replace(LAWKWORDS.FIRSTPROP, proposition.rawData)
            operator = result[1]
            con = result[2].replace(LAWKWORDS.SECONDPROP, proposition.secondProp)
            returnProp = ComplexProp(ant, operator, con)
        return returnProp
""" END CLASS """

class ImplicationReplacement(Law):
    """ Encodes (P => Q) <==> (~P => Q)
    """

    def __init__(self, *args, **kwargs):
        toDisjunction = [LAWKWORDS.NOTFIRST, BinaryOperators.DISJUNCTION, LAWKWORDS.SECONDPROP]
        toImplication = [LAWKWORDS.NOTFIRST, BinaryOperators.IMPLICATION, LAWKWORDS.SECONDPROP]
        mapping = {
                BinaryOperators.IMPLICATION : toDisjunction,
                BinaryOperators.DISJUNCTION : toImplication,
            }
    
    def applyImplicationReplacement(self, proposition):
        allowedOperators = [BinaryOperators.IMPLICATION, BinaryOperators.DISJUNCTION]
        return self.applyMapping(proposition, allowedOperators)
""" END CLASS """

class DemorgansLaw(Law):
    """ Encodes Demorgan's Law (c.f. https://en.wikipedia.org/wiki/De_Morgan%27s_laws)
    """
    def __init__(self, *args, **kwargs):
        conjunction = [LAWKWORDS.NOTFIRST, BinaryOperators.DISJUNCTION, LAWKWORDS.NOTSECOND + ")"]
        disjunction = [LAWKWORDS.NOTFIRST, BinaryOperators.CONJUNCTION, LAWKWORDS.NOTSECOND + ")"]
        implication = [LAWKWORDS.FIRSTPROP, BinaryOperators.CONJUNCTION, LAWKWORDS.NOTSECOND + ")"]
        self.mapping = {
            BinaryOperators.CONJUNCTION : conjunction,
            BinaryOperators.DISJUNCTION : disjunction,
            BinaryOperators.IMPLICATION : implication
            }    

    def applyDemorgansLaw(self, proposition):
        return self.applyMapping(proposition)
""" END CLASS """

