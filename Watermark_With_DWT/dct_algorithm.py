import numpy as np
from math import sqrt, cos, floor, pi
import cv2

BLOCK_WIDTH = 8
BLOCK_HEIGHT = 8
N = 8
def dct(array):	
	dct_rs = np.ones((BLOCK_WIDTH,BLOCK_HEIGHT))
	for u in range(N):
		for v in range(N):
			if u == 0:
				cu = 1 / sqrt(N)
			else: 
				cu = sqrt(2) / sqrt(N)
			if v == 0:
				cv = 1 / sqrt(N)
			else:
				cv = sqrt(2) / sqrt(N) 

			sum = 0
			for x in range(N):
				for y in range(N):
					dct1 = array[x][y] * cos((2 * x + 1) * u * pi / (2 * BLOCK_WIDTH)) * cos((2 * y + 1) * v * pi / (2 * BLOCK_HEIGHT))
					sum += np.float32(dct1)
			dct_rs[u][v] = cu * cv * sum
	return dct_rs
def idct(array):
	dct_rs = np.ones((BLOCK_WIDTH,BLOCK_HEIGHT))
	for x in range(N):
		for y in range(N):
			sum = 0
			for u in range(N):
				for v in range(N):
					if u == 0:
						cu = 1 / sqrt(N)
					else: 
						cu = sqrt(2) / sqrt(N)
					if v == 0:
						cv = 1 / sqrt(N)
					else:
						cv = sqrt(2) / sqrt(N) 
					dct1 = cu * cv * array[u][v] * cos((2 * x + 1) * u * pi / (2 * N)) * cos((2 * y + 1) * v * pi / (2 * N))
					sum += np.float32(dct1)
			dct_rs[x][y] = sum
	return dct_rs


# if __name__ == "__main__":
# 	array = [	[16,  11,  10,  16,  24,  40,  51,  61],
# 				[12,  12,  14,  19,  26,  58,  60,  55],
# 				[14,  13,  16,  24,  40,  57,  69,  56],
# 				[14,  17,  22,  29,  51,  87,  80,  62],
# 				[18,  22,  37,  56,  68, 109, 103,  77],
# 				[24,  35,  55,  64,  81, 104, 113,  92],
# 				[49,  64,  78,  87, 103, 121, 120, 101],
# 				[72,  92,  95,  98, 112, 100, 103,  99] ]
# 	array = dct(array)
# 	#for a in range(8):
# 	#	for b in range(8):
# 	#		print("{:.16f}".format(array[a][b]))
# 	print(array)
# 	print("===============")
# 	array_idct = idct(array)
# 	print(array_idct)

	