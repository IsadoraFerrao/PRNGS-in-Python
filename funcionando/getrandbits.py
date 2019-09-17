import random
n = 100000
for i in range(n):
	print(random.getrandbits(32) % 10000)
