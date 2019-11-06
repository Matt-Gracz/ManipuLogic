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
    pass

class ReplacementLaw(Law):
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

class IMPLReplacement(ReplacementLaw):
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

class XorReplacement(ReplacementLaw):
    """ Encodes (P (+) Q) <==> (~P /\ Q) \/ (P /\ ~Q)
    """

    #Xor replacement is always the same so we can hard-code it inline for
    #performance considerations rather than call applyMapping
    def __init__(self, *args, **kwargs):
        pass
    
    def applyXorReplacement(self, proposition):
        #allowedOperators = [OpStrings.XOR] legacy/deprecated
        if proposition.operator != OpStrings.XOR:
            return proposition
        dis = OpStrings.DISJUNCT
        oldRawData = proposition.rawData
        oldSecondProp = proposition.secondProp
        newRawData = "(~" + oldRawData + dis + oldSecondProp + ")"
        newOp = OpStrings.CONJUNCT
        newSecondProp = "(" + oldRawData + dis + "~" + oldSecondProp + ")"
        returnProp = ComplexProp(newRawData, newOp, newSecondProp)
        return returnProp
        
""" END CLASS """


class DemorgansLaw(ReplacementLaw):
    """ Encodes Demorgan's Law (c.f. https://en.wikipedia.org/wiki/De_Morgan%27s_laws)
    """
    def __init__(self, *args, **kwargs):
        CONJUNCT = [LawKWords.NOTFIRST, OpStrings.DISJUNCT, LawKWords.NOTSECOND]
        DISJUNCT = [LawKWords.NOTFIRST, OpStrings.CONJUNCT, LawKWords.NOTSECOND]
        """TODO: Decide which common form of xor to use:
           (1) (P AND Q) OR (~P AND ~Q)
                        v.s.
           (2) (P AND ~Q) OR (~P AND Q)
           (in order to figure out a way to toggle between them so the user can select a preferred
           form)
        """
        #xor is a little more complicated syntactically so we'll build it up in stages
        firstDisjunct = "(" + LawKWords.FIRSTPROP + OpStrings.CONJUNCT + LawKWords.SECONDPROP + ")"
        secondDisjunct = "(" + LawKWords.NOTFIRST + OpStrings.CONJUNCT + LawKWords.NOTSECOND + ")"
        XOR = [firstDisjunct, OpStrings.DISJUNCT, secondDisjunct]
        self.mapping = {
            OpStrings.CONJUNCT : CONJUNCT,
            OpStrings.DISJUNCT : DISJUNCT,
            OpStrings.XOR : XOR
            }    

    def applyDemorgansLaw(self, proposition):
        allowedOperators = [OpStrings.CONJUNCT, OpStrings.DISJUNCT, OpStrings.XOR]
        return self.applyMapping(proposition)
""" END CLASS """

