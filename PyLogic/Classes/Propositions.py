#!/usr/bin/python
#< ----------- Classes to represent propositions, e.g., "Socrates is a man." ----------- >
from enum import Enum
from BaseClasses import *

class PropTypes(Enum):
    SIMPLE = 0,
    COMPLEX = 1


class Proposition(LogicalConstruct):
    """ Represents an arbitrary proposition; treated as an abstract class, of sorts """

    def __invert__(self):
        """ Shortcut for converting a Proposition to a string.  So ~P == str(P) """
        return self.rawData
    def __and__(self, value):
        """ Shortcut for conjoining two Propositions """
        from Operators import createConjunction
        cp = createConjunction(self,value)
        return cp
    def __or__(self, value):
        """ Shortcut for disjoining (inclusive) two Propositions """
        from Operators import createDisjunctionn
        cp = createDisjunctionn(self,value)
        return cp
    def __gt__(self, value):
        """ Shortcut for createDisjunction(negate(P), Q), where (P,Q) are Propositions """
        from Operators import createImplication
        cp = createImplication(self,value)
        return cp
    def __iter__(self):
        """ Make all propositions iterable so they can be used in iterable manipulations """
        return self
    def __next__(self):
        """ Make all propositions iterable so they can be used in iterable manipulations,
            however each subclass needs to implement what "next" means when iterating *over* a
            proposition, rather than over a *list* of propositions
        """
        pass

    def propType():
        """ Virtual function that each subclass of Proposition must implement as a conceptual 
            shortcut for typeOf(P), where P is an instantiation of a subclass of Proposition 
        """
        raise NotImplementedError()
""" END CLASS"""
class SimpleProp(Proposition):
    """ Represents a single simple proposition in string form; e.g., "Pythons are snakes", which can
        be represented by a single symbol, e.g. P=="Pythons are snakes" 
    """
    def __not___(self):
        """ Shortcut for negating a proposition, e.g., !"My favorite food is cake" ==
            "My favorite food is not cake"
        """
        negate(self)
    def propType():
        """ C.f. propType in the base class Proposition 
        """
        return PropTypes.SIMPLE
""" END CLASS """
class ComplexProp(Proposition):
    """ Represents a single binary proposition, e.g., "2+2=4"=>"1+1=2" or "P OR Q", etc...
    """
    rawData = ""
    secondProp = ""
    operator = ""
    """ Variables: rawData is the first Proposition (of any type, including ComplexProp), and the
                   secondProp is similarly the first Proposition.  The operator is any supported
                   binary operater in propositional logic.
    """
    def __eq__(self, value):
        """ Defines P=>Q == P=>Q and P=>Q != Q=>P, etc...
        """
        #props = [self, value] ITERABLE VERSION BROKEN
        #members = ['rawData', 'operator', 'secondProp']
        #print(getattr(props[0], members[0]))
        #return all([[getattr(x, z) == getattr(y, z) for x, y in props] for z in members])
        return self.rawData == value.rawData and self.operator == value.operator and self.secondProp== value.secondProp

    def __str__(self):
        """ If (P,=>,Q) is a ComplexProp, then str((P,=>,Q)) == "P=>Q"
        """
        return self.rawData+self.operator+self.secondProp
    def __invert__(self):
        """ Need to override the base class' invert as just returning rawData doesn't properly 
            represent the string form of a ComplexProp
        """
        return str(self)
    def __init__(self, *args, **kwargs):
        """ Logic: ComplexProp(P,<op>,Q) needs to properly represent P <op> Q, and we also need
            to account for P or Q being a ComplexProp by using parentheses.
        """
        self.rawData = args[0]
        self.operator= args[1]
        self.secondProp = args[2]
        from Operators import BinaryOperators as b
        if(b.DISJUNCTION in self.rawData or b.CONJUNCTION in self.rawData or b.IMPLICATION in self.rawData):
            self.rawData = "("+self.rawData+")"
        if(b.DISJUNCTION in self.secondProp or b.CONJUNCTION in self.secondProp or b.IMPLICATION in self.secondProp):
            self.secondProp = "("+self.secondProp+")"
    def propType():
        """ C.f. propType in the base class Proposition 
        """
        return PropTypes.COMPLEX

"""END CLASS"""
