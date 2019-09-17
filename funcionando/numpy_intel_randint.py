from numpy import random_intel
# PRNG numpy random_intel

def prng(amount, interval):
    for i in range(amount):
        print(random_intel.randint(interval + 1))

def main():
    interval = 10000
    amount = 100000
    prng(amount, interval)

if __name__ == "__main__":
    main()
