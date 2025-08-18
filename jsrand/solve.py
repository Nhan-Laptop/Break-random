from z3 import * 
import struct
import sys
from decimal import *




def to_double(value):
    """
    https://github.com/v8/v8/blob/master/src/base/utils/random-number-generator.h#L111
    """
    double_bits = (value >> 12) | 0x3FF0000000000000
    return struct.unpack('d', struct.pack('<Q', double_bits))[0] - 1

def from_double(dbl):
    """
    https://github.com/v8/v8/blob/master/src/base/utils/random-number-generator.h#L111

    This function acts as the inverse to @to_double. The main difference is that we
    use 0x7fffffffffffffff as our mask as this ensures the result _must_ be not-negative
    but makes no other assumptions about the underlying value.

    That being said, it should be safe to change the flag to 0x3ff...
    """
    return struct.unpack('<Q', struct.pack('d', dbl + 1))[0] & 0x7FFFFFFFFFFFFFFF


def re_xs128(sym_state0, sym_state1):
    
    s1 = sym_state0
    s0 = sym_state1
    s1 ^= (s1 << 23) 
    s1 ^= LShR(s1, 17)
    s1 ^= s0
    s1 ^= LShR(s0, 26)
    sym_state0 = sym_state1
    sym_state1 = s1
    

    return sym_state0, sym_state1

def solve( number ):
    a,b = BitVecs('a b',64)
    s = Solver()

    mask = 0xFFFFFFFFFFFFFFFF
    for i in number:
        a,b = re_xs128(a,b)
        mantissa = from_double(i)
        mantissa &= ((1 << 52) - 1)
        s.add(
            ( LShR( a, 12) ) == mantissa  
        )    
    print(s.check())
    if s.check() == sat: 
        model = s.model()
        a,b = BitVecs('a b',64)
        a = model[a].as_long()
        b = model[b].as_long()
        return a,b
    
def next_guess(sym_state0,sym_state1):
    s1 = sym_state0
    s0 = sym_state1
    result = sym_state0
    mask = 0xFFFFFFFFFFFFFFFF
    s1 ^= (s1 << 23) & mask
    s1 ^= (s1 >> 17) & mask
    s1 ^= s0 & mask
    s1 ^= (s0 >> 26) & mask
    sym_state0 = sym_state1
    sym_state1 = s1

    return to_double(result)

numbers =  [
  0.9311600617849973,
  0.3551442693830502,
  0.7923158995678377,
  0.787777942408997,
  0.376372264303491,
  # 0.23137147109312428
]

# browser chrome
a,b = solve(numbers[::-1])
print(next_guess(a,b))