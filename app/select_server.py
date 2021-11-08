import socket
import select
import os


CWD = os.getcwd().replace("\\", "/") + '/'
FILES = ''
SAMPLE_HEADER =\
'''GET / HTTP/1.1
Host: 127.0.0.1:3022
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1
Accept-Language: ja-jp
Accept-Encoding: gzip, deflate
Connection: keep-alive

'''

def file_to_bin(path):
    print(path)
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except:
        data = None
    return data



class SelectServer:
    def __init__(self, *args, **kwargs):
        self.server_socket = socket.socket(*args, **kwargs)
        self.read_waiters = {}
        self.write_waiters = {}
        
    def serve_forever(self):
        self.read_waiters[self.server_socket] = self.accept
        
        while True:
            #print(len(self.read_waiters), len(self.write_waiters))
            readables, writables, _ = select.select(
                    self.read_waiters.keys(),
                    self.write_waiters.keys(),
                    []
                )
            
            for readable in readables:
                func = self.read_waiters[readable]
                func(readable)
                self.read_waiters.pop(readable)
                
            for writable in writables:
                func, arg = self.write_waiters[writable]
                func(writable, arg)
                self.write_waiters.pop(writable)
        
    def bind(self, address):
        self.server_socket.bind(address)
        self.server_socket.listen(socket.SOMAXCONN)
        
    def accept(self, sock):
        conn, addr = sock.accept()
        self.read_waiters[conn] = self.recv
    
    def send(self, sock, data):
        sock.sendall(data)
        self.read_waiters[self.server_socket] = self.accept
        sock.close()
        
    def response(self, sock, status, options={}):
        status_code = status[0]
        status_message = status[1]
        response_message = ''
        
        response_message += f'HTTP/1.0 {str(status[0])} {status[1]}\r\n'
        
        for key in options.keys():
            val = str(options[key])
            response_message += f'{key}: {val}\r\n'
        
        #print(response_message)
        sock.sendall((response_message+'\r\n').encode())
    
    def recv(self, sock):
        header = sock.recv(2048).decode()
        
        if not header:
            self.read_waiters[self.server_socket] = self.accept
            return
        cmd, path = self.parse_header(header)
        
        if cmd == 'GET':
            data = file_to_bin(path)
            if data:
                self.response(sock, (200, 'OK'), {"Content-Length":len(data)})
                self.write_waiters[sock] = (self.send, data)
            else:
                self.response(sock, (404, 'NOT FOUND'))
                self.read_waiters[self.server_socket] = self.accept
                sock.close()
                
    
    def parse_header(self, header_str):
        lines = header_str.split('\r\n')
        cmd, path, version = lines[0].split()
        
        if path == '/':
            path = '/index.html'
        
        path = CWD + FILES + path
        
        return cmd, path


server = SelectServer()
server.bind(('0.0.0.0', 8000))
print('ready')
server.serve_forever()
