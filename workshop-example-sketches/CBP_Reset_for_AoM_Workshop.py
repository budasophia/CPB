"""CPB_Reset_for_AoM_Workshop
Resets the Circuit Playground so it's a blank slate and ready for the first exercise of the workshop.
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.0 Amelia Glenn 2/14/2022

Last modified:
Benjamin Esquieres 02/17/2023
Changes:
Formatting
"""

import board
import neopixel

onboard = neopixel.NeoPixel(board.D8, 10, brightness=0.5)
while True:
    onboard.fill((0, 0, 0))
