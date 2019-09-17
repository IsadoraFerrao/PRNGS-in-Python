#!usr/bin/env python3
from numpy import random

# PRNG numpy random

def prng(amount, interval):
    for i in range(amount):
        print(random.randint(interval + 1))

def main():
    interval = 10000
    amount = 100000
    prng(amount, interval)

if __name__ == "__main__":
    main()
