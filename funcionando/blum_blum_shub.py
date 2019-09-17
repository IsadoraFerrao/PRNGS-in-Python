#!/usr/bin/env python2.7
import random

def decompose(n):
   exponentOfTwo = 0

   while n % 2 == 0:
      n = n/2
      exponentOfTwo += 1

   return exponentOfTwo, n

def isWitness(possibleWitness, p, exponent, remainder):
   possibleWitness = pow(possibleWitness, remainder, p)

   if possibleWitness == 1 or possibleWitness == p - 1:
      return False

   for _ in range(exponent):
      possibleWitness = pow(possibleWitness, 2, p)

      if possibleWitness == p - 1:
         return False

   return True

def probablyPrime(p, accuracy=100):
   if p == 2 or p == 3: return True
   if p < 2: return False

   exponent, remainder = decompose(p - 1)

   for _ in range(accuracy):
      possibleWitness = random.randint(2, p - 2)
      if isWitness(possibleWitness, p, exponent, remainder):
         return False

   return True


def goodPrime(p):
    return p % 4 == 3 and probablyPrime(p, accuracy=100)

def findGoodPrime(numBits=512):
    candidate = 1
    while not goodPrime(candidate):
        candidate = random.getrandbits(numBits)
    return candidate

def makeModulus():
    return findGoodPrime() * findGoodPrime()

def parity(n):
    return sum(int(x) for x in bin(n)[2:]) % 2


class BlumBlumShub(object):
    def __init__(self, seed=None):
        self.modulus = makeModulus()
        self.state = seed if seed is not None else random.randint(2, self.modulus - 1)
        self.state = self.state % self.modulus

    def seed(self, seed):
        self.state = seed

    def bitstream(self):
        while True:
            yield parity(self.state)
            self.state = pow(self.state, 2, self.modulus)

    def bits(self, n=20):
        outputBits = ''
        for bit in self.bitstream():
            outputBits += str(bit)
            if len(outputBits) == n:
                break

        return outputBits

def main():
    generator = BlumBlumShub()
    for i in range(100000):
        print(int(generator.bits(17), 2)% 10000)

if __name__ == "__main__":
    main()
