#Capacitive Touch Example with Onboard NeoPixels
#Sophia Buda -- Last modified 2/22/2024

import board    #import the pins on this board
import neopixel     #import neopixel
import time     #import time functionality
import touchio  #import touch functionality

onboard = neopixel.NeoPixel(board.D8, 10, brightness=2)     #assigning 10 onboard neopixels at pin D8
touch_pad = board.A1    #assigning touch trigger at pin A1
touch_pad2 = board.A6   #assigning another touch trigger at pin A6
touch2 = touchio.TouchIn(touch_pad2)    #assigning another variable that reads if pin A6 is touched
touch = touchio.TouchIn(touch_pad)  #assigning variable that reads if pin A1 is touched
while True:
    if touch.value:     #if pin A1 is touched
        onboard.fill((255, 0, 255))     #change onboard neopixels to purple color
        onboard.show()  #show purple LED color
        onboard.fill((0, 0, 0))     #change onboard neopixels to no color
        onboard.show()   #show no LED color (LEDs off)

    elif touch2.value:   #if pin A6 is touched
        onboard.fill((0, 255, 0))   #change onboard neopixels to green color
        onboard.show()  #show green LED color
        onboard.fill((0, 0, 0))  #change onboard neopixels to no color.
        onboard.show()   #show no LED color (LEDs off)
