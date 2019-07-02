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
            ant = ant.replace(LAWKWORDS.SECONDPROP, proposition.secondProp)
            operator = result[1]
            con = result[2].replace(LAWKWORDS.FIRSTPROP, proposition.rawData)
            con = con.replace(LAWKWORDS.SECONDPROP, proposition.secondProp)
            returnProp = ComplexProp(ant, operator, con)
        return returnProp
""" END CLASS """

class IMPLReplacement(Law):
    """ Encodes (P => Q) <==> (~P => Q)
    """

    def __init__(self, *args, **kwargs):
        toDISJUNCT = [LAWKWORDS.NOTFIRST, BinaryOperators.DISJUNCT, LAWKWORDS.SECONDPROP]
        toIMPL = [LAWKWORDS.NOTFIRST, BinaryOperators.IMPL, LAWKWORDS.SECONDPROP]
        mapping = {
                BinaryOperators.IMPL : toDISJUNCT,
                BinaryOperators.DISJUNCT : toIMPL,
            }
    
    def applyIMPLReplacement(self, proposition):
        allowedOperators = [BinaryOperators.IMPL, BinaryOperators.DISJUNCT]
        return self.applyMapping(proposition, allowedOperators)
""" END CLASS """

class DemorgansLaw(Law):
    """ Encodes Demorgan's Law (c.f. https://en.wikipedia.org/wiki/De_Morgan%27s_laws)
    """
    def __init__(self, *args, **kwargs):
        CONJUCT = [LAWKWORDS.NOTFIRST, BinaryOperators.DISJUNCT, LAWKWORDS.NOTSECOND]
        DISJUNCT = [LAWKWORDS.NOTFIRST, BinaryOperators.CONJUCT, LAWKWORDS.NOTSECOND]
        IMPL = [LAWKWORDS.FIRSTPROP, BinaryOperators.CONJUCT, LAWKWORDS.NOTSECOND]
        """TODO: Decide which common form of xor to use:
           (1) (P AND Q) OR (~P AND ~Q)
                        v.s.
           (2) (P AND ~Q) OR (~P AND Q)
           (in order to figure out a way to toggle between them so the user can select a preferred
           form)
        """
        #xor is a little more complicated syntactically so we'll build it up in stages
        firstDisjunct = "(" + LAWKWORDS.FIRSTPROP + BinaryOperators.CONJUCT + LAWKWORDS.SECONDPROP + ")"
        secondDisjunct = "(" + LAWKWORDS.NOTFIRST + BinaryOperators.CONJUCT + LAWKWORDS.NOTSECOND + ")"
        XOR = [firstDisjunct, BinaryOperators.DISJUNCT, secondDisjunct]
        self.mapping = {
            BinaryOperators.CONJUCT : CONJUCT,
            BinaryOperators.DISJUNCT : DISJUNCT,
            BinaryOperators.IMPL : IMPL,
            BinaryOperators.XOR : XOR
            }    

    def applyDemorgansLaw(self, proposition):
        return self.applyMapping(proposition)
""" END CLASS """

