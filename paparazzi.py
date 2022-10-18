#AOM Paparazzi code!
import time
import board
from rainbowio import colorwheel
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)

while True:
    pixels.fill((150,150,150))
    pixels.show()
    time.sleep(0.25)
    pixels.fill(0)
    pixels.show()
    time.sleep(0.25)

