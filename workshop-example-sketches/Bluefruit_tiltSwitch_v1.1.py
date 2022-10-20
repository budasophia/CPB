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

tiltball = digitalio.DigitalInOut(board.D10)  # tilt switch is conneted to pin D10
tiltball.switch_to_input(
    pull=digitalio.Pull.UP
)  # tiltball is an input and is initially off

while True:  # loop until program terminates, analogous to void loop() in Arduino
    if tiltball.value == True:  # if tilt switch is vertical (closed circuit)
        led.value = False  # turn off LED
    else:  # if not vertical (open circuit)
        led.value = True  # turn on LED
