import os

n = 100000

for i in range(n):
	print(int.from_bytes(os.urandom(2), byteorder='little') % 10000)
