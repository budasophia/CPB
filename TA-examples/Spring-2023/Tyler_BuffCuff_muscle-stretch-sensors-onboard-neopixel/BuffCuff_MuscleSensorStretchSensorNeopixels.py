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

#configure analog inputs
muscleIn = AnalogIn(board.A4)  #myoware muscle sensor
stretchIn = AnalogIn(board.A3)  #conductive rubber cord sensor

#configure onboard neopixels
onboard = neopixel.NeoPixel(board.D8, 10, brightness=0.5)

#establish constants to be used in while loop
muscleThreshold = 60000  #value you choose to set how much you flex before the program reacts to it
stretchThreshold = 55000  #value you choose to set how much you stretch the rubber cord before the program reacts to it

while True:

    if muscleIn.value > muscleThreshold:
        onboard.fill((0, 255, 0))  #onboard neopixels set to completely green
    elif stretchIn.value < stretchThreshold:
        onboard.fill((0, 0, 255))  #onboard neopixels set to completely blue
    else:
        onboard.fill((0, 0, 0))  #onboard neopixels turned off

    time.sleep(0.5)  #delay to account for minor fluctuations
