#!/usr/bin/python
from Propositions import ComplexProp, SimpleProp, PropTypes
from enum import Enum
#< ----------- Functions to represent operations/operators over the domain of propositions,
#              e.g., negation or material implication ----------- >

class BinaryOperators:
    DISJUNCTION = " OR "
    CONJUNCTION = " AND "
    IMPLICATION = " => "

def negate(proposition):
    """ Applies the unary operation of negation to an arbitrary instance of any subclass
        of Proposition.
    """
    if(proposition.propType() == PropTypes.SIMPLE):
        proposition.rawData = "~"+proposition.rawData
    elif(proposition.propType() == PropTypes.COMPLEX):
        proposition.rawData = "~"+"("+proposition.rawData
        proposition.secondProp = proposition.secondProp+")"
    else:
        raise NotImplementedError()
    return proposition

def createBinaryOperator(antecdent, operator, consequent):
    """ Creates a generic ComplexProp of the form (antecdent, operator, consequent)
    """
    cp = ComplexProp(~antecdent, operator, ~consequent)
    return cp

def createDisjunctionn(antecedent, consequent):
    """ Creates a  ComplexProp of the form (antecdent, OR, consequent)
    """
    cp = createBinaryOperator(antecedent, BinaryOperators.DISJUNCTION, consequent)
    return cp

def createConjunction(antecedent, consequent):
    """ Creates a  ComplexProp of the form (antecdent, AND, consequent)
    """
    cp = createBinaryOperator(antecedent, BinaryOperators.CONJUNCTION, consequent)
    return cp

def createImplication(antecedent, consequent):
    """ Creates a  ComplexProp of the form (antecdent, =>, consequent)
    """
    cp = createBinaryOperator(antecedent, BinaryOperators.IMPLICATION, consequent)
    return cp


