#!/usr/bin/python
#< ----------- Base Classes for all objects used in PyLogic's propositonal logic processing ----------- >


class LogicalConstruct:
    """ Basic construct that represents propositons, logic operators, and all
 processing units """
    rawData = ""
    def __eq__(self, value):
        return self.rawData == value.rawData
    def __str__(self):
        return self.rawData
    def __init__(self, *args, **kwargs):
        if(len(args) > 0):
            self.rawData = args[0]

""" END CLASS """

