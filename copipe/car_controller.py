import time

import pigpio

import car


class CarController(car.Car):
    def __init__(self):
        super().__init__()
    
    def slottle(self, x):
        x *= 100
        super().speed(x)
    
    def steer(self, x):
        x *= 30
        super().steer(x)
    
    def brake(self):
        super().stop()
