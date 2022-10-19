import board
import neopixel
import time
from adafruit_circuitplayground import cp
import digitalio
from analogio import AnalogIn

#onboard=neopixel.NeoPixel(board.D8,10,brightness=.5)
analog_in = AnalogIn(board.A3)
count = 0

while 1:
    #onboard.fill((255,255,255))
    if analog_in.value > 50000:
        cp.play_tone(262, 1)
        count = count + 1
        print(count)
        time.sleep(1)
    if count == 5:
        for x in range(5):
            #onboard.fill((0,0,255))
            cp.play_tone(262, 0.2)
            time.sleep(0.1)
            count = 0
    time.sleep(0.1)
