# Bluefruit_NeoPixel_Current_Test.py
# Script loaded onto CPBs for the Art of Making Current Measuring Workshop
# v1.0 11-10-2022
# Jospeh Samosky

import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1, auto_write=False)

while True:
    pixels[0]=(255,255,255) # Illuminate 1 NeoPixel white for 5 seconds
    pixels.show()
    time.sleep(5)

    pixels[0]=pixels[1]=(255,255,255) # Illuminate 2 NeoPixels white for 5 seconds
    pixels.show()
    time.sleep(5)

    pixels.fill((255,255,255)) # Illuminate all 10 onboard NeoPixels white for 5 seconds
    pixels.show()
    time.sleep(5)

    pixels.fill(0) # Turn off all NeoPixels for 5 seconds
    pixels.show()
    time.sleep(5)
