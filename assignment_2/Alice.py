import sys
import zlib
from socket import *

class Alice:
    def __init__(self, port_number):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.address = ('localhost', port_number)
        self.seq = 0
        self.packet = bytearray()
        self.feedback = bytearray()

    def send(self):
        try:
            self.socket.sendto(self.packet, self.address)
            self.socket.settimeout(0.1)
            self.feedback, address = self.socket.recvfrom(1024)
            self.validate()
        except timeout:
            self.send()
    
    def validate(self):
        resp = self.feedback.decode()
        if resp.count(' ') < 1:
            self.send()
            return
        substrings = resp.split(' ', 1)
        if not substrings[0].isdigit():
            self.send()
            return
        checksum, key = int(substrings[0]), substrings[1]
        if checksum != zlib.crc32(key.encode()) or key != 'ACK':
            self.send()
            return

    def start(self):
        while True:
            message = sys.stdin.read(50)
            if message == '':
                break
            data = message.encode()
            checksum = zlib.crc32(data)
            self.packet = (str(checksum) + ' ' + str(self.seq) + ' ').encode() + data
            self.send()
            self.seq += 1

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 Alice.py port_number\n")
        sys.stderr.write("Example: python3 Alice.py 9000\n")
        return
    Alice(int(sys.argv[1])).start()

if __name__ == "__main__":
    main()
