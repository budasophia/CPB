'''Bluefruit_MicToLight
Allows a neopixel strip or the onboard neopixels, to ligth up in a line based on sound input to the onboard micropone.
For this code, connect external neopixels to A1/D6!

To switch between the strip and onboard neopixels, change this line towards the bottom of the code:

    pixels  = strip_neopixels

To tune the system edit the tuning parameters:

    volumeInMax
    volumeInMin
    setBrightness
    numExtNeopixels

Inspired by:
    - Sensor Plotting with Mu and CircuitPython Sound on adafruit - https://learn.adafruit.com/sensor-plotting-with-mu-and-circuitpython/sound
    - Amelia Glenn's Bluefruit_LightShow

Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering

v1.0 Issam Abushaban 03/03/2022
'''

import array
import time
import audiobusio
import board
import neopixel

import AOM_Library

# Global Variable - Keeping track of neopixel stretch will help us make smooth transitions!
lastStretch         = 0

# Some tuning paramaters
volumeInMin         = 10                    # This serves as a noise reduction. Set this to a threshold based on ambient noise (range 0 : 30000 for screaming)
volumeInMax         = 500                   # This serves as the max volume in. Anything higher, would be considered equal (range 0 : 30000 for screaming)
setBrightness       = 0.1                   # This is the brightness of your neopixels (range 0.0 : 1.0 warning will burn your eyes if greater than 0.5)
numExtNeopixels     = 14                    # This is the number of external neopixels

# So our input is audio volume and neopixels
def soundToLightShow(magnitude, pixels):
    # Set lastStretch as global so we reference it from outside the function
    global lastStretch

    # Lets just cut back magnitude, in case any really loud sounds come in :)
    if magnitude > volumeInMax:
        magnitude = volumeInMax
    elif magnitude < volumeInMin:
        magnitude = volumeInMin

    # First we want the amount of "stretch" (AKA fraction of neopixels to light up)
    # to be determined by the magnitude of the volume of incoming audio...
    # To do this, you need to use the AOM mapToRange() function!
    newStretch = int(AOM_Library.mapToRange(magnitude,volumeInMin,volumeInMax,0,len(pixels) - 1))

    ## Debugging code! Comment it out if you don't need it!
    # print("lastStretch: " + str(lastStretch))
    # print("newStretch: " + str(newStretch))

    # Last we want color to be a function of time!
    modTime = time.time() % 10
    newColor = (int(AOM_Library.mapToRange(modTime,0,10,0,255)),
                int(AOM_Library.mapToRange(modTime + 4,0,10,0,255)),
                int(AOM_Library.mapToRange(modTime + 9,0,10,0,255)))

    ## Debugging code! Comment it out if you don't need it!
    # print("modTime: " + str(modTime))
    # print("newColor: " + str(newColor))

    # clean up everything if no stretching
    # (If we have silence then all the lights shoud turn off)
    if (newStretch == 0):
        for i in range(len(pixels)):
            pixels[i]=(0,0,0)

    # Clean up neopixels from last round only!
    # (Otherwise if last time the stretch was longer aka the sound was louder, turn off the neo pixles that are not gonna be used!)
    if (lastStretch >= newStretch):
        for i in range(lastStretch, newStretch, -1):
            pixels[i]=(0,0,0)
        for i in range(newStretch, 0,1):
            pixels[i]=newColor

    # Color this rounds neopixels!
    # If the new stretch is longer than the old stretch we should just give them the new colors!
    else:
        for i in range(1, newStretch, 1):
            pixels[i-1]=newColor

    # Set the last stretch length to the new one!
    lastStretch = newStretch

# Define the Onboard Mic
onboard_mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)

# Define the Onboard Neopixels
onboard_neopixels=neopixel.NeoPixel(
    board.D8,
    10,
    brightness=setBrightness
)

# Define the Strip of Neopixels
strip_neopixels=neopixel.NeoPixel(
    board.D6,
    numExtNeopixels,
    brightness=setBrightness
)

# The choice of neopixels you want to use
pixels  = strip_neopixels

# For collecting the audio sample
samples = array.array('H', [0] * 160)

while True:
    # Take a recording
    onboard_mic.record(samples, len(samples))

    # Get the magnitude (volume) of that recording
    magnitude = AOM_Library.normalized_rms(samples)

    #Put on the show!
    soundToLightShow(magnitude, pixels)
