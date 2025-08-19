from z3 import * 
import struct
import sys
from decimal import *
from v8rand import breakv8
from v47rand import breakv47
from mathrandom import MathRandom

type = "v8"

Rand = MathRandom()
numbers = [Rand.next() for i in range(4)]

if type == "v8":

    cracker = breakv8(numbers)
    assert cracker.next_guess()[1] == Rand.next()
    assert cracker.next_guess()[1] == Rand.next()

else:
    cracker = breakv47(numbers)

    print(cracker.next_guess()) 
