"""Bluetooth, Bluefruit App, and Onboard Temperature Sensor Demo"""

# Import necessary libraries
from time import sleep
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_circuitplayground.bluefruit import (cpb)
from adafruit_circuitplayground import cp
import board
import digitalio

# Define constants
COMPLETE_NAME_MAX_LEN = 8  # value found experimentally
OGTEMPERATURE_THRESHOLD = 28
temp = 0
BRIGHTNESS = 0.2

# Define and configure a digital input pin for a switch with a pulldown resistor
zipper_pin = digitalio.DigitalInOut(board.D9)
zipper_pin.switch_to_input(pull=digitalio.Pull.DOWN)

# Initialize Bluetooth, UART service, and advertising
ble = BLERadio()
uart_server = UARTService()
uart_advertisement = ProvideServicesAdvertisement(uart_server)
uart_connection = None

# Set the pixel brightness
cpb.pixels.brightness = 0.2

# Define color constants for LED colors
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

# Define a dictionary to map an index to a color
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

# Function to check if the zipper switch is closed
def zipper_Switch() -> bool:
    """Check the state of the zipper switch and return True if it's closed."""
    accept = zipper_pin.value  # Read the state of the zipper switch (0 for open, 1 for closed)
    return accept  # Return True if the switch is closed, indicating a closed zipper

# Function to scan for distress signals
def scan_for_temp(TEMPERATURE_THRESHOLD) -> bool:
    """
    Scan for distress signals and respond accordingly.

    This function scans for nearby devices advertising the UART service, which is used
    to transmit distress signals. It checks if the zipper switch is closed, and if so,
    it connects to the discovered device and handles distress signal data. If the temperature
    exceeds the threshold, it triggers a response and plays an audio alert.
    """
    print("Scanning for distress...")
    for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=0.1):
        if UARTService in advertisement.services:
            print("Located distress signal")
            ble.stop_scan()
            accept = zipper_Switch()  # Check if the zipper switch is closed
            if accept:
                uart_connection = ble.connect(advertisement)  # Connect to the discovered device
                sleep(0.5)
                print(f"Connected: {uart_connection.connected}")
                if uart_connection connected:
                    cpb.pixels.fill(MAGENTA)  # Set LED color to MAGENTA
                    uart_service = uart_connection[UARTService]
                    ble.start_advertising(uart_advertisement)
                    print("Advertising Started")
                    sleep(1)
                    while uart_connection.connected:
                        try:
                            temperature = (
                                uart_service.readline()
                                .decode("utf-8")
                                .strip()
                                .split(":")
                            )  # Read and decode temperature data
                            print(f"Received temperature: {temperature}")

                            if ble.connected:
                                uart_server.write(
                                    f"{temperature}\n"
                                )  # Send the temperature data to connected device
                                temp = temperature[0]  # Extract the temperature value
                                temp = float(temp)

                            if temp >= TEMPERATURE_THRESHOLD:
                                cpb.pixels.fill(RED)  # Set LED color to RED
                                cp.play_mp3("HOT.mp3")  # Play the "HOT" audio alert
                                accept = False  # Set 'accept' to False to indicate distress
                                break
                            else:
                                cpb.pixels.fill(WHITE)  # Set LED color to WHITE
                                cp.play_mp3("cold.mp3")  # Play the "cold" audio alert
                                accept = False  # Set 'accept' to False to indicate no distress
                                break

                            print("END OF TRY")

                        except Exception as e:
                            print(f"Error: {e}")
                            break
                    cpb.pixels.fill(BLACK)  # Set LED color to BLACK
                    ble.stop_advertising()
                    uart_connection.disconnect()
            break
    print("Scan for distress complete")

# Function to begin broadcasting a distress message
def advertise() -> None:
    """
    Start broadcasting a distress message and handle LED and BLE interactions.

    This function starts advertising the UART service to broadcast a distress signal.
    It also provides visual feedback with LEDs and audio feedback. It will stop broadcasting
    when a connection is established with a receiving device.
    """
    print("Distress broadcast started")
    ble.start_advertising(uart_advertisement)  # Start advertising the UART service
    pixel_pos = 0
    pixel_pos2 = 9
    cpb.pixels.fill(BLUE)  # Set LED color to BLUE
    color = PURPLE
    while True:
        print("Truth")
        if ble.connected:
            print("Connected")
            print(f"Writing {cpb.temperature}\n")
            uart_server.write(f"{cpb.temperature}\n")  # Send temperature data
            sleep(0.05)
            break
        else:
            cpb.pixels[pixel_pos] = color
            cpb.pixels[pixel_pos2] = color
            pixel_pos = (pixel_pos + 1)
            pixel_pos2 = (pixel_pos2 - 1)
            sleep(0.1)
            if pixel_pos == 5 and pixel_pos2 == 4:
                color = BLACK  # Transition LED color to BLACK
            if pixel_pos == 10 and pixel_pos2 == -1:
                color = PURPLE  # Reset LED color to PURPLE
                pixel_pos = 0
                pixel_pos2 = 9
    cpb.pixels.fill(BLACK)  # Set LED color to BLACK
    ble.stop_advertising()  # Stop advertising the UART service
    print("Distress broadcast stopped")

# Function to set temperature threshold based on user input
def temp_set(number):
    """
    Set the temperature threshold based on user input and provide visual and audio feedback.

    This function sets the distress temperature threshold based on user input.
    It plays an audio alert and changes LED colors to indicate the selected threshold.
    """
    if number == 1:
        TEMPERATURE_THRESHOLD = -1
        cp.play_mp3("30.mp3")  # Play the "30 degrees" audio alert
        cpb.pixels.fill(INDIGO)  # Set LED color to INDIGO
    elif number == 2:
        TEMPERATURE_THRESHOLD = 4
        cp.play_mp3("40.mp3")  # Play the "40 degrees" audio alert
        cpb.pixels.fill(BLUE)  # Set LED color to BLUE
    elif number == 3:
        TEMPERATURE_THRESHOLD = 10
        cp.play_mp3("50.mp3")  # Play the "50 degrees" audio alert
        cpb.pixels.fill(GREEN)  # Set LED color to GREEN
    elif number == 4:
        TEMPERATURE_THRESHOLD = 15
        cp.play_mp3("60.mp3")  # Play the "60 degrees" audio alert
        cpb.pixels.fill(YELLOW)  # Set LED color to YELLOW
    elif number == 5:
        TEMPERATURE_THRESHOLD = 21
        cp.play_mp3("70.mp3")  # Play the "70 degrees" audio alert
        cpb.pixels.fill(RED)  # Set LED color to RED
    return TEMPERATURE_THRESHOLD  # Return the selected temperature threshold

# Main loop
while True:
    if cpb.switch:
        # Switch is in the 'ON' position - Sender mode
        # Bluefruit Connected to Door
        # Check temperature and trigger distress signal
        advertise()

    else:
        # Switch is in the 'OFF' position - Receiver mode
        # Bluefruit on Jacket
        # Scan for a sender
        # Select Threshold Temperature
        count = 4
        temp_set(count)
        tempInt = OGTEMPERATURE_THRESHOLD
        sleep(0.1)
        while not cpb.button_b:
            if cpb.button_a:
                count += 1
                if count == 6:
                    count = 1
                tempInt = temp_set(count)
        cpb.pixels.fill(BLUE)
        sleep(1)
        print("GO")
        while True:
            print("GO")
            scan_for_temp(tempInt)
            sleep(0.5)

    print("\n\n")