class Distributive(Law): #TODO
    """ Encodes an abstract law of distribution across arbitrary binary operator combinations e.g.,
        (P \/ Q) /\ R <==> (P \/ R) /\ (Q \/ R)
    """

    def __init__(self, *args, **kwargs):
        toDISJUNCT = [LawKWords.NOTFIRST, OpStrings.DISJUNCT, LawKWords.SECONDPROP]
        toIMPL = [LawKWords.NOTFIRST, OpStrings.IMPL, LawKWords.SECONDPROP]
        self.mapping = {
                OpStrings.IMPL : toDISJUNCT,
                OpStrings.DISJUNCT : toIMPL,
            }

    #experimental functions; pull this out to be more general if it ends up working
    def detectEmbeddedProps(self, complexProp):
        #first off, we only can embed in complex props
        if complexProp.propType is not PropTypes.COMPLEX:
            return [False, False]
        #non-embedded props look like:
        #P OP1 Q
        #embedded props look like:
        #1: (P OP1 Q) OP2 R
        #2: P OP1 (Q OP2 R)
        #3: (P OP1 Q) OP2 (R OP3 W)
        #So it's sufficient to just check for a parens in either rawData or secondProp
        yesRawData = "(" in complexProp.rawData or ")" in complexProp.rawData
        yesSecondProp = "(" in complexProp.secondProp or ")" in complexProp.secondProp
        return [yesRawData, yesSecondProp]
    def splitEmbeddedComplexProp(data):
        #we have to find the main connector/operator in the embedded prop.  Note we can't
        #use str.split because the LHS of the embedded prop itself might contain that
        #same operator, which would cause the resultant call to str.split to parse into
        #more than 3 strs (we ultimately want [LHS, OP, RHS] to create our new ComplexProp
        #from)
        #case 1: (SIMPLE OP SIMPLE)
        #case 2: (SIMPLE OP (COMPLEX))
        #case 3: ((COMPLEX) OP SIMPLE)
        #case 4: ((COMPLEX) OP (COMPLEX))
        
        #pre-processing: strip out 
        
        
        pass
    def extractEmbeddedProps(self, complexProp):
        from Operators import OpStrings
        operators = [op for op in OpStrings.opList]
        embedded = self.detectEmbeddedProps(complexProp)
        prop1 = None
        prop2 = None
        data = ""
        #LHS
        if embedded[0]:
            data = complexProp.rawData
            firstOpIndeces = {}
            for op in operators:
                firstOpIndeces[data.find(op)] = op
            strippedIndeces = [x for x in firstOpIndeces.keys() if x >= 0]

            #alternate method: find all op indeces
            #tested in cmd line; seems to work; 11/6/19
            tempData = data
            allOpsWithIndeces = {}
            stop = False
            while(not stop):
                lowestOpIndex = len(tempData)
                tempOpIndeces = {}
                for op in operators:
                    index = tempData.find(op)
                    if(index > 0):
                        tempOpIndeces[index] = op
                        lowestOpIndex = min(lowestOpIndex, index)
                if len(tempOpIndeces.keys()) > 0:
                    allOpsWithIndeces[lowestOpIndex+(len(data)-len(tempData))] = tempOpIndeces[lowestOpIndex]
                    tempData = tempData[lowestOpIndex+1:]
                else: #no more operators left
                    stop = True

            sortedIndeces = sorted(strippedIndices)
            #simple on LHS of embeddedprop
            if "(" != data[0]:
                firstOp = sortedIndeces[0]
                prop1 = SimpleProp(data.split(firstOp)[0])
            else: #complex on LHS of embeddedProp
                #we have to find the main connector/operator in the embedded prop.  Note we can't
                #use str.split because the LHS of the embedded prop itself might contain that
                #same operator, which would cause the resultant call to str.split to parse into
                #more than 3 strs (we ultimately want [LHS, OP, RHS] to create our new ComplexProp
                #from)
                #case 1: sos (SIMPLE OP SIMPLE)
                #case 2: soc (SIMPLE OP (COMPLEX))
                #case 3: cos ((COMPLEX) OP SIMPLE)
                #case 4: coc ((COMPLEX) OP (COMPLEX))
        
                #pre-processing: remove leading and trailing parens
                data = data[1:-1]
                propData = []
                #case 1: sos
                if len(sortedIndeces) == 1:
                    propData = data.split(firstOp)
                    prop1 = ComplexProp(data[0], firstOp, data[1])


    def applyDistribution(self, proposition):
        #PROBLEM; need to search for embedded propositions!
        #first hacky stab at solving this problem is below
        
        #first off, we only can distribute over complex props
        if proposition.propType is not PropTypes.COMPLEX:
            return proposition

        #unravel a proposition if it has a bunch of double negations to cancel out
        from Operators import UnaryOperator
        uo = UnaryOperator()
        uo.applyDoubleNegation(proposition)

        #once we're in normal form we'll build up the strings to replace
        
        
        
""" END CLASS """