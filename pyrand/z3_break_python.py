from z3 import * 

class Break_rand:
    
    def __init__(self):

        self.output = []

    def untemper(self,output):
        y1 = BitVec('y1', 32)
        y2 = BitVec('y2', 32)
        y3 = BitVec('y3', 32)
        y4 = BitVec('y4', 32)
        y = BitVecVal(output, 32)

        s = Solver()
        equations = [
            y2 == y1 ^ (LShR(y1, 11)),
            y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
            y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
            y == y4 ^ (LShR(y4, 18))
        ]
        s.add(equations)
        s.check()
        return s.model()[y1].as_long()
    
    def recover_state_mt(self):
        assert len(self.output)>= 624, "Can not recover state!"
        state = tuple(self.untemper(n)& 0xffffffff  for n in self.output[:624])
        return (3, state + (624,), None)
    
    def submit(self,n):
        self.output.append(n)

"""
Test function
"""
from random import *

rng = Random()
tmp = []
breakrand = Break_rand()

for i in range(624):
    breakrand.submit(rng.getrandbits(32))

Ran = Random()
Ran.setstate(breakrand.recover_state_mt())

assert Ran.getrandbits(32)==rng.getrandbits(32)