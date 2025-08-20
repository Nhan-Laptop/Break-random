from z3 import * 
from rand import *
from rng import *


k = [BitVec(f"k_{i}",64)for i in range(RNG_LEN)]

src = RngSource(k)
sym_ran = new(src)

rand = new_source(2006)
random = new(rand)
s = Solver()
for i in range(700):
    """
    We need at least 608 polynomials to recover 607 states
    """
    tmp = random.uint64()
    cmp = sym_ran.uint64()
    s.add( tmp== cmp)


assert s.check() == sat 


m = s.model()

k = [(m[ki].as_long()) for ki in k]

src = RngSource(k)
sym_ran = new(src)

for i in range(700):
    sym_ran.uint64()

assert sym_ran.uint64() == random.uint64()