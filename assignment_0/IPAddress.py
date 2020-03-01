import sys

n = sys.argv[1]

for i in range(0, 3):
  print(int(n[i * 8 : (i + 1) * 8], 2), end = '.')

print(int(n[24 : 32], 2))
