# Write your code here :-)
import board
import neopixel
import digitalio
import time
import busio
import adafruit_lis3dh

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket

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
        pass  # not always supported by every board!

# Enable the speaker
spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

led1 = digitalio.DigitalInOut(board.A1)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.A3)
led2.direction = digitalio.Direction.OUTPUT
buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)
buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)
switchA = digitalio.DigitalInOut(board.A2)
switchA.direction = digitalio.Direction.INPUT
switchA.pull = digitalio.Pull.UP

# The two files assigned to buttons A & B
#audiofiles = "Ding.wav"
#sound = audiofiles
audiofiles = ["Ding.wav", "LetsGOOO.wav", "GreatJob.wav", "Amazing.wav"]
sound = audiofiles[0]

exercise=1

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)

i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

lis3dh.set_tap(1, 127)



# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
#lis3dh.range = adafruit_lis3dh.RANGE_2_G

def play_file(filename):
    #print("Playing file: " + filename)
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass
    #print("Finished")

a, b, c = lis3dh.acceleration
time.sleep(0.5)
d, e, f = lis3dh.acceleration

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:

        #press button A to set position 1
        if buttonA.value == True:
            a, b, c = lis3dh.acceleration
            #print(a, b, c)
            time.sleep(0.5)

        #press button B to set position 2 (this is the position that will trigger a sound
        if buttonB.value == True:
            d, e, f = lis3dh.acceleration
            print(d, e, f)
            time.sleep(0.5)

        #as loop runs, this will continuously update the x, y, and z variables with the current acceleration data.
        x, y, z = lis3dh.acceleration
        #print(x, y, z)


        #if the y acceleration value collected from button A is higher than the y acceleration value collected from button B
        if e<b:
            if y<=e:
                pixels.fill((2, 14, 0))
                #play_file(sound)
            elif y>e:
                pixels.fill((14, 0, 0))

        #if the y acceleration value collected from button A is Lower than the y acceleration value collected from button B
        if e>b:
            if y<e:
                pixels.fill((14, 0, 0))
            elif y>=e:
                pixels.fill((2, 14, 0))
                #play_file(sound)

        time.sleep(0.05)


    # Now we're connected

    while ble.connected:
        x, y, z = lis3dh.acceleration
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, ButtonPacket):
                if packet.pressed:

                    #up button ~ push up
                    if packet.button == ButtonPacket.UP:
                        print("UP button pressed!")
                        exercise=1

                    #down button ~ leg lifts
                    if packet.button == ButtonPacket.DOWN:
                        print("DOWN button pressed!")
                        exercise=2
                    #left button ~ squats
                    elif packet.button == ButtonPacket.LEFT:
                        print("LEFT button pressed!")
                        exercise=3

                    #right button ~ bicep curls
                    elif packet.button == ButtonPacket.RIGHT:
                        print("RIGHT button pressed!")
                        exercise=4

                    #button 1 sets audio to default "ding" sound
                    elif packet.button == ButtonPacket.BUTTON_1:
                        print("1 button pressed!")
                        sound=audiofiles[0]

                    #button 2 sets audio to sound
                    elif packet.button == ButtonPacket.BUTTON_2:
                        print("2 button pressed!")
                        sound=audiofiles[1]

                    #button 3 sets audio to sound
                    elif packet.button == ButtonPacket.BUTTON_3:
                        print("3 button pressed!")
                        sound=audiofiles[2]

                    #button 4 sets audio to sound
                    elif packet.button == ButtonPacket.BUTTON_4:
                        print("4 button pressed!")
                        sound=audiofiles[3]

            #if isinstance(packet, ColorPacket):
                #print(packet.color)
                #pixels.fill(packet.color)

        if exercise == 1: #push up
            if y<=2.5:
                pixels.fill((2, 14, 0))
                play_file(sound)
            if y>2.5:
                pixels.fill((14, 0, 0))
        elif exercise == 2: #leg lift
            if y>=7:
                pixels.fill((2, 14, 0))
                play_file(sound)
            if y<7:
                pixels.fill((14, 0, 0))
        elif exercise == 3: #squats
            if y<=5:
                pixels.fill((2, 14, 0))
                play_file(sound)
            if y>5:
                pixels.fill((14, 0, 0))
        elif exercise == 4: #bicep curls
            if y>=9:
                pixels.fill((2, 14, 0))
                play_file(sound)
            if y<9:
                pixels.fill((14, 0, 0))

        #if buttonA.value == True:
            #print("button A pressed")
            #led1.value = True
            #time.sleep(0.5)

        #if buttonB.value == True:
            #play_file(audiofiles[1])
            #print("button B pressed")
            #led1.value = False
            #time.sleep(0.5)

        #if switchA.value == True:
            #print("switch off")
            #led2.value = False
            #time.sleep(0.5)

        #if switchA.value == False:
            #print("switch on")
            #led2.value = True
            #time.sleep(0.5)

        #if lis3dh.shake(shake_threshold=13):
            #print("Shaken!")
            #play_file(audiofiles)

        #if lis3dh.tapped:
            #print("Tapped!")
            #time.sleep(0.05)

        #if y<=5:
            #pixels.fill((2, 14, 0))
            #play_file(audiofiles)

        #if y>5:
            #pixels.fill((14, 0, 0))

        #led1.value = True
        #time.sleep(0.5)
        #led1.value = False
        #time.sleep(0.5)
        #led1.value = True
        #time.sleep(0.5)
        #led1.value = False
        #time.sleep(0.5)

    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
