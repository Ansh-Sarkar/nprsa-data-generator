import math

def multiplier(primes):
    prod = 1
    for prime in primes: prod *= prime
    return prod

def totient(primes):
    tot = 1
    for prime in primes: tot *= (prime - 1)
    return tot

# a < p < b
def publicKeyComponent(a, b, fn):
    for p in range(b - a, a, -1):
        if math.gcd(p, fn) == 1:
            return p
    return -1

# a < d < b
def privateKeyComponent(publicKey, a, b, fn):
    for d in range(b - 1, a, -1):
        if (publicKey * d) % fn == 1:
            return d
    return -1

# generate ciphertext from plaintext message
def encrypt(publicKey, plaintext):
    return pow(plaintext, publicKey[0], publicKey[1])

# generate plaintext from ciphertext message
def decrypt(privateKey, ciphertext):
    return pow(ciphertext, privateKey[0], privateKey[1])