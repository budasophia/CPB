'''CPB_capTouch-Sound v1.0 
Description: A sketch demonstrating how capacitive touch can trigger CircuitPhython Bluefruit's audio output
Author: Mark Hofmeister 2/25/2022
Last Modified: 2/25/2022'''

#import neccessary libraries

# time: used to delay in code
import time

# array: used to store sine wave values
import array

# math: used to compute values for the sine wave
import math

# board: used to communicate with the CPB board
import board

# digitalio: used to configure CPB GPIO pins
import digitalio

# touchio: used to enable capacitive touch on analog input pins
import touchio

#try to import audio library options
try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  
        
# Audio signal construction parameters
FREQUENCY = 440  # 440 Hz middle 'A'
SAMPLERATE = 8000  # 8000 samples/second, fancy DSP talk

# Generate one period of a sine wave
length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

#set audio to sound wave
audio = AudioOut(board.SPEAKER)
sine_wave_sample = RawSample(sine_wave)

#enable A1 as capacitive touch input
touch_A1 = touch_A1 = touchio.TouchIn(board.A1)

while True:

    if touch_A1.value:      # if the capacitive touch pin senses an input
        audio.play(sine_wave_sample, loop=True)  # Play the play a single sine wave at the given frequency
        time.sleep(1)  # for the duration of the sleep (in seconds)
        audio.stop()  # stop audio output.

    time.sleep(0.01)
    
    
    
    
    
    