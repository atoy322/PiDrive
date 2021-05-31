import socket
import struct
import io
import time

from PIL import Image


RASPI_IP = "192.168.17.133"


def get_frame(stream_sock):
    received = 0
    img_buf = b""
    size_data = stream_sock.recv(4)
    size = struct.unpack(">I", size_data)[0]

    while True:
        data = stream_sock.recv(size-received)
        received += len(data)
        img_buf += data
        if size <= received:
            break

    img = Image.open(io.BytesIO(img_buf))

    return img


c = socket.socket()
c.connect((RASPI_IP, 8080))

s = socket.socket()
s.connect((RASPI_IP, 8000))

i = 0

while True:
    frame = get_frame(s)
    print(i)
    frame.save(f"train_data/img-{i}.jpg")
    i += 1


