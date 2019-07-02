#!/usr/bin/python
#< ----------- Starts the ManipuLogic program up ----------- >

""" Program-level TODOs:
    1.) Check all comments for clarity
    2.) Create CLI interation
    3.) Create GUI interaction
    4.) Refactor such that classes, functions, data, and control flow
        are abstracted away to account for 1st order logic.
"""

import sys
sys.path.append('Classes')
#from BaseClasses import *
from Propositions import *
#from Operators import *
#from Laws import *

#p = SimpleProp("Socrates is a man.")
#q = SimpleProp("2 + 2 = 5")
#cp = p & q | p > p | q
#cp2 = p & q
#cp2 = cp2 | p > p | q
#cp2 = -cp

p = SimpleProp("P")
q = SimpleProp("Q")
cp = p > q
cp = cp & q
cp2 = -cp

print("CP " + ~cp)
print("CP2 " + ~cp2)
