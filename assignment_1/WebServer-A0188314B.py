import sys
from socket import *

class HTTPRequest:
    def __init__(self, input_request):
        substrings = input_request.split()
        self.method = substrings[0].upper().decode()
        self.path = substrings[1].decode()
        if (self.method == 'POST'):
            self.content_length = substrings[-2].decode()
            self.content_body = substrings[-1]
    
    def get_method(self):
        return self.method
    
    def get_path(self):
        return self.path

    def get_content_length(self):
        return self.content_length
    
    def get_content_body(self):
        return self.content_body

class WebServer:
    def __init__(self, port_number):
        self.port_number = port_number
        self.buffer_input = bytearray()
        self.buffer_output = bytearray()
        self.current_request = bytearray()
        self.current_request_count = 0
        self.current_content_length = 0
        self.current_content_count = 0
        self.parsing_content = False
        self.hashtable = dict()

    def start(self):
        listening_socket = socket(AF_INET, SOCK_STREAM)
        listening_socket.bind(('', self.port_number))
        listening_socket.listen(1)
        sys.stderr.write('[Server] Listening on port ' + str(self.port_number) + '.\n')
        while True:
            connection_socket = listening_socket.accept()
            sys.stderr.write('[Server] Connected to client.\n')
            self.buffer_input = connection_socket.recv(1024)
            while len(self.buffer_input) > 0:
                self.extract_request(connection_socket)
                self.buffer_input = connection_socket.recv(1024)
        listening_socket.close()

    def extract_request(self, connection_socket):
        for i in range(len(self.buffer_input)):
            self.current_request.append(self.buffer_input[i])
            self.current_request_count += 1
            if (self.current_request_count > 1) and (self.current_request[-1] == ord(' ')) and (self.current_request[-2] == ord(' ')):
                if (self.current_request.startswith(('POST').encode())):
                    # ?
                    self.current_content_length = int(chr(self.current_request[-3]))
                    self.parsing_content = True
                else:
                    self.handle_request(connection_socket)
                    self.current_request = bytearray()
                    self.current_request_length = 0

            if self.parsing_content == True:
                if self.current_content_count == self.current_content_length:
                    self.handle_request(connection_socket)
                    self.current_request = bytearray()
                    self.current_request_length = 0
                    self.current_content_count = 0
                    self.parsing_content = False
                self.current_content_count += 1

    def handle_request(self, connection_socket):
        request = HTTPRequest(self.current_request)

        method = request.get_method()
        path = request.get_path()
        
        if path.startswith('/key/'):
            key = path.replace('/key/', '')
            if method == 'POST':
                self.hashtable[key] = request.get_content_body()
                self.send_200(connection_socket, -1)
            elif method == 'GET':
                if key in self.hashtable:
                    self.buffer_output += self.hashtable[key]
                    self.send_200(connection_socket, len(self.hashtable[key]))
                else:
                    self.send_404(connection_socket)
            elif method == 'DELETE':
                if key in self.hashtable:
                    del self.hashtable[key]
                    self.send_200(connection_socket, len(self.hashtable[key]))
                else:
                    self.send_404(connection_socket)
            else:
                sys.stderr.write('[Server] Unknown request method.\n')
        else:
            sys.stderr.write('[Server] Unknown request path.\n')

    def send_404(self, connection_socket):
        response = ('404 NotFound  ').encode()
        connection_socket.send(response)

    def send_200(self, connection_socket, content_length):
        response = bytearray()
        if content_length > 0:
            response = ('200 OK content-length ' + str(content_length) + '  ').encode() + self.buffer_output
        else:
            response = ('200 OK  ').encode()
        connection_socket.send(response)
        self.buffer_output = bytearray()

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python WebServer-A0188314B.py port_number\n")
        sys.stderr.write("Example: python WebServer-A0188314B.py 1024\n")
        exit(0)
    WebServer(int(sys.argv[1])).start()

if __name__ == "__main__":
    main()
