from websocket_server import WebSocketServer
from car_ctrl import Car


c = Car()
ws = WebSocketServer(8080)

while True:
    ws.accept()

    while True:
        try:
            data = ws.recv()
            if b": " not in data: continue
            name, val = data.decode().split(": ")
            print(val)
            if name == "slider1":
                c.speed(int(float(val)-50)*2)
            elif name == "slider2":
                c.steer(int(float(val)/100*60 - 30))
            elif name == "head":
                c.light("head", int(val))
            elif name == "back":
                c.light("back", int(val))
        except Exception as e:
            print(e)
            c.stop()
            c.steer(0)
            break


