import sys
import zlib
from socket import *

class Bob:
    def __init__(self, port_number):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', port_number))
        self.seq = 0
        self.packet = bytearray()
    
    def send(self, address, flag):
        key = 'ACK' if flag else 'NAK'
        feedback = key.encode()
        checksum = zlib.crc32(feedback)
        self.packet = (str(checksum) + ' ').encode() + feedback
        self.socket.sendto(self.packet, address)

    def start(self):        
        while True:
            segdata, address = self.socket.recvfrom(2048)
            resp = segdata.decode()
            if resp.count(' ') < 2:
                self.send(address, 0)
                continue
            substrings = resp.split(' ', 2)
            if not (substrings[0].isdigit() and substrings[1].isdigit()):
                self.send(address, 0)
                continue
            checksum = int(substrings[0])
            recvseq = int(substrings[1])
            segment = substrings[2]
            if checksum == zlib.crc32(segment.encode()):
                if recvseq == self.seq:
                    self.seq += 1
                    print(segment, end = '')
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
