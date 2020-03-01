import sys
from socket import *

class HTTPRequest:
    def __init__(self, request):
        self.method = request[0]
        self.path = request[1]
        if (self.method == 'POST'):
            self.content_body = request[2]
    
    def get_method(self):
        return self.method
    
    def get_path(self):
        return self.path
    
    def get_content_body(self):
        return self.content_body

class WebServer:
    def __init__(self, port_number):
        self.port_number = port_number
        self.current_request = bytearray()
        self.hashtable = dict()

    def start(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', self.port_number))
        self.socket.listen(1)
        sys.stderr.write('[Server] Listening on port ' + str(self.port_number) + '.\n')
        while True:
            self.connection_socket, address = self.socket.accept()
            sys.stderr.write('[Server] Connected to client.\n')
            while True:
                input_data = self.connection_socket.recv(1024)
                self.current_request += input_data
                if len(input_data) == 0 and len(self.current_request) == 0:
                    break
                self.parse_request()
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()

    def parse_request(self):
        while True:
            header_end = self.current_request.find(('  ').encode())
            if header_end == -1:
                break
            substrings = self.current_request[:header_end].decode().split()
            content_exist = False
            content_length = 0
            for i in range(len(substrings)):
                if substrings[i].lower() == 'Content-Length'.lower() :
                    try:
                        content_exist = True
                        content_length = int(substrings[i + 1])
                        break
                    except ValueError:
                        continue
            request = [substrings[0].upper(), substrings[1]]
            if content_exist:
                if header_end + 2 + content_length > len(self.current_request):
                    break
                else:
                    request.append(self.current_request[header_end + 2 : header_end + 2 + content_length])
                    self.process_request(HTTPRequest(request))
                    self.current_request = self.current_request[header_end + 2 + content_length:]
            else:
                self.process_request(HTTPRequest(request))
                self.current_request = self.current_request[header_end + 2:]

    def process_request(self, request):
        method = request.get_method()
        path = request.get_path()
        if path.startswith('/key/'):
            key = path.replace('/key/', '')
            if method == 'POST':
                self.hashtable[key] = request.get_content_body()
                self.send_response(200)
            elif method == 'GET':
                if key in self.hashtable:
                    self.send_response(200, self.hashtable[key])
                else:
                    self.send_response(404)
            elif method == 'DELETE':
                if key in self.hashtable:
                    self.send_response(200, self.hashtable[key])
                    del self.hashtable[key]
                else:
                    self.send_response(404)
            else:
                sys.stderr.write('[Server] Unknown request method.\n')
        else:
            sys.stderr.write('[Server] Unknown request path.\n')

    def send_response(self, code, content_body = bytearray()):        
        response = bytearray()
        if code == 404:
            response = ('404 NotFound  ').encode()
        else:
            if len(content_body) > 0:
                response = ('200 OK content-length ' + str(len(content_body)) + '  ').encode() + content_body
            else:
                response = ('200 OK  ').encode()
        self.connection_socket.send(response)

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python WebServer-A0188314B.py port_number\n")
        sys.stderr.write("Example: python WebServer-A0188314B.py 1024\n")
        return
    WebServer(int(sys.argv[1])).start()

if __name__ == "__main__":
    main()
