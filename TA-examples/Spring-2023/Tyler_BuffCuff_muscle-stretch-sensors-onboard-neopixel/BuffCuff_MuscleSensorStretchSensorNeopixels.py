""" BuffCuff_MuscleAndStretchSensorDemo
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.0 Tyler Hansen 3/2/2023

Last modified:
Tyler Hansen 3/2/2023
Changes:
First version implemented with Myoware Muscle Sensor & stretch sensor
"""

import board
import digitalio
from analogio import AnalogIn
import neopixel
import time

muscleIn = AnalogIn(board.A4)
stretchIn = AnalogIn(board.A3)

onboard = neopixel.NeoPixel(board.D8, 10, brightness=0.5)

while True:

    if muscleIn.value > 60000:
        onboard.fill((0, 255, 0))
    elif stretchIn.value < 55000:
        onboard.fill((0, 0, 255))
    else:
        onboard.fill((0, 0, 0))

    time.sleep(0.1)
