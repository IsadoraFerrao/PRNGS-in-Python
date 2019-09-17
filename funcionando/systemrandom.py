import random
n = 100000

# PRNG System Random

for i in range(n):
	print(random.SystemRandom().randint(0,10000))
