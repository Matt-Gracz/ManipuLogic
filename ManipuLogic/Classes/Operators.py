#!/usr/bin/python
from Propositions import ComplexProp, SimpleProp, PropTypes
from BaseClasses import Operator

#< ----------- Functions to represent operations/operators over the domain of propositions,
#              e.g., negation or material IMPL ----------- >

class OpStrings():
    DISJUNCT = " OR "
    CONJUCT = " AND "
    IMPL = " => "
    XOR = " (+) "
    opList = [DISJUNCT, CONJUCT, IMPL, XOR]

class BinaryOperator(Operator):
    """ Encodes all binary operators in propositional logic, e.g., conjunction, implication, 
        etc... 
    """

    def applyBinaryOperator(self, antecdent, operator, consequent):
        """ Creates a generic ComplexProp of the form (antecdent, operator, consequent) """
        cp = ComplexProp(~antecdent, operator, ~consequent)
        return cp

    def disjoin(self, antecedent, consequent):
        """ Creates a ComplexProp of the form (antecdent, OR, consequent) """
        cp = self.applyBinaryOperator(antecedent, OpStrings.DISJUNCT, consequent)
        return cp

    def conjoin(self, antecedent, consequent):
        """ Creates a ComplexProp of the form (antecdent, AND, consequent) """
        cp = self.applyBinaryOperator(antecedent, OpStrings.CONJUCT, consequent)
        return cp

    def imply(self, antecedent, consequent):
        """ Creates a ComplexProp of the form (antecdent, =>, consequent) """
        cp = self.applyBinaryOperator(antecedent, OpStrings.IMPL, consequent)
        return cp

    def xor(self, antecdent, consequent):
        """ Creates a ComplexProp of the form (antecdent (+) conseqent) """
        cp = self.applyBinaryOperator(antecdent, OpStrings.XOR, consequent)
        return cp

class UnaryOperator(Operator):
    """ Encodes all unary operators in propositional logic, e.g., negation. """

    def negate(self, proposition):
        """ Applies the unary operation of negation to an arbitrary instance of any subclass
            of Proposition.
        """
        if(proposition.getPropType() == PropTypes.SIMPLE):
            newProp = SimpleProp()
            newProp.rawData = "~"+proposition.rawData
        elif(proposition.getPropType() == PropTypes.COMPLEX):
            """ If we're negating a complex prop, i.e., a proposition with an infixed binary
                operator, then first we need to check if the operator is an implication. If so,
                then we need to convert it to a disjunction.  Secondly, once that's done, we'll be
                sure that the infixed operator is a disjunction or conjunction, so we'll apply
                DeMorgan's law and end up with our final simplest negated form to return to the 
                caller.
            """
            newProp = ComplexProp(proposition.rawData, proposition.operator, proposition.secondProp)
            if(newProp.operator == OpStrings.IMPL):
                from Laws import IMPLReplacement
                IR = IMPLReplacement()
                newProp = IR.applyIMPLReplacement(newProp)
            from Laws import DemorgansLaw
            DL = DemorgansLaw()
            newProp = DL.applyDemorgansLaw(newProp)
        else:
            raise NotImplementedError()

        #check for double negation
        if(newProp.rawData[0:2] == "~~"):
            newProp.rawData = newProp.rawData[2:]
        if(newProp.getPropType() == PropTypes.COMPLEX):            
            if(newProp.secondProp[0:2] == "~~"):
                newProp.secondProp = newProp.secondProp[2:]

        return newProp

