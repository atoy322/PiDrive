import socket
import struct
import hashlib
import base64


GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def mask(key, val):
    result = b""

    for i in range(len(val)):
        result += (val[i] ^ key[i % 4]).to_bytes(1, "big")
    
    return result


def parse_header(header_string):
    result_dict = dict()
    lines = header_string.split("\r\n")[:-2]
    line1 = lines.pop(0)
    method, uri, version = line1.split(" ")
    result_dict["method"] = method
    result_dict["uri"] = uri
    result_dict["version"] = version

    for line in lines:
        key, val = line.split(": ")
        result_dict[key] = val
    
    return result_dict


def gen_key(sec_websocket_key):
    key = (sec_websocket_key + GUID).encode()
    key = hashlib.sha1(key).digest()
    key = base64.b64encode(key).decode()
    return key


def parse_frame(first_2byte):
    FIN = bool((first_2byte[0] & 0b10000000) >> 7)
    RSV = (first_2byte[0] & 0b01110000) >> 4
    OPCODE = first_2byte[0] & 0b00001111
    MASK = bool((first_2byte[1] & 0b10000000) >> 7)
    PAYLOAD_LEN = first_2byte[1] & 0b01111111
    return FIN, RSV, OPCODE, MASK, PAYLOAD_LEN


class WebSocketServer:
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.bind(("", port))
        self.sock.listen(1)

    def accept(self):
        while True:
            self.conn, address = self.sock.accept()

            header = self.conn.recv(2048).decode()
            if not header:
                continue
            else:
                break
        
        header = parse_header(header)

        key = header["Sec-WebSocket-Key"]
        key = gen_key(key)
        response = f"HTTP 101 OK\r\nUpgrade: websocket\r\nConnection: upgrade\r\nSec-WebSocket-Accept: {key}\r\n\r\n"
        self.conn.send(response.encode())

    def send(self, data):
        buffer = []
        fin = 1
        rsv = 0
        mask_ = 0

        if type(data) == str:
            opcode = 1
            data = data.encode("utf8")
        elif type(data) == bytes:
            opcode = 2
        
        buffer.append((fin << 7) + (rsv << 4) + (opcode)) # FIN RSV OPCODE

        payload_length = len(data)
        if payload_length < 126:
            buffer.append((mask_ << 7) + (payload_length))
        elif payload_length < 65536:
            byte = payload_length.to_bytes(2, "big")
            buffer.append((mask_ << 7) + (126)) # MASK PAYLOAD_LEN
            buffer.append(byte[0])
            buffer.append(byte[1])
        else:
            byte = payload_length.to_bytes(8, "big")
            buffer.append((mask_ << 7) + (127)) # MASK PAYLOAD_LEN
            buffer.append(byte[0])
            buffer.append(byte[1])
            buffer.append(byte[2])
            buffer.append(byte[3])
            buffer.append(byte[4])
            buffer.append(byte[5])
            buffer.append(byte[6])
            buffer.append(byte[7])

        payload_data = b"".join([i.to_bytes(1, "big") for i in buffer]) + data
        length = len(payload_data)
        sent = 0

        while True:
            sent = self.conn.send(payload_data[sent:])
            length -= sent
            if not length:
                break

    def recv(self):
        frame = self.conn.recv(2)
        if not frame:
            return

        _, _, opcode, _, payload_length = parse_frame(frame)

        """
        if opcode == 1:
            print("this is text frame.")
        elif opcode == 2:
            print("this is binary frame.")
        elif opcode == 8:
            print("this is close frame.")
            # raise Exception("Connection closed")
        elif opcode == 9:
            print("this is ping frame.")
        elif opcode == 10:
            print("this is pong frame.")
        """

        if payload_length == 126:
            payload_length = self.conn.recv(2)
            payload_length = struct.unpack(">H", payload_length)[0]
        elif payload_length == 127:
            payload_length = self.conn.recv(8)
            payload_length = struct.unpack(">Q", payload_length)[0]

        mask_key = self.conn.recv(4)

        buf = b""
        while payload_length != len(buf):
            data = self.conn.recv(payload_length)
            if not data: break
            payload_length -= len(data)
            buf += data

        return mask(mask_key, buf)


if __name__ == "__main__":
    wss = WebSocketServer(8080)

    while True:
        print("accept")
        wss.accept()
        while True:
            data = wss.recv()
            if not data: break
            print(data)
