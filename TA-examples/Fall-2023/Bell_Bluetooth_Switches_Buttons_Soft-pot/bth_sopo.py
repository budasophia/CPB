#SPDX-FileCopyrightText: 2019 John Edgar Park for Adafruit Industries
#
#SPDX-License-Identifier: MIT

"""
Circuit Playground Bluefruit Ornament Proximity
This demo uses advertising to set the color of scanning devices depending on the strongest broadcast
signal received. Circuit Playgrounds can be switched between advertising and scanning using the
slide switch. The buttons change the color when advertising.

Hi Makers! Hope this sample code is of interest to you! I'll try to explain as clearly and
as concisely as I can, especially as someone who had to spontaneously learn Python for this lol.
Please feel free to reach out if you have any questions! Spam my Piazza box. Please. -Bell
"""

#These contain important functions and definitions we'll need for our code.
import board, analogio, time

#For CPB board functions.
from adafruit_circuitplayground.bluefruit import cpb

#BLERadio allows us to initialize bluetooth broadcasting. "BLE" = Bluetooth Low Energy.
from adafruit_ble import BLERadio

#This special advertising library allows us to "advertise" the current color of the on-board neopixels across Bluetooth.
from adafruit_ble.advertising.adafruit import AdafruitColor

#The above imports are Mark's area of expertise,
#so if you have an inquiry about the imports Piazza him. -Bell

#This is very important line of code! It initializes our soft potentiometer as an input
# so we can read numbers from it. I have my soft potentiometer hooked up to pin A4.
softpot = analogio.AnalogIn(board.A4)

#Here, we define our array of colors.
color_options = [0x111100, #happy, yellow, 0
                 0x000011, #sad, blue, 1
                 0x110000, #pissed, red, 2
                 0x001100, #jealous, green, 3
                 0x110011, #in love, pink, 4
                 0x111111] #achieved nirvana, white, 5

#We intialize a bluetooth radio object that we can use later in the code to broadcast color data.
ble = BLERadio()

#We'll default the first color to the first hex value in the color array.
advertisement = AdafruitColor()
advertisement.color = color_options[0]

cpb.pixels.auto_write = False

#We'll also fill the on-bord neopixels with the same color that we are broadcasting.
cpb.pixels.fill(color_options[0])

while True:
    # The "broadcasting" mode reads in a value from the softpot, converts it to an integer,
    # and uses that integer to select a color from our color_options array.

    if cpb.switch:
        #Print statements are useful for knowing where we are in our code.
        print("Broadcasting color!")

        #With this line of code, we're now broadcasting our color to receiving bluefruits!
        ble.start_advertising(advertisement)

        #Basically, read in a value from the softpot, assign it to an integer which corresponds
        #to a color in the array, display it on the broadcasting bluefruit, and project it to
        #receiving bluefruits!
        while cpb.switch:
            color_num = min(5, max(0, int((softpot.value - 2000) / 9333)))
            cpb.pixels.fill(color_options[color_num])
            cpb.pixels.show()
            print(softpot.value)

            advertisement.color = color_options[color_num]
            ble.stop_advertising()
            ble.start_advertising(advertisement)
            time.sleep(0.5)
        ble.stop_advertising()

    #The second mode listens for color broadcasts and shows the color of the strongest signal.
    #The proximity sensor, essentially. If you have any questions about this, ask Mark. -Bell
    else:
        closest = None
        #RSSI = Received Strength Signal Indicator (dB)
        closest_rssi = -80
        closest_last_time = 0
        print("Scanning for colors")
        while not cpb.switch:
            for entry in ble.start_scan(AdafruitColor, minimum_rssi=-100, timeout=1):
                if cpb.switch:
                    break
                now = time.monotonic()
                if entry.address == closest:
                    pass
                elif entry.rssi > closest_rssi or now - closest_last_time > 0.4:
                    closest = entry.address
                else:
                    continue
                closest_rssi = entry.rssi
                closest_last_time = now
                discrete_strength = min((100 + entry.rssi) // 5, 10)
                cpb.pixels.fill(0x000000)
                for i in range(0, discrete_strength):
                    cpb.pixels[i] = entry.color
                cpb.pixels.show()

            # Clear the pixels if we haven't heard from anything recently.
            now = time.monotonic()
            if now - closest_last_time > 1:
                cpb.pixels.fill(0x000000)
                cpb.pixels.show()
        ble.stop_scan()
