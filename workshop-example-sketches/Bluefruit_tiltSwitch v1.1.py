""" Bluefruit_tiltSwitch
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.1 Amelia Glenn 2/13/2022

Last modified:
Benjamin Esquieres 10/14/2022
Changes:
Formatting and comments
"""

import board  # import the pins on this board
import digitalio  # import access to basic digital input/output


led = digitalio.DigitalInOut(board.D9)  # led is connected to pin D9
led.switch_to_output()  # led is an output pin

switch = digitalio.DigitalInOut(board.D10)  # tilt switch is conneted to pin D10
switch.switch_to_input(
    pull=digitalio.Pull.UP
)  # switch is an input and is initially off

while True:  # loop until program terminates, analogous to void loop() in Arduino
    if switch.value:  # if tilt switch is vertical (on)
        led.value = False  # turn off LED
    else:  # else (if not vertical)
        led.value = True  # turn on LED
