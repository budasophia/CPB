""" Bluefruit_tiltSwitch_v1.4.py
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.1 Amelia Glenn 2/13/2022

Latest version: v1.4

Last modified:
Benjamin Esquieres 03/02/2023
Changes:
Remove input pull direction
"""

import board  # import board module to access board's pins
import digitalio  # import digitalio module to access digital input/output


led = digitalio.DigitalInOut(board.D9)  # LED is connected to pin D9
led.switch_to_output()  # LED is a digital output

tiltball = digitalio.DigitalInOut(board.D10)  # tilt switch is conneted to pin D10
tiltball.switch_to_input()  # tiltball is a digital input

while True:  # loop until program terminates, analogous to void loop() in Arduino
    if tiltball.value == True:  # if tilt switch is vertical (closed circuit)
        led.value = False  # turn off LED
    else:  # if not vertical (open circuit)
        led.value = True  # turn on LED
