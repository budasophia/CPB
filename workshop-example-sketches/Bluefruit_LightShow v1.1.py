'''Bluefruit_LightShow
Cycles through 5 different functions that demonstrate various illumination effects with NeoPixels:
colorWipe, theaterChase, rainbow, rainbowCycle, theaterChaseRainbow
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
Based on Flora version of code by Joe Samosky
v1.0 Amelia Glenn 2/10/2022
'''

import board
import neopixel
import digitalio
import time
import usb_hid
from rainbowio import colorwheel

onboard=neopixel.NeoPixel(board.D8,10,brightness=.5)
strip=neopixel.NeoPixel(board.D6,2,brightness=.5)

def rainbow(pixels):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        time.sleep(.05)

def colorWipe(pixels,color):
    for i in range(len(pixels)):
        pixels[i]=color
        time.sleep(.25)
    time.sleep(.25)

def theaterChase(pixels,color,wait):
    for q in range(0,2,1):
        for i in range(0,len(pixels),2):
            pixels[i+q]=color
            time.sleep(wait)
    time.sleep(wait)
    for k in range(0,2,1):
        for i in range(0,len(pixels),2):
            pixels[i+k]=(0,0,0)
            time.sleep(wait)
    time.sleep(wait)

def theaterChaseX(pixels,color,x):
    y=0
    while y<x:
        theaterChase(pixels,color,.25)
        y+=1

def theaterChaseRainbow(pixels):
    for j in range(0,255,10):
        for i in range(len(pixels)):
            idx = int(i + j)
            color=colorwheel(idx & 255)
            theaterChase(pixels,color,.05)

def startShow(showtype,pixels):
    'a very long if statement bc circuitpy is not quite updated for match case'
    if showtype==0:
        for k in range(0,3,1):
            'three cycles of off/r/g/b'
            colorWipe(pixels,(0,0,0))
            colorWipe(pixels,(255,0,0))
            colorWipe(pixels,(0,255,0))
            colorWipe(pixels,(0,0,255))
    elif showtype==4:
        'white theater chase'
        theaterChaseX(pixels,(50,50,50),3)
    elif showtype==5:
        'red theater chase'
        theaterChaseX(pixels,(50,0,0),3)
    elif showtype==6:
        'blue theater chase'
        theaterChaseX(pixels,(0,0,50),3)
    elif showtype==7:
        rainbow(pixels)
    elif showtype==8:
        theaterChaseRainbow(pixels)
    else:
        print('error number')
    time.sleep(.5)


while True:
    for showType in range(9):
        print(showType)
        startShow(showType,strip)
        if showType>9:
            showType=0
