"""Bluetooth, Bluefruit App, and Onboard Temperature Sensor Demo"""

from random import randint
from time import sleep

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_circuitplayground.bluefruit import (
    cpb,
)  # use cpb.pixel and cpb.temperature when import cpb

COMPLETE_NAME_MAX_LEN = 8  # value found experimentally
TEMPERATURE_THRESHOLD = 28

ble = BLERadio()
uart_server = UARTService()
uart_advertisement = ProvideServicesAdvertisement(uart_server)
uart_connection = None

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
                    uart_service = uart_connection[UARTService]
                    ble.start_advertising(uart_advertisement)
                    while uart_connection.connected and not check_button_press():
                        color_num, temperature = (
                            uart_service.readline().decode("utf-8").strip().split(":")
                        )
                        cpb.pixels.fill(COLOR_ENUM[int(color_num)])
                        print(f"Received temperature: {temperature}")
                        if ble.connected:
                            uart_server.write(
                                f"{temperature}\n"
                            )  # Write temperature from distress signal to Bluefruit App
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
    while not check_button_press():
        if ble.connected:
            cpb.pixels.fill(COLOR_ENUM[color_num])
            # TODO write GPS
            print("Connected")
            print(f"Writing {cpb.temperature}\n")
            uart_server.write(f"{color_num}:{cpb.temperature}\n")
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
