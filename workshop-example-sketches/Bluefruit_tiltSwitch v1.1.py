''' Bluefruit_tiltSwitch
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.1 Amelia Glenn 2/13/2022
'''

import board
'import the pins on this board'
import digitalio

'led connected to D9'
led = digitalio.DigitalInOut(board.D9)
'led is an output pin'
led.switch_to_output()

'tilt switch conneted to D10'
switch = digitalio.DigitalInOut(board.D10)
'switch is an input, and starts off'
switch.switch_to_input(pull=digitalio.Pull.UP)

while True:
    'if tilt switch is vertical (on)'
    if switch.value:
        'turn off LED'
        led.value=False
    else:
        'if not vertical, turn on LED'
        led.value=True
