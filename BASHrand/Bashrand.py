import time
import os 
import struct 

class Bash_Random:

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
        """
        /* Returns a 32-bit pseudo-random number. */
        """
        if last == 0: last = 123459876 
        ret = last
        h = ret // self.q 
        l = ret % self.q
        t = self.a * l - self.r * h 
        if t < 0 :
            t += self.m
        return t 
    
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
        """
        /* Returns a pseudo-random number between 0 and 32767. */
        """
        self.rseed = self.intrand32(self.rseed)
        if self.shell_compatibility_level > 50:
            ret = (self.rseed >> 16) ^ (self.rseed & 0xffff)
        else:
            ret = self.rseed
        return ret & self.BASH_RAND_MAX
    
    def sbrand(self,seed):
        """
        /* Set the random number generator seed to SEED. */
        """
        self.rseed = seed
        self.last_random_value = 0

    def seedrand(self):
        self.sbrand(self.genseed())
    
    def brand32(self):
        """
        /* Returns a 32-bit pseudo-random number between 0 and 4294967295. */
        """
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