# Write your code here :-)
#import these libraries
import time
import board
import array
import math
import adafruit_tcs34725
import neopixel
import digitalio
import simpleio
import analogio
import adafruit_lsm303_accel

#importing audio libraries to play code-tone
try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

#importing audio library to play wav file
try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

#import library for AudioOut
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass

#parameters for constructing code-made tone
frequency = 440
sampleRate = 8000

#assemble code tone via sine wave sampling
length = sampleRate // frequency
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

#enable speaker output
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audio = AudioOut(board.SPEAKER) #configure audio out as audio var
sine_wave_sample = RawSample(sine_wave) #configure sine wave as audio sample

#play shutter sound for the color capture
def shutter():
    wave_file = open("shutter.wav", "rb")
    with WaveFile(wave_file) as wave:
        audio.play(wave)
        while audio.playing:
            pass

#mix function that plays sloshing and light-chases onboard neopixels
def mix(color1, color2):
    wave_file = open("slosh.wav", "rb")
    with WaveFile(wave_file) as wave:
        audio.play(wave)
        while audio.playing:
            pass
            for x in range(10):
                for i in range(9):
                    if i < 5:
                        pixels[(i + x)%10] = color1 #using modulo math to shift color1 one-by-one
                    else:
                        pixels[(i + x)%10] = color2 #using modulo math to shift color2 one-by-one
                pixels.show()

                time.sleep(.1)

#configure I2C for sensors
i2c = board.I2C()
colorSensor = adafruit_tcs34725.TCS34725(i2c) #initialize colorSensor
accelSensor = adafruit_lsm303_accel.LSM303_Accel(i2c) #initialize accelerometer

#initialize neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)

#initialize button A
buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)

#initialize button B
buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

#initialize two color inputs as RGB black
color1 = (0,0,0)
color2 = (0,0,0)


while True:
    # Button One Capture
    # Turn on one side of neopixels one by one, each one with a tone (3)
    # Play a click capture sound for the read of the onboard color sensor
    # Set neopixels to that captured color

    if buttonA.value: #pressed down Button A

        for i in range(5): #clear input 1 indicator neopixels
            pixels[i] = (0, 0, 0)
            pixels.show()

        time.sleep(.1) #wait

        for i in range(3): #countdown
            pixels[i*2] = (255, 255, 255) #set 0th, 2nd, 4th neopixel to white
            audio.play(sine_wave_sample, loop=True) #play beep tone
            pixels.show()
            time.sleep(.75)
            audio.stop() #stop tone
            time.sleep(.25)

        for i in range(5): #clear input 1 indicator neopixels
            pixels[i] = (0, 0, 0)
            pixels.show()

        time.sleep(.1) #wait

        shutter() #shutter function

        color1 = colorSensor.color_rgb_bytes #read colorSensor and set it to color1

        for i in range(5): #set input 1 indicator neopixels to color1
            pixels[i] = color1
            pixels.show()



    if buttonB.value:

        for i in range(5): #clear input 2 indicator neopixels
            pixels[i + 5] = (0, 0, 0)
            pixels.show()

        time.sleep(.1) #wait

        for i in range(3): #countdown
            pixels[9 - i*2] = (255, 255, 255) #set 9th, 7th, 5th neopixels to white
            audio.play(sine_wave_sample, loop=True) #play beep tone
            pixels.show()
            time.sleep(.75)
            audio.stop() #stop tone
            time.sleep(.25)

        for i in range(5): #clear input 2 indicator neopixels
            pixels[i + 5] = (0, 0, 0)
            pixels.show()

        time.sleep(.1) #wait

        shutter() #shutter function

        color2 = colorSensor.color_rgb_bytes #read colorSensor and set to color2

        for i in range(5): #set input 2 indicator neopixels to color2
            pixels[i + 5] = color2
            pixels.show()


    accX, accY, accZ = accelSensor.acceleration #read in accelerometer values

    #print((accX, accY, accZ)) #for debugging accelerometer values
    time.sleep(.3)
    if ((accX > 15) or (accY > 15) or (accZ > 15)): #if movement of vigorous intensity is detected

        for i in range(3): #run mix function 3 times
            mix(color1, color2)
            time.sleep(.2)

        newColor = tuple(map(lambda i, j: i + j, color1, color2)) #add up color1 and color2 tuples to get newColor

        #ensure RGB values do not exceed max values
        if newColor[0] > 255:
            newColor = (255, newColor[1], newColor[2])
        if newColor[1] > 255:
            newColor = (newColor[0], 255, newColor[2])
        if newColor[2] > 255:
            newColor = (newColor[0], newColor[1], 255)

        for i in range(10): #set all neopixels to newColor
            pixels[i] = newColor
        pixels.show()

        #set both inputs as the newColor
        color1 = newColor
        color2 = newColor

    time.sleep(.3)
