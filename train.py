import socket
import struct
import io
import time

from PIL import Image
import numpy as np


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


ctrl_stream = socket.socket()
ctrl_stream.connect((RASPI_IP, 8080))

data_stream = socket.socket()
data_stream.connect((RASPI_IP, 8000))



while True:
    frame = get_frame(data_stream)
    array = np.array(frame)

    print(array.shape)
