from utils import *
from prime_generator import *

class NPRSA:

    def __init__(self, CONFIG):
        self.nbits = CONFIG["nbits"]
        self.nprimes = CONFIG["nprimes"]
        self.initialized = False
        self.pl = []
        self.pg = CONFIG["prime_generator"]
        self.mt = CONFIG["multiplier"]
        self.tt = CONFIG["totient"]
        self.N = None
        self.T = None
        self.publicKey = None
        self.privateKey = None

    def __str__(self):
        return "<nbits:{nbits}, nprimes:{nprimes}, N:{N}, T:{T}, publicKey:{publicKey}>".format(
            nbits = self.nbits, nprimes = self.nprimes, N = self.N, T = self.T, publicKey = self.publicKey
        )

    def initialize(self):
        if self.initialized:
            return True
        self.pl = self.pg(self.nprimes, self.nbits)
        self.N = self.mt(self.pl)
        self.T = self.tt(self.pl)
        self.publicKey = (publicKeyComponent(1, self.T, self.T), self.N)
        self.privateKey = (privateKeyComponent(self.publicKey[0], 1, self.T, self.T), self.N)
        if self.N != None and self.T != None and self.publicKey[0] != -1 and self.privateKey[0] != -1:
            self.initialized = True
            return True
        self.initialized = False
        return False
    
    def encrypt(self, plaintext):
        return pow(plaintext, self.publicKey[0], self.publicKey[1])

    def decrypt(self, ciphertext):
        return pow(ciphertext, self.privateKey[0], self.privateKey[1])

    def getPublicKey(self):
        return self.publicKey
