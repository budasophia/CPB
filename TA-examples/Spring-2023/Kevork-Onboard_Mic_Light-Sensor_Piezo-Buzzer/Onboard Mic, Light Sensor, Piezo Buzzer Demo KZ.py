#Onboard Mic, Light Sensor, Piezo Buzzer Demo

#This code will activate a buzzer when the board reads a high enough input from the light sesnsor.
#The buzzer will continue to buzz until the sound sensor registers a loud enough sound.
#Once it does, the buzzing will stop.

#Written by Kevork Zeibari
#Updated 3/28/2023

#You always need to import 'board' and 'time' to make sure your CPB functions
import board
import time


import neopixel  # this is for your on-board and off-board neopixels
from rainbowio import colorwheel
import analogio
import simpleio
import touchio
import digitalio
import array
import math
import audiobusio
import pulseio
import pwmio

#-----------------------------------------------------------------------------
# This is where you make instances of your inputs and outputs (think arduino!)
#-----------------------------------------------------------------------------

#Exponential Scaling Factor
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

#Set amount of samples to read at once
NUM_SAMPLES = 160

# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


# Scale input_value between output_min and output_max, exponentially.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / (input_max - input_min)
    return output_min + math.pow(normalized_input_value, SCALE_EXPONENT) * (
        output_max - output_min
    )


# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(float(sample - minbuf) * (sample - minbuf) for sample in values)

    return math.sqrt(samples_sum / len(values))


def mean(values):
    return sum(values) / len(values)


# Initialize Microphone and Set Sample Rate
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
sample_rate=16000, bit_depth=16)

#Create array to store samples in
samples = array.array("H", [0] * NUM_SAMPLES)
mic.record(samples, len(samples))

# Set min and max microphone values
input_floor = normalized_rms(samples) + 10
input_ceiling = input_floor + 500
peak = 0


# Inititalize AUDIO pin
buzzer = pwmio.PWMOut(board.AUDIO)

# Set parameters for ON/OFF states
OFF = 0 #Duty cycle of 0 for PWM Buzzer Output
ON = 2**15 #Represents 2^15 or 32768 which is half of the max duty cycle of 65535 for the PWM Buzzer Output

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# The main loop you put your code into
while True:

    print(light.value) # Print to serial monitor
    mic.record(samples, len(samples)) #Start recording from microphone
    magnitude = normalized_rms(samples) #Run sample array through rms function to get the magnitude
    print(magnitude) # Print to serial monitor

    if light.value >= 500: #Conditional statement to activate buzzer when light levels reach over 500

        buzzer.duty_cycle = ON
    elif magnitude >= 600: #Additional conditional statement to break pout of the code when sound levels over 600 are reached
        break

    time.sleep(0.01)
