import socket


class Car:
    def __init__(self, ip="192.168.183.132"):
        self.client = socket.socket()
        self.client.connect((ip, 8080))

    def speed(self, speed):
        speed = int(speed)
        self.client.send("SPEED:{}".format(speed).encode())

    def steer(self, angle):
        angle = int(angle)
        self.client.send("STEER:{}".format(angle).encode())

