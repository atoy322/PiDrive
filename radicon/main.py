import socket

from threading import Thread

from function_http import HTTPServer
from function_ws import thread


t = Thread(target=thread, daemon=True)
t.start()

server_sock = socket.socket()
server_sock.bind(("", 8000))
server_sock.listen(1)
server = HTTPServer(server_sock)

print("[Now Serving]")
server.client_loop()
