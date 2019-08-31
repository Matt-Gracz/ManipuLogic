#!/usr/bin/python
#< ----------- Encodes the laws of Propositional Logic ----------- >
from BaseClasses import *
from Operators import *
from Propositions import *
from enum import Enum

class LawKWords:
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
            ant = result[0].replace(LawKWords.FIRSTPROP, proposition.rawData)
            ant = ant.replace(LawKWords.SECONDPROP, proposition.secondProp)
            operator = result[1]
            con = result[2].replace(LawKWords.FIRSTPROP, proposition.rawData)
            con = con.replace(LawKWords.SECONDPROP, proposition.secondProp)
            returnProp = ComplexProp(ant, operator, con)
        return returnProp
""" END CLASS """

class IMPLReplacement(Law):
    """ Encodes (P => Q) <==> (~P \/ Q)
    """

    def __init__(self, *args, **kwargs):
        toDISJUNCT = [LawKWords.NOTFIRST, OpStrings.DISJUNCT, LawKWords.SECONDPROP]
        toIMPL = [LawKWords.NOTFIRST, OpStrings.IMPL, LawKWords.SECONDPROP]
        self.mapping = {
                OpStrings.IMPL : toDISJUNCT,
                OpStrings.DISJUNCT : toIMPL,
            }
    
    def applyIMPLReplacement(self, proposition):
        allowedOperators = [OpStrings.IMPL, OpStrings.DISJUNCT]
        return self.applyMapping(proposition, allowedOperators)
""" END CLASS """

class DemorgansLaw(Law):
    """ Encodes Demorgan's Law (c.f. https://en.wikipedia.org/wiki/De_Morgan%27s_laws)
    """
    def __init__(self, *args, **kwargs):
        CONJUCT = [LawKWords.NOTFIRST, OpStrings.DISJUNCT, LawKWords.NOTSECOND]
        DISJUNCT = [LawKWords.NOTFIRST, OpStrings.CONJUCT, LawKWords.NOTSECOND]
        IMPL = [LawKWords.FIRSTPROP, OpStrings.CONJUCT, LawKWords.NOTSECOND]
        """TODO: Decide which common form of xor to use:
           (1) (P AND Q) OR (~P AND ~Q)
                        v.s.
           (2) (P AND ~Q) OR (~P AND Q)
           (in order to figure out a way to toggle between them so the user can select a preferred
           form)
        """
        #xor is a little more complicated syntactically so we'll build it up in stages
        firstDisjunct = "(" + LawKWords.FIRSTPROP + OpStrings.CONJUCT + LawKWords.SECONDPROP + ")"
        secondDisjunct = "(" + LawKWords.NOTFIRST + OpStrings.CONJUCT + LawKWords.NOTSECOND + ")"
        XOR = [firstDisjunct, OpStrings.DISJUNCT, secondDisjunct]
        self.mapping = {
            OpStrings.CONJUCT : CONJUCT,
            OpStrings.DISJUNCT : DISJUNCT,
            OpStrings.IMPL : IMPL,
            OpStrings.XOR : XOR
            }    

    def applyDemorgansLaw(self, proposition):
        return self.applyMapping(proposition)
""" END CLASS """

