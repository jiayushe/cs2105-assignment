import sys
import zlib
from socket import *

class Alice:
    def __init__(self, port_number):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port = port_number
        self.server = 'localhost'
        self.seq = 0
        self.packet = bytearray()
        self.feedback = ''
        self.maxn = 60
    
    def send(self):
        self.socket.sendto(self.packet, (self.server, self.port))
        self.feedback, address = self.socket.recvfrom(2048)

    def start(self):        
        while True:
            message = input()
            offset = 0
            while offset < len(message):
                if offset + self.maxn < len(message):
                    segment = message[offset:offset + self.maxn]
                else:
                    segment = message[offset:]
                offset += self.maxn
                segdata = segment.encode()
                if offset >= len(message):
                    segdata += ('\n').encode()
                checksum = zlib.crc32(segdata)
                self.packet = (str(checksum) + ' ' + str(self.seq) + ' ').encode() + segdata
                self.send()
                self.validate()
                self.seq += 1
    
    def validate(self):
        while True:
            resp = self.feedback.decode()
            if resp.count(' ') < 1:
                self.send()
                continue
            substrings = resp.split(' ', 1)
            if not substrings[0].isdigit():
                self.send()
                continue
            fbkchecksum = int(substrings[0])
            fbksegment = substrings[1]
            if fbkchecksum != zlib.crc32(fbksegment.encode()) or substrings[1] != 'ACK':
               self.send()
               continue
            break

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 Alice.py port_number\n")
        sys.stderr.write("Example: python3 Alice.py 9000\n")
        return
    Alice(int(sys.argv[1])).start()

if __name__ == "__main__":
    main()
