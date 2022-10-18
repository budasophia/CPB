""" Bluefruit_SafetyBeacon
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.1 Amelia Glenn 2/11/2022

Last modified:
Benjamin Esquieres 10/14/2022
Changes:
Formatting and comments
"""

import board  # import the pins on this board
from analogio import AnalogIn  # import access to analog input from basic analog IO
import pwmio  # import access to basic PWM IO

anin = AnalogIn(board.A3)  # anin is an analog input connected to pin A3
pwmout = pwmio.PWMOut(board.A2)  # pwmout is a PWM output connected to pin A2

"""The digitized value of the analog input ranges from 0 to 65535.
(The Bluefruit has 16-bit analog-to-digital conversion, yielding 65536 unique digital values.)
Note that this output is not "true analog": it will be a pulse width modulated square wave (PWM)."""

while True:  # loop until program terminates, analogous to void loop() in Arduino
    "Write the digitized analog input value to the serial monitor. To view: Ctrl+Shift+M (PC) or Cmd+Shift+M (Mac)"

    """Light brightens"""
    for i in range(0, 65535, 10):  # for i = 0, 10, 20, ... , 65530
        duty_cycle = (
            anin.value * i
        ) / 100000  # multiply the value of anin by i and divide by 100000 to calculate PWM duty cycle
        pwmout.duty_cycle = int(duty_cycle)  # set pwmout duty cycle, which sets the brightness of the LED
        print(duty_cycle)  # print duty cycle to serial monitor

    """Light dims"""
    for i in range(65535, 0, -10):  # for i = 65535, 65525, 65515, ... , 5
        duty_cycle = (anin.value * i) / 100000
        pwmout.duty_cycle = int(duty_cycle)
        print(duty_cycle)
