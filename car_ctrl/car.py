import time

import pigpio



EN = 12  #  GPIO12 (PWM0)
A1 = 23  #  GPIO23
A2 = 24  #  GPIO24
SERVO = 13  #  GPIO13 (PWM1)

PWM_FREQ = 1000  # 1 kHz

STEER_ERROR = -10

class Car:
    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(EN, pigpio.OUTPUT)
        self.pi.set_mode(A1, pigpio.OUTPUT)
        self.pi.set_mode(A2, pigpio.OUTPUT)

    def change_speed(self, speed):
        assert speed >= 0
        speed *= 10000
        self.pi.hardware_PWM(EN, PWM_FREQ, speed)

    def forward(self):
        self.pi.write(A1, 0)
        self.pi.write(A2, 1)

    def backward(self):
        self.pi.write(A1, 1)
        self.pi.write(A2, 0)

    def stop(self):
        self.pi.write(A1, 0)
        self.pi.write(A2, 0)

    def steer(self, angle):
        assert angle <= 30 or angle >= -30
        self.pi.set_servo_pulsewidth(SERVO, 1450 + angle*10 + STEER_ERROR)

    def speed(self, speed):
        if speed >= 0:
            self.forward()
            self.change_speed(speed)
        else:
            self.backward()
            self.change_speed(-speed)

    def terminate(self):
        self.pi.stop()

