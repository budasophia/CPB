# Write your code here :-)
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

try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass

frequency = 440
sampleRate = 8000

length = sampleRate // frequency
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audio = AudioOut(board.SPEAKER)
sine_wave_sample = RawSample(sine_wave)

def shutter():
    wave_file = open("shutter.wav", "rb")
    with WaveFile(wave_file) as wave:
        audio.play(wave)
        while audio.playing:
            pass


def mix(color1, color2):
    wave_file = open("slosh.wav", "rb")
    with WaveFile(wave_file) as wave:
        audio.play(wave)
        while audio.playing:
            pass
            for x in range(10):
                for i in range(9):
                    if i < 5:
                        pixels[(i + x)%10] = color1
                    else:
                        pixels[(i + x)%10] = color2
                pixels.show()

                time.sleep(.1)


i2c = board.I2C()
colorSensor = adafruit_tcs34725.TCS34725(i2c)

accelSensor = adafruit_lsm303_accel.LSM303_Accel(i2c)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)

buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

lightSenseOB = analogio.AnalogIn(board.LIGHT)

#def onBoardLightSense():
#
#    pixels[1] = (255, 0, 0)
#    pixels.show()
#    redRaw = lightSenseOB.value
#    #time.sleep(.1)
#
#    pixels[1] = (0, 255, 0)
#    pixels.show()
#    greenRaw = lightSenseOB.value
#    #time.sleep(.1)
#
#    pixels[1] = (0, 0, 255)
#    pixels.show()
#    blueRaw = lightSenseOB.value
    #time.sleep(.1)


#    pixels[1] = (0, 0, 0)
#   pixels.show()
#
#
#   #shutter()
#
#   maximum = max(redRaw, greenRaw, blueRaw)
#   minimum = min(redRaw, greenRaw, blueRaw)
#
#  red = simpleio.map_range(redRaw, minimum, maximum, 0, 255)
#   green = simpleio.map_range(greenRaw, minimum, maximum, 0, 255)
#   blue = simpleio.map_range(blueRaw, minimum, maximum, 0, 255)
#
#   if red < 30:
#       red = 0
#   if green < 30:
#       green = 0
#   if blue < 30:
#       blue = 0
#
#   r = int(red)
#   g = int(green)
#   b = int(blue)
#
#   value = (r, g, b)
#
#   #if maximum - minimum <= 30:
#   #    value = (0, 0, 0)
#
#   print("Maximum Light: %i" % (maximum))
#   print("Minimum Light: %i" % (minimum))
#   print("Raw RGB: {0} {1} {2}". format(redRaw, greenRaw, blueRaw))
#   print("Output RGB: {0} {1} {2} ". format(r, g, b))
#
#
#   return value

color1 = (0,0,0)
color2 = (0,0,0)


while True:
    # Button One Capture
    # Turn on one side of neopixels one by one, each one with a tone (3)
    # Play a click capture sound for the read of the onboard color sensor
    # Set neopixels to that captured color
    if buttonA.value:

        for i in range(5):
            pixels[i] = (0, 0, 0)
            pixels.show()

        time.sleep(.1)

        for i in range(3):
            pixels[i*2] = (255, 255, 255)
            audio.play(sine_wave_sample, loop=True)
            pixels.show()
            time.sleep(.75)
            audio.stop()
            time.sleep(.25)

        for i in range(5):
            pixels[i] = (0, 0, 0)
            pixels.show()

        time.sleep(.1)

        shutter()

        color1 = colorSensor.color_rgb_bytes

        for i in range(5):
            pixels[i] = color1
            pixels.show()



    if buttonB.value:

        for i in range(5):
            pixels[i + 5] = (0, 0, 0)
            pixels.show()

        time.sleep(.1)

        for i in range(3):
            pixels[9 - i*2] = (255, 255, 255)
            audio.play(sine_wave_sample, loop=True)
            pixels.show()
            time.sleep(.75)
            audio.stop()
            time.sleep(.25)

        for i in range(5):
            pixels[i + 5] = (0, 0, 0)
            pixels.show()

        time.sleep(.1)

        shutter()

        color2 = colorSensor.color_rgb_bytes

        for i in range(5):
            pixels[i + 5] = color2
            pixels.show()


    accX, accY, accZ = accelSensor.acceleration

    print((accX, accY, accZ))
    time.sleep(.3)
    if ((accX > 15) or (accY > 15) or (accZ > 15)):
        #for i in range(5):
        #    pixels[i + 5] = (0, 255, 0)
        #    color2 = (0, 255, 0)
        #    pixels.show()

        #for i in range(5):
        #    pixels[i] = (255, 0, 0)
        #    color1 = (255, 0, 0)
        #    pixels.show()

        for i in range(3):
            mix(color1, color2)
            time.sleep(.2)

        newColor = tuple(map(lambda i, j: i + j, color1, color2))

        if newColor[0] > 255:
            newColor = (255, newColor[1], newColor[2])
        if newColor[1] > 255:
            newColor = (newColor[0], 255, newColor[2])
        if newColor[2] > 255:
            newColor = (newColor[0], newColor[1], 255)

        for i in range(10):
            pixels[i] = newColor
        pixels.show()

        color1 = newColor
        color2 = newColor



    #print((accX, accY, accZ))
    time.sleep(.3)
