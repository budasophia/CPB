#import the libraries we need
import board
import neopixel
import time
import math
import digitalio
from analogio import AnalogIn

analog_in = AnalogIn(board.A3) #Set A3 (Myoware Input) as Analog In
num_pixels = 10; #Define number of pixels to use (this is the number of pixels onboard the Bluefruit)
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.2, auto_write=False) #Define pixels object as onboard NeoPixels

#Define RGB values for common colors
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

#Quick helper function for setting the number of neopixels to light up
#Input: level (number of NeoPixels to light up)
def level_ring(level):
    #Create a color gradient based on the number of pixel to light up
    for i in range(0, level):
        if i >= 0 and i < 4:
            # Set first 4 pixels to green
            pixels[i] = GREEN
        elif i >= 4 and i < 7:
            #Set middle 3 pixels to yellow
            pixels[i] = YELLOW
        elif i >= 7 and i < 10:
            #Set last 3 pixels to red
            pixels[i] = RED
        else:
            pixels[i] = OFF
    #Set unused pixels to off
    for i in range(level+1, num_pixels):
        pixels[i] = OFF
    #Update pixels with new colors
    pixels.show()

#Main loop
while True:
    analog_level = round((analog_in.value/65535)*num_pixels) #Read in analog value from Myoware and round to integer level between 0 and 10
    print(analog_level) #Print analog value to serial monitor for debugging while connected to a computer
    level_ring(analog_level) #Set number of pixels to light up using helper function
    time.sleep(0.01) #Time delay to prevent problems with serial monitor
