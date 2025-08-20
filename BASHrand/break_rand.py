from z3 import * 
from Bashrand import Bash_Random
from Z3break import Z3_Random

k = BitVec('x',32)
rand = Bash_Random(2006,40)
rand_sym = Z3_Random(k,40)

s = Solver()

for i in range(4):
    s.add( rand.brand() == rand_sym.brand() )

assert s.check() == sat 


m = s.model()

seed = m[k].as_long()
seed = int (seed)

breakrand = Bash_Random(seed,40)

for i in range(4):
    breakrand.brand()

assert breakrand.brand() == rand.brand()