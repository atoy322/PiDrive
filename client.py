import socket
import struct
import io
import time#

from PIL import Image



s = socket.socket()
s.connect(("atoy322.ddns.net", 8000))


try:
    while True:
        t1 = time.time()#
        received = 0
        img_buf = b""
        size_data = s.recv(4)
        size = struct.unpack(">I", size_data)[0]

        while True:
            data = s.recv(size-received)
            received += len(data)
            #print("\r", "expect: {:6d}   real: {:6d}".format(size, received), end="")
            img_buf += data
            if size <= received:
                break

        img = Image.open(io.BytesIO(img_buf))
        print(1/(time.time()-t1))#
        img.save("img.jpg")#


except Exception as e:
    raise e#
    s.close()
