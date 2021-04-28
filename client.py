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
        print(size)

        while True:
            data = s.recv(4096)
            received += len(data)
            print(received)
            img_buf += data
            if size <= received:
                break

        img = Image.open(io.BytesIO(img_buf))
        print(img)


except Exception as e:
    raise e
    s.close()
