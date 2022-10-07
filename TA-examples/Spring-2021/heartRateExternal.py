# Edited Spring 2022 by Eli Wissenbach
#Measures heart rate using the onboard neopixel while the buzzer beeps per beat#
"""CircuitPython Essentials Analog In example"""
import time
import board
#import pulseio
from analogio import AnalogIn
#import simpleio
import digitalio
import neopixel
import pwmio
from rainbowio import colorwheel

analog_in = AnalogIn(board.A1)
#from adafruit_circuitplayground import cp
#light = digitalio.DigitalInOut(board.D13)
#light.switch_to_output()
buzzer = pwmio.PWMOut(board.A2, variable_frequency=True)
threshold=550
oldRange= 65535
newRange=1023
OFF=0
ON=2**15  #2^15

low2=0
high2=1023 #high analog value from arduino
low1=0
high1=65535 #high analog value from bluefruit
def mapper(val):
    val = low2+(val-low1)*(high2-low2)/(high1-low1)
    return val
def get_voltage(pin):
    return (mapper(pin.value))
def sign(value):
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0
# How many light readings per sample
NUM_OVERSAMPLE = 10
# How many samples we take to calculate 'average'
NUM_SAMPLES = 20
samples = [0] * NUM_SAMPLES
lasttime = time.monotonic()

onboard=neopixel.NeoPixel(board.NEOPIXEL,10,brightness=.5)
onboard[1]=((0,255,0))  #set pixel color to green

while True:
    for i in range(NUM_SAMPLES):
        # Take NUM_OVERSAMPLE number of readings really fast
        oversample = 0
        for s in range(NUM_OVERSAMPLE):
            oversample += float(get_voltage(analog_in))
        # and save the average from the oversamples
        samples[i] = oversample / NUM_OVERSAMPLE  # Find the average

        mean = sum(samples) / float(len(samples))  # take the average
        print((samples[i] - mean,))  # 'center' the reading

        if i > 0:
            # If the sign of the data has changed munus to plus
            # we have one full waveform (2 zero crossings), pulse LED
            if sign(samples[i]-mean) <= 0 and sign(samples[i-1]-mean) > 0:
                onboard[9] = (200, 0, 0)  # Pulse LED
                buzzer.frequency=440
                buzzer.duty_cycle=ON
            else:
                onboard[9] = (0, 0, 0)    # Turn LED off
                buzzer.duty_cycle=OFF

        time.sleep(0.025)  # change to go faster/slower




