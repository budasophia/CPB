""" Tyler_Light-sensor_Mic_Buzzer_Soft-pot.py
The PitchPacer
Enables user to determine if their presentation is properly paced and if they are speaking with appropriate volume
User operation instructions:
    Power System On
    Slide SoftPot to set presentation duration in minutes
    Press Button B to see how many minutes you have selected as shown by the number of neopixels illuminated
    Cover Light Sensor to start the clock
    Prolonged beep will occur from Piezo Buzzer to confirm clock has started
    Onboard neopixels will begin illuminating with a color code to indicate volume (yellow = quiet, green = good, red = loud)
    Piezo Buzzer will beep once when 1/3 of the way through the time and twice at 2/3
    Piezo buzzer will once again emit a prolonged beep when time is up
    If you wish to stop the clock before the time is up, cover the Light Sensor again
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.0 Tyler Hansen 10/22/2023

Latest version: v1.0

Last modified:
Tyler Hansen 10/22/2023
Changes:
Initial release
"""

import board                                           # needed to utilize i/o
from time import sleep                                 # needed for incrementation and timing
import pwmio                                           # used for PWM output to piezo buzzer
import analogio                                        # used for softpot
from adafruit_circuitplayground.bluefruit import cpb   # used for light sensor, microphone, neopixels


# Softpot initializations
softpot = analogio.AnalogIn(board.A4)
line1_2 = 4800
line2_3 = 10500
line3_4 = 18800
line4_5 = 24900
line5_6 = 31300
line6_7 = 38300
line7_8 = 44600
line8_9 = 51700
line9_10 = 57900

# Buzzer initializations
buzzer = pwmio.PWMOut(board.AUDIO, variable_frequency=True) # buzzer output signal through AUDIO/D0 pad
interFreq = 400     # output frequency for intermediate timing intervals (1/3, 2/3)
start_endFreq = 800 # output frequency for start and end of timing

OFF = 0             # 0 percent duty cycle turns buzzer off
ON = 2**15          # 50 percent duty cycle turns buzzer on

# Light sensor initializations
threshold = 10      # set threshold to start the timer

# Onboard LEDs initializations
color = 25          # set common color value for RGB inputs to neopixels

# Presentation timing values
short = 0.1         # incrementation time (0.1s)
long = 1            # longer delay for when necessary (1s)

# Functions for Main Loop
def buzzOnce():     # for 1/3 of the way through timing
    buzzer.frequency = interFreq
    buzzer.duty_cycle = ON
    sleep(short)
    buzzer.duty_cycle = OFF

def buzzTwice():    # for 2/3 of the way through timing
    buzzer.frequency = interFreq
    buzzer.duty_cycle = ON
    sleep(short)
    buzzer.duty_cycle = OFF
    sleep(short)
    buzzer.duty_cycle = ON
    sleep(short)
    buzzer.duty_cycle = OFF

def buzzLong():     # for start and end of timing
    buzzer.frequency = start_endFreq
    buzzer.duty_cycle = ON
    sleep(long)
    buzzer.duty_cycle = OFF

def timerSet():     # splits softpot input into 10 different bins for different amounts of minutes
    inTime = softpot.value
    if inTime < line1_2:
        return 1
    elif inTime >= line1_2 and inTime < line2_3:
        return 2
    elif inTime >= line2_3 and inTime < line3_4:
        return 3
    elif inTime >= line3_4 and inTime < line4_5:
        return 4
    elif inTime >= line4_5 and inTime < line5_6:
        return 5
    elif inTime >= line5_6 and inTime < line6_7:
        return 6
    elif inTime >= line6_7 and inTime < line7_8:
        return 7
    elif inTime >= line7_8 and inTime < line8_9:
        return 8
    elif inTime >= line8_9 and inTime < line9_10:
        return 9
    elif inTime >= line9_10:
        return 10

def numIterations():  # determines number of times needed to increment the loop to reach desired number of minutes for presentation
    numMinutes = timerSet()
    iterationsPerMinute = 60 / short
    return (round(0.8*(numMinutes * iterationsPerMinute)))

def volLights():      # determines if the sound level is appropriate for presentation
    volume = cpb.sound_level
    if volume < 200:  # too quiet
        cpb.pixels.fill((color, color, 0)) # yellow
    elif volume > 800: # too loud
        cpb.pixels.fill((color, 0, 0))     # red
    else:             # just right
        cpb.pixels.fill((0, color, 0))     # green
    cpb.pixels.show()


while True:
    if cpb.light < threshold:               # starts the clock if light sensor is covered
        buzzLong()                          # initial buzz to tell user the clock has started
        iterate = numIterations() + 1       # determine number of iterations needed based on softpot value
        for i in range(0, (iterate)):       # loop through to ensure proper timing
            if cpb.light < threshold:       # break the loop if light sensor is covered again
                sleep(long)
                break
            elif i == (round(iterate/3)):   # buzz once if 1/3 of the way through
                buzzOnce()
            elif i == (round(2*iterate/3)): # buzz twice if 2/3 of the way through
                buzzTwice()
            elif i == iterate - 1:          # prolonged buzz at end of presentation time
                buzzLong()
            else:
                sleep(short)                # do nothing if not one of those timing cases
            volLights()                     # always illuminate the neopixels based on volume

    elif cpb.button_b:                      # if you press button b
        length = timerSet()                 # determines selected length of presentation based on softpot values
        for j in range(0,length):           # illuminates the number of neopixels that aligns with the number of minutes for the presentation
            cpb.pixels[j] = ((0, 0, color))
        cpb.pixels.show()
        sleep(long)


    sleep(short)
    cpb.pixels.fill((0,0,0))                # ensures reset to no illumination once out of loop
