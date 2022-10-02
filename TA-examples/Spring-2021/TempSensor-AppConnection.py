# Write your code here :-)
import board
import time
import adafruit_thermistor
import neopixel
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE,10000,10000,25,3950)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        temp_c=thermistor.temperature
        uart.write("{}\n".format(thermistor.temperature))
        print("Temp= %F" % (temp_c))
        if temp_c<27:
            pixels.fill((0,0,150))
        else:
            pixels.fill((0,0,0))
        time.sleep(1)
