import socket
import struct
import io

from PIL import Image



s = socket.socket()
s.connect(("atoy322.ddns.net", 8000))


try:
    while True:
        received = 0
        img_buf = b""
        size_data = s.recv(4)
        size = struct.unpack(">I", size_data)[0]

        while True:
            data = s.recv(size-received)
            received += len(data)
            img_buf += data
            if size <= received:
                break

        img = Image.open(io.BytesIO(img_buf))


except Exception as e:
    s.close()
