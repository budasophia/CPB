''' Bluefruit_SafetyBeacon
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.1 Amelia Glenn 2/11/2022
'''

import time
import board
from analogio import AnalogIn
import pwmio

anin = AnalogIn(board.A3)
pwmout = pwmio.PWMOut(board.A2)

'''The digitized value of the analog input ranges from 0 to 1023.
(The Flora has 10-bit analog-to-digital conversion, yielding 1024 unique digital values.)
Note that this output is not "true analog": it will be a pulse width modulated square wave (PWM).'''

while True:
    'Write the digitized analog input value to the serial monitor. To view: Ctrl+Shift+M (PC) or Cmd+Shift+M (Mac)'

    for i in range(0,65535,10):
        pwmout.duty_cycle=int((anin.value*i)/100000)
        print((anin.value*i)/100000)

    for i in range(65535,0,-10):
        pwmout.duty_cycle=int((anin.value*i)/100000)
        print((anin.value*i)/100000)
