import time
import donkeycar as dk
import RPi.GPIO as GPIO

g_angle = 0

class ZumoSteering:

    def __init__(self):

        global g_angle
        g_angle = 0


    def run(self, angle):

        global g_angle
        g_angle = angle

    def shutdown(self):
        self.run(0) #set steering straight



class ZumoThrottle:

    MIN_THROTTLE = -1
    MAX_THROTTLE =  1

    def __init__(self, controller_l=None,
                       controller_r=None,
                       gpio_l=11,
                       gpio_r=12,
                       max_pulse=0,
                       min_pulse=0,
                       zero_pulse=0):

        self.controller_l = controller_l
        self.controller_r = controller_r
        self.gpio_l = gpio_l
        self.gpio_r = gpio_r
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse

        #send zero pulse to calibrate ESC
        self.controller_l.set_pulse(self.zero_pulse)
        self.controller_r.set_pulse(self.zero_pulse)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_l, GPIO.OUT)
        GPIO.output(self.gpio_l, 0)
        GPIO.setup(self.gpio_r, GPIO.OUT)
        GPIO.output(self.gpio_r, 0)

        time.sleep(1)


    def run(self, throttle):
        global g_angle

        if throttle > 0:
            pulse_l = dk.util.data.map_range(throttle * (1.0 + g_angle),
                                                    0, self.MAX_THROTTLE,
                                                    self.zero_pulse, self.max_pulse)
            pulse_r = dk.util.data.map_range(throttle * (1.0 - g_angle),
                                                    0, self.MAX_THROTTLE,
                                                    self.zero_pulse, self.max_pulse)
            GPIO.output(self.gpio_l, 0)
            GPIO.output(self.gpio_r, 0)

        else:
            pulse_l = dk.util.data.map_range(throttle * (1.0 + g_angle),
                                                    self.MIN_THROTTLE, 0,
                                                    self.max_pulse, self.zero_pulse)
            pulse_r = dk.util.data.map_range(throttle * (1.0 - g_angle),
                                                    self.MIN_THROTTLE, 0,
                                                    self.max_pulse, self.zero_pulse)
            GPIO.output(self.gpio_l, 1)
            GPIO.output(self.gpio_r, 1)

        self.controller_l.set_pulse(pulse_l)
        self.controller_r.set_pulse(pulse_r)

    def shutdown(self):
        self.run(0) #stop vehicle
