from z3 import * 
import struct
import sys
from decimal import *



class breakv47:
    def __init__(self,numbers):
        a,b = BitVecs('a b' , 64)
        self.sym_state0 = a 
        self.sym_state1 = b 
        self.solver = Solver()
        self.numbers = numbers
        self.mask = 0xFFFFFFFFFFFFFFFF
        self.a1 = a 
        self.b1 = b 
        self.solve()

        if self.sym_state0: 
            for i in range(len(numbers)):
                (self.next_guess())
            # return to the current value 
            
            print('Success!')    
        else: 
            print('Can not recover!')
            exit()

    def to_double(self,value):
        """
        https://github.com/v8/v8/blob/master/src/base/utils/random-number-generator.h#L111
        """
        double_bits = (value >> 12) | 0x3FF0000000000000
        return struct.unpack('d', struct.pack('<Q', double_bits))[0] - 1

    def from_double(self,dbl):
        """
        https://github.com/v8/v8/blob/master/src/base/utils/random-number-generator.h#L111

        This function acts as the inverse to @to_double. The main difference is that we
        use 0x7fffffffffffffff as our mask as this ensures the result _must_ be not-negative
        but makes no other assumptions about the underlying value.

        That being said, it should be safe to change the flag to 0x3ff...
        """
        return struct.unpack('<Q', struct.pack('d', dbl + 1))[0] & 0x7FFFFFFFFFFFFFFF


    def re_xs128(self):
        
        s1 = self.sym_state0
        s0 = self.sym_state1
        s1 ^= (s1 << 23) 
        s1 ^= LShR(s1, 17)
        s1 ^= s0
        s1 ^= LShR(s0, 26)
        self.sym_state0 = self.sym_state1
        self.sym_state1 = s1

        
        

    def solve( self ):
      
        for i in self.numbers:
            self.re_xs128()
            mantissa = int( i * ( 0x1 << 53 ) )
            self.solver.add(
                ( ( self.sym_state0 + self.sym_state1 )  & 0x1FFFFFFFFFFFFF  ) == (mantissa)  
            )    
        if self.solver.check() == sat: 
            model = self.solver.model()
          
            self.sym_state0 = model[self.a1].as_long()
            self.sym_state1 = model[self.b1].as_long()
        else: self.sym_state0 = None


    def next_guess(self):
        s1 = self.sym_state0 
        s0 = self.sym_state1

        s1 ^= (s1 << 23) & self.mask
        s1 ^= (s1 >> 17) & self.mask
        s1 ^= s0 & self.mask
        s1 ^= (s0 >> 26) & self.mask
        self.sym_state0 = s0 & self.mask
        self.sym_state1 = s1 & self.mask
        return self.to_double( int(( self.sym_state0 + self.sym_state1 ) & self.mask) ) 
       

