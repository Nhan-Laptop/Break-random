from z3 import * 
import time
import os 
import struct 

class Z3_Random:

    BASH_RAND32_MAX = 0x7fffffff
    BASH_RAND_MAX = 0x7fff
    m = 2147483647
    a = 16807 
    q = 127773
    r = 2836 
    urandfd = -1

    def __init__(self, seed = None,level = None ):

        self.rseed = seed 
        self.rseed32 = 1073741823
        self.last_random_value = 0
        self.last_rand32 = 0
        self.shell_compatibility_level = level

    
    def intrand32(self,last):
        last = If(last == 0, BitVecVal(123459876, 32), last)
        ret = last
        h = UDiv(last, BitVecVal(self.q, 32))
        l = URem(last, BitVecVal(self.q, 32))
        t = BitVecVal(self.a, 32) * l - BitVecVal(self.r, 32) * h
        return If(t < 0, t + BitVecVal(self.m, 32), t)
    
    def genseed(self):
        tv   = time.time()
        sec  = int(tv)
        usec = int((tv-sec)*1_000_000)

        pid = os.getpid()
        ppid = os.getppid()
        uid = os.getuid() if hasattr(os, "getuid") else 1000

        iv = id(self.genseed) & 0xffffffff
        return sec ^ usec ^ pid ^ ppid ^ uid ^ iv
    
    def brand(self):
        self.rseed = self.intrand32(self.rseed)
        if self.shell_compatibility_level > 50:
            ret = LShR(self.rseed, 16) ^ (self.rseed & BitVecVal(0xffff,32))
        else:
            ret = self.rseed
        return ret & BitVecVal(self.BASH_RAND_MAX,32)
    
    def sbrand(self,seed):
        self.rseed = seed
        self.last_random_value = 0

    def seedrand(self):
        self.sbrand(self.genseed())
    
    def brand32(self):
        self.rseed32 = self.intrand32(self.rseed32)
        return self.rseed32 & self.BASH_RAND32_MAX

    def sbrand32(self, seed):
        self.rseed32 = seed
        self.last_rand32 = seed
    
    def seedrand32(self):
        self.sbrand32(self.genseed())

    def perturb_rand32(self):
        self.rseed32 ^= self.genseed()

    def get_urandom32(self):
        try:
            data = os.urandom(4)
            ret, = struct.unpack("I", data)
            self.last_rand32 = ret
            return ret
        except Exception:
            self.perturb_rand32()
            ret = self.brand32()
            while ret == self.last_rand32:
                ret = self.brand32()
            self.last_rand32 = ret
            return ret