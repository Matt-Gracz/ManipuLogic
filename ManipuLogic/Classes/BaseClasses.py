#!/usr/bin/python
#< ----------- Base Classes for all objects used in ManipuLogic's propositonal logic processing ----------- >


class LogicalConstruct:
    """ Basic construct that represents propositons, logic operators, and all
        processing units 
    """
    rawData = ""
    def __eq__(self, value):
        return self.rawData == value.rawData
    def __str__(self):
        return self.rawData
    def __init__(self, *args, **kwargs):
        if(len(args) > 0):
            self.rawData = args[0]
""" END CLASS """
class Proposition(LogicalConstruct):
    """ Any proposition in any type of logic (e.g., propositional, first-order, etc...) """
    propType = ""
""" END CLASS """

class Operator(LogicalConstruct):
    """ Any operator in any type of logic (e.g., CONJUCT, for-all(x) etc...) """
""" END CLASS """

