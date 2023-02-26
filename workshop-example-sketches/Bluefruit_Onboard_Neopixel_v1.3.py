""" Bluefruit_Onboard_Neopixel_v1.3.py
Illuminates the CPB's built-in NeoPixels (internally connected to pin 8).
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.2 Amelia Glenn 02/11/2022
Wheel() colorwheel function based on Adafruit's Flora demo code: https://learn.adafruit.com/pages/5682/elements/1711074/download

Latest version: v1.3

Last modified:
Benjamin Esquieres 02/17/2023
Changes:
Formatting and comments
"""

import board  # import board module to access board's pins
import neopixel  # import neopixel module to access neopixels
from time import sleep  # import sleep function from time library


def Wheel(wheelpos):
    """In python, functions must be defined before they are called. We'll use this later!
    Wheel(n) -- input a value n ranging from 0 to 255 to get a color value from a color wheel
    The colours are a transition red - green - blue - back to red."""
    wheelpos = 255 - wheelpos
    if wheelpos < 85:  # if wheelpos is less than 85
        return (255 - wheelpos * 3, 0, wheelpos * 3)  # return tuple with the calculated RGB values
    elif wheelpos < 170:  # if wheelpos is less than 170 but not less than 85
        wheelpos -= 85  # wheelpos = wheelpos - 85
        return (0, wheelpos * 3, 255 - wheelpos * 3)
    else:  # if wheelpos is not less than 170 (greater than or equal to 170)
        wheelpos -= 170
        return (wheelpos * 3, 255 - wheelpos * 3, 0)


"""Let's have the Bluefruit's onboard NeoPixels illuminate red, green, blue and white in sequence for 1 second each.// strip.setPixelColor(n, R, G, B) is the function used to send an RGB color value to a NeoPixel.
The first argument is the pin the neopixels are connected to, in this case pin D8
The second argument is the number of pixels in the strip. In this case, there is ten pixels on the "strip" -- so n=10
    red, green and blue range from 0 (off) to 255 (maximum brightness)
Note that onboard.fill DOES immeditely set the color;
if you want to set pixels as off, use (0,0,0)"""
onboard = neopixel.NeoPixel(board.D8, 10, brightness=0.5)

while True:
    onboard.fill((255, 0, 0))  # set onboard neopixels to red (255, 0, 0) and display
    sleep(1)  # Wait for 1 second. sleep() takes numbers in seconds

    onboard.fill((0, 255, 0))  # set pixel color to green
    sleep(1)

    onboard.fill((0, 0, 255))  # set pixel color to blue
    sleep(1)

    onboard.fill((255, 255, 255))  # set pixel color to white
    sleep(1)
    """Now let's transition smoothly through rainbow colors
    We'll use the function "Wheel" defined above"""
    for i in range(1, 5):  # for i = 1, 2, 3, 4
        for j in range(0, 255):  # for j = 0, 1, 2, ... , 254
            onboard.fill(Wheel(j))  # set pixel color to the value returned by Wheel(j)
            sleep(0.03)
