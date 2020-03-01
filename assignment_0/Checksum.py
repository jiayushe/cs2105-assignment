import sys
import zlib

n = sys.argv[1]

with open(n, "rb") as f:
  bytes = f.read()
checksum = zlib.crc32(bytes)

print(checksum)
