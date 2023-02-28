#Capacitive Touch Example with Onboard NeoPixels
#Annabella Peretti -- Last modified 2/27/2023

import board #import the pins on this board
import neopixel #import neopixel
import time #import time functionality
import touchio #import touch functionality

onboard = neopixel.NeoPixel(board.D8, 10, brightness=2) #assigning 10 onboard neopixels at pin D8
touch_pad = board.A1 #assigning touch trigger at pin A1
touch = touchio.TouchIn(touch_pad) #assigning variable that reads if pin A1 is touched
while True:
    if touch.value: #if pin A1 is touched
        onboard.fill((255, 0, 0)) #change onboard neopixels to red color
        onboard.show() #show red LED color
        time.sleep(1) #hold color for 1 second
        onboard.fill((0, 0, 0)) #change onboard neopixels to no color
        onboard.show() #show no LED color (LEDs off)
