import sys

while True:
  data = sys.stdin.buffer.read1(1)

  if len(data) == 0:
    break

  size = 0

  while data.decode().isdigit() == False:
    data = sys.stdin.buffer.read1(1)
  
  while data.decode().isdigit():
    size *= 10
    size += int(data.decode())
    data = sys.stdin.buffer.read1(1)

  data = sys.stdin.buffer.read(size)
  sys.stdout.buffer.write(data)
  sys.stdout.buffer.flush()
