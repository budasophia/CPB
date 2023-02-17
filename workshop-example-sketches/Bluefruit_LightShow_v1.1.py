"""Bluefruit_LightShow
Cycles through 5 different functions that demonstrate various illumination effects with NeoPixels:
colorWipe, theaterChase, rainbow, rainbowCycle, theaterChaseRainbow
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
Based on Flora version of code by Joe Samosky
v1.0 Amelia Glenn 2/10/2022

Last modified:
Benjamin Esquieres 02/17/2023
Changes:
Formatting and comments
"""

import board  # import board module to access board's pins
import neopixel  # import neopixel module to access neopixels
from time import sleep  # import sleep function from time module
from rainbowio import colorwheel  # import colorwheel function from rainbowio module

"""colorwheel() returns colorwheel RGB value as an integer value"""

strip = neopixel.NeoPixel(
    board.D6, 2, brightness=0.5
)  # strip is the 2 external neopixels connected to Bluefruit on pin D6


def rainbow(pixels):
    """Cycle through entire RGB spectrum"""
    for j in range(255):
        for i in range(len(pixels)):  # len() returns length, i.e. len(pixels) returns 2
            idx = int(i + j)
            pixels[i] = colorwheel(
                idx & 255
            )  # set RGB value of pixel at index i in pixels list to integer value of bitwise AND of idx and 255
        sleep(0.05)  # wait for 0.05 seconds


def colorWipe(pixels, color):
    """Set pixels RGB values equal to color"""
    for i in range(len(pixels)):
        pixels[i] = color
        sleep(0.25)
    sleep(0.25)


def theaterChase(pixels, color, wait):
    """Sequantially set pixels RGB values equal to color, then to off at interval specified by wait"""
    for q in range(0, 2, 1):
        for i in range(0, len(pixels), 2):
            pixels[i + q] = color
            sleep(wait)
    sleep(wait)
    for k in range(0, 2, 1):
        for i in range(0, len(pixels), 2):
            pixels[i + k] = (0, 0, 0)
            sleep(wait)
    sleep(wait)


def theaterChaseX(pixels, color, x):
    """Run theaterChase(pixels, color, 0.25) x number of times"""
    y = 0
    while y < x:  # loop until y is not less than x
        theaterChase(pixels, color, 0.25)
        y += 1  # increment y each time through loop


def theaterChaseRainbow(pixels):
    """Sequantially set pixels RGB values equal to every RGB value"""
    for j in range(0, 255, 10):
        for i in range(len(pixels)):
            idx = int(i + j)
            color = colorwheel(idx & 255)
            theaterChase(pixels, color, 0.05)


def startShow(showtype, pixels):
    "Python equivalent of switch case to start light show specified by showType"
    if showtype == 0:
        for _ in range(0, 3, 1):  # cycle through off/r/g/b three times
            colorWipe(pixels, (0, 0, 0))  # off
            colorWipe(pixels, (255, 0, 0))  # red
            colorWipe(pixels, (0, 255, 0))  # green
            colorWipe(pixels, (0, 0, 255))  # blue
    elif showtype == 4:
        theaterChaseX(pixels, (50, 50, 50), 3)  # (50, 50, 50) -> white theater chase
    elif showtype == 5:
        theaterChaseX(pixels, (50, 0, 0), 3)  # (50, 0, 0) -> red theater chase
    elif showtype == 6:
        theaterChaseX(pixels, (0, 0, 50), 3)  # (0, 0, 50) -> blue theater chase
    elif showtype == 7:
        rainbow(pixels)
    elif showtype == 8:
        theaterChaseRainbow(pixels)
    else:
        print("error number")
    sleep(0.5)


while True:  # loop until program terminates, analogous to void loop() in Arduino
    for showType in range(9):  # for showType = 0, 1, 2, ... , 8
        print(showType)  # print showType to serial monitor
        startShow(showType, strip)  # start type of light show specified by showType
