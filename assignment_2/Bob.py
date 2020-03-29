import sys
import zlib
from socket import *

class Bob:
    def __init__(self, port_number):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', port_number))
        self.seq = 0

    def send(self, address, flag):
        key = ('ACK' if flag else 'NAK').encode()
        checksum = zlib.crc32(key)
        packet = (str(checksum) + ' ').encode() + key
        self.socket.sendto(packet, address)

    def start(self):        
        while True:
            data, address = self.socket.recvfrom(1024)
            resp = data.decode()
            if resp.count(' ') < 2:
                self.send(address, 0)
                continue
            substrings = resp.split(' ', 2)
            if not (substrings[0].isdigit() and substrings[1].isdigit()):
                self.send(address, 0)
                continue
            checksum, recvseq, recvdata = int(substrings[0]), int(substrings[1]), substrings[2]
            if checksum == zlib.crc32(recvdata.encode()):
                if recvseq == self.seq:
                    sys.stdout.write(recvdata)
                    self.seq += 1
                self.send(address, 1)
            else:
                self.send(address, 0)

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 Bob.py port_number\n")
        sys.stderr.write("Example: python3 Bob.py 9001\n")
        return
    Bob(int(sys.argv[1])).start()

if __name__ == "__main__":
    main()
