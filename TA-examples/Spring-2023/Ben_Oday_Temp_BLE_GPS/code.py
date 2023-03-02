"""Bluetooth, Bluefruit App, and Onboard Temperature Sensor Demo"""

from random import randint
from time import sleep

import adafruit_gps
import board
import busio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_circuitplayground.bluefruit import (
    cpb,
)  # use cpb.pixel and cpb.temperature when import cpb

COMPLETE_NAME_MAX_LEN = 8  # value found experimentally
TEMPERATURE_THRESHOLD = 28
BRIGHTNESS = 0.2

ble = BLERadio()
uart_server = UARTService()
uart_advertisement = ProvideServicesAdvertisement(uart_server)
uart_connection = None

# GPS setup
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=True)  # Use UART/pyserial
gps.send_command(b"PMTK220,1000")  # Set update rate to 1000 milliseconds (1Hz)
gps.send_command(
    b"PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
)  # send GGA sentences at update rate (1Hz)

cpb.pixels.brightness = 0.2

# Color constants
RED = (255, 0, 0)
MAGENTA = (255, 0, 20)
ORANGE = (255, 40, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
JADE = (0, 255, 40)
BLUE = (0, 0, 255)
INDIGO = (63, 0, 255)
VIOLET = (127, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLOR_ENUM = {
    0: MAGENTA,
    1: ORANGE,
    2: YELLOW,
    3: GREEN,
    4: JADE,
    5: BLUE,
    6: INDIGO,
    7: VIOLET,
    8: PURPLE,
    9: WHITE,
}


def get_gps_coords() -> list:
    """
    Attempt to get latitude and longitude coordinates from GPS
    Return [latitude, longitude] if successful, [0,0] otherwise
    """
    gps_update = gps.update()
    print(f"GPS update: {gps_update}")
    if gps_update:
        if gps.has_fix:
            print(f"Lat: {gps.latitude:.6f}, Long: {gps.longitude:.6f}")
            return [gps.latitude, gps.longitude]
        else:
            print("GPS does not have fix")
            return [0, 0]


def check_button_press() -> bool:
    """Check if either on board button has been press"""
    button_press = cpb.button_a or cpb.button_b
    if button_press:
        sleep(0.25)
    return button_press


def distress_indicator() -> bool:
    """Flash neopixels red and play alert until user accepts or declines"""
    accept = False
    while True:
        cpb.pixels.fill(RED)
        cpb.start_tone(frequency=1000)
        # Press button A to accept
        if cpb.button_a:
            print("Distress Signal Accepted")
            accept = True
            break
        # Press button B to decline
        if cpb.button_b:
            print("Distress Signal Declined")
            break
        sleep(0.1)
        cpb.pixels.fill(BLACK)
        cpb.stop_tone()
        sleep(0.1)
    cpb.stop_tone()
    cpb.pixels.fill(BLACK)
    sleep(0.25)
    return accept


def scan_for_distress(timeout: int = 0.1) -> bool:
    """Scan for any distress signals"""
    print("Scanning for distress...")
    for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=timeout):
        if UARTService in advertisement.services:
            print(f"Located distress signal")
            ble.stop_scan()
            accept = distress_indicator()
            if accept:
                uart_connection = ble.connect(advertisement)
                sleep(0.5)
                print(f"Connected: {uart_connection.connected}")
                if uart_connection.connected:
                    cpb.pixels.fill(BLACK)
                    uart_service = uart_connection[UARTService]
                    ble.start_advertising(uart_advertisement)
                    while uart_connection.connected and not check_button_press():
                        try:
                            color_num, temperature, gps_coords = (
                                uart_service.readline()
                                .decode("utf-8")
                                .strip()
                                .split(":")
                            )
                            for i in range(0, 10, 2):
                                cpb.pixels[i] = COLOR_ENUM[int(color_num)]
                            cpb.pixels.show()
                            print(f"Received temperature: {temperature}")
                            if ble.connected:
                                uart_server.write(
                                    f"{temperature},{gps_coords}\n"
                                )  # Write temperature from distress signal to Bluefruit App
                        except Exception as e:
                            print(f"Error: {e}")
                            break
                    cpb.pixels.fill(BLACK)
                    ble.stop_advertising()
                    uart_connection.disconnect()
            break
    print("Scan for distress complete")


def distress_broadcast() -> None:
    """Begin broadcast distress message"""
    print("Distress broadcast started")
    ble.start_advertising(uart_advertisement)
    pixel_pos = 0
    color_num = randint(0, 9)
    color = COLOR_ENUM[color_num]
    cpb.pixels.fill(BLACK)
    while not check_button_press():
        if ble.connected:
            cpb.pixels.fill(BLACK)
            for i in range(0, 10, 2):
                cpb.pixels[i] = color
            cpb.pixels.show()
            print("Connected")
            print(f"Writing {color_num}:{cpb.temperature}:{get_gps_coords()}\n")
            uart_server.write(f"{color_num}:{cpb.temperature}:{get_gps_coords()}\n")
            sleep(0.1)
        else:
            cpb.pixels[pixel_pos] = BLACK
            pixel_pos = (pixel_pos + 1) % 10
            cpb.pixels[pixel_pos] = RED
            cpb.pixels.show()
            sleep(0.05)
    cpb.pixels.fill(BLACK)
    ble.stop_advertising()
    print("Distress broadcast stopped")


def check_temperature() -> None:
    """Print temperature and flash and play tone if too hot"""
    print(f"Temperature: {cpb.temperature}")
    if cpb.temperature < TEMPERATURE_THRESHOLD:
        return
    for _ in range(2):
        cpb.pixels.fill(RED)
        cpb.start_tone(frequency=2000)
        sleep(0.1)
        cpb.pixels.fill(BLACK)
        cpb.stop_tone()
        sleep(0.1)


while True:

    # Broadcast help message if button pressed
    if check_button_press():
        distress_broadcast()

    # Check for distress signals
    scan_for_distress()

    # Check temp sensor
    check_temperature()

    print("\n\n")
