import time

import pigpio



EN = 18  #  GPIO18 (PWM0)
A1 = 23  #  GPIO23
A2 = 24  #  GPIO24
SERVO = 13  #  GPIO13 (PWM1)

PWM_FREQ = 1000  # 1 kHz


class Car:
    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(EN, pigpio.OUTPUT)
        self.pi.set_mode(A1, pigpio.OUTPUT)
        self.pi.set_mode(A2, pigpio.OUTPUT)

    def change_speed(self, speed):
        speed *= 1000
        self.pi.hardware_PWM(EN, PWM_FREQ, speed)

    def forward(self):
        self.pi.write(A1, 1)
        self.pi.write(A2, 0)

    def backward(self):
        self.pi.write(A1, 0)
        self.pi.write(A2, 1)

    def stop(self):
        self.pi.write(A1, 0)
        self.pi.write(A2, 0)

    def action(self, speed):
        if speed >= 0:
            self.forward()
            self.change_speed(speed)
        else:
            self.backward()
            self.change_speed(speed)

    def terminate(self):
        self.pi.stop()

