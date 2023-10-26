"""Oday Bluetooth, Bluefruit App, and Onboard Temperature Sensor Demo
The Weather Sweater
A sweater that alerts you if it's too hot to wear a sweater outside via BlueTooth Communication. Concsists of two CPBs working together
one is a sender, the other is a receiver. This code operates both CPBs, the mode between the two is simply set via the CPB's onboard switch.

How to use:
    Turn on sender CPB (onboard switch in left position) and set it up outside
    
    Turn on receiver PCB (onboard switch in right position) and put the sweater it is connected to on (it can be zipped up now, or later, it shouldn't matter)
    
    Receiver PCB It will play and audio file to alert you what the current temperature threshold is to trigger an alert of whether it's too hot
    
    To change that threshold, press the A button to cycle through temperatures in degrees Fahrenheit between 30 and 70 (in increments of 10)
    
    The onboard neopixels will also illuminate to give a color representation of the temperature with PURPLE, BLUE, GREEN, YELLOW, & RED 
        associating with 30, 40, 50, 60 & 70 degrees respectively
        
    Press the B button to confirm the selection for the temperature threshold

    Approach the sender CPB which should be illuminating a growing and shrinking ring of Purple neopixels
    
    Zip up the sweater connected to the receiver PCB as a digital input with pulldown to ground, and the sweater will alert if 
        it's too hot to wear the sweater or if it's appropriate to wear it based on the temperature threshold set by the user

    Connect outdoor CPB to phone via Bluefruit Connect App to get a constant reading of outdoor temperature

Version 1.0 Oday Abushaban 10.23.2023
"""


## Import necessary libraries
# Used for timing and delays
from time import sleep
# Used for BlueTooth Connectivity
from adafruit_ble import BLERadio
# Used to create an advertisement that specifies the services provided by device over Bluetooth Low Energy (BLE)
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
# Used for the UART service that allows device to communicate over BLE using a UART (serial communication) interface
from adafruit_ble.services.nordic import UARTService
# Provides access to the features of the CPB, specifically temperature sensor, onboard buttons/switches, neopixels, and Bluetooth functionality
from adafruit_circuitplayground.bluefruit import (cpb)
# Used to play mp3 files which are saved onto the CPB
from adafruit_circuitplayground import cp
# Used to access pins on board for i/o connection
import board
# Used for Zipper Switch as a Digital Input
import digitalio


## Define constants
# Used as an initial value for temperature threshold in degrees Celsius
OGTEMPERATURE_THRESHOLD = 15
# Used to temporarily as a placeholder for a temperature float used in logic comparison later
temp = 0.0
# Set the neopixel brightness
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


## Initialize Bluetooth, UART service, and advertising
ble = BLERadio()
uart_server = UARTService()
uart_advertisement = ProvideServicesAdvertisement(uart_server)
uart_connection = None


## Define and configure a digital input pin for a switch with a pulldown resistor
zipper_pin = digitalio.DigitalInOut(board.D9)
zipper_pin.switch_to_input(pull=digitalio.Pull.DOWN)


## Functions
# Function to check if the zipper switch is closed
def zipper_Switch() -> bool:
    """Check the state of the zipper switch and return True if it's closed."""
    # Read the state of the zipper switch (0 for open, 1 for closed)
    accept = zipper_pin.value
    # Return True if the switch is closed, indicating a closed zipper
    return accept

# Function to scan for outdoor temperature
def scan_for_temp(TEMPERATURE_THRESHOLD) -> bool:
    """
    Scan for distress signals and respond accordingly.

    This function scans for nearby devices advertising the UART service, which is used
    to transmit live temperature. It checks if the zipper switch is closed, and if so,
    it connects to the discovered device and handles temperature data. If the temperature
    exceeds the threshold, it triggers a response and plays an audio alert.
    """
    print("Scanning for temperature data...")
    for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=0.1):
        if UARTService in advertisement.services:
            print("Located distress signal")
            ble.stop_scan()
            # Check if the zipper switch is closed
            accept = zipper_Switch()
            if accept:
                # Connect to the discovered device
                uart_connection = ble.connect(advertisement) 
                sleep(0.5)
                print(f"Connected: {uart_connection.connected}")
                if uart_connection connected:
                    # Set neopixel color to MAGENTA to indicate connection made
                    cpb.pixels.fill(MAGENTA)
                    # Create a UARTService object for communication
                    uart_service = uart_connection[UARTService]
                    # Start advertising a BlueTooth connection
                    ble.start_advertising(uart_advertisement)
                    print("Advertising Started")
                    sleep(1)
                    # Once a connection is made, temperature is extracted, converted to a float, then compared to the threshold temperature
                    while uart_connection.connected:
                        try:
                            # Read and decode temperature data
                            temperature = (
                                uart_service.readline()
                                .decode("utf-8")
                                .strip()
                                .split(":")
                            ) 
                            print(f"Received temperature: {temperature}")

                            if ble.connected:
                                # Send the temperature data to connected device
                                uart_server.write(f"{temperature}\n")
                                # Extract the temperature value
                                temp = temperature[0]
                                temp = float(temp)

                            if temp >= TEMPERATURE_THRESHOLD:
                                # Set neopixel color to RED to indicate it's too hot
                                cpb.pixels.fill(RED)
                                # Play the "HOT" audio alert
                                cp.play_mp3("HOT.mp3")
                                # Set 'accept' to False to allow loop to run again
                                accept = False
                                break
                            else:
                                # Set neopixel color to BLUE to indicate it's cold
                                cpb.pixels.fill(BLUE)
                                # Play the "cold" audio alert
                                cp.play_mp3("cold.mp3")
                                # Set 'accept' to False to allow loop to run again
                                accept = False
                                break

                        except Exception as e:
                            print(f"Error: {e}")
                            break
                    # Turn neopixels OFF
                    cpb.pixels.fill(BLACK)
                    ble.stop_advertising()
                    uart_connection.disconnect()
            break
    print("Scan for temperature complete")

# Function to begin broadcasting temperature
def advertise() -> None:
    """
    Start broadcasting recorded temperature and handle BLE interactions.

    This function starts advertising the UART service to broadcast temperature data.
    It provides neopixel feedback to indicate broadcasting is underway as it scans for a receiver.
    It will stop broadcasting when a connection is established with a receiving device.
    """
    print("Temperature broadcast started")
    # Start advertising the UART service
    ble.start_advertising(uart_advertisement)
    # Set initial pixel positions for neopixel broadcast indication
    pixel_pos = 0
    pixel_pos2 = 9
    # Set starter color to PURPLE for boradcasting neopixel animation
    color = PURPLE
    while True:
        print("Truth")
        # If the sweater with the other CPB is on, and zipped up, bluetooth connection begins
        if ble.connected:
            print("Connected")
            # Write Temperature to Serial Plotter
            print(f"Writing {cpb.temperature}\n")
            # Write Temperature to UART to send temperature data via BlueTooth to 
            # other CPB as well as any phones using the Bluefruit Connect App
            uart_server.write(f"{cpb.temperature}\n")
            sleep(0.05)
            break
        # Play neopixel broadcast animation to wait for connection to be established
        else:
            # Set pixels at position to whatever color is, PURPLE when ON, BLACK when OFF
            cpb.pixels[pixel_pos] = color
            cpb.pixels[pixel_pos2] = color
            # Increment and decrement pixel positions to create growing
            # and shrinking neopixel ring animation on the CPB
            pixel_pos = (pixel_pos + 1)
            pixel_pos2 = (pixel_pos2 - 1)
            sleep(0.1)
            # Once ring is fully colored PURPLE, need to unfill by coloring BLACK
            if pixel_pos == 5 and pixel_pos2 == 4:
                # Color constant set to BLACK for neopixels to turn OFF
                color = BLACK
            # Once ring is fully turned OFF (AKA BLACK), need to refill by coloring PURPLE
            if pixel_pos == 10 and pixel_pos2 == -1:
                # Color constant set to BLACK for neopixels to turn OFF
                color = PURPLE
                # Resetting pixel positions to restart animation
                pixel_pos = 0
                pixel_pos2 = 9
    # Turn neopixels OFF
    cpb.pixels.fill(BLACK)
    # Stop advertising the UART service
    ble.stop_advertising()
    print("Temperature broadcast stopped")

# Function to set temperature threshold based on user input
def temp_set(number):
    """
    Set the temperature threshold based on user input and provide visual and audio feedback.

    This function sets the distress temperature threshold based on user input.
    User input is tied to a number between 1 and 5 to set the temperature between 30 and 70 degrees.
    It plays an audio alert and changes LED colors to indicate the selected threshold.
    """
    if number == 1:
        TEMPERATURE_THRESHOLD = -1
        # Play the "30 degrees" audio alert
        cp.play_mp3("30.mp3")
         # Set neopixel color to PURPLE
        cpb.pixels.fill(PURPLE)
    elif number == 2:
        TEMPERATURE_THRESHOLD = 4
        # Play the "40 degrees" audio alert
        cp.play_mp3("40.mp3")
        # Set neopixel color to BLUE
        cpb.pixels.fill(BLUE)
    elif number == 3:
        TEMPERATURE_THRESHOLD = 10
        # Play the "50 degrees" audio alert
        cp.play_mp3("50.mp3")
        # Set neopixel color to GREEN
        cpb.pixels.fill(GREEN)
    elif number == 4:
        TEMPERATURE_THRESHOLD = 15
        # Play the "60 degrees" audio alert
        cp.play_mp3("60.mp3")
        # Set neopixel color to YELLOW
        cpb.pixels.fill(YELLOW)
    elif number == 5:
        TEMPERATURE_THRESHOLD = 21
        # Play the "70 degrees" audio alert
        cp.play_mp3("70.mp3")
        # Set neopixel color to RED
        cpb.pixels.fill(RED)
    # Return the selected temperature threshold    
    return TEMPERATURE_THRESHOLD


## Main loop
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
        # Count acts as input to temp_set
        # Count set to 4 (60 degrees as threshold)
        count = 4
        temp_set(count)
        tempInt = OGTEMPERATURE_THRESHOLD
        sleep(0.1)

        # Until B button is pressed, A button acts as a way to change between temperatures by being pressed repetitvely
        while not cpb.button_b:
            # Increment the count which is fed into the temp_set function
            if cpb.button_a:
                count += 1
                # Set count back to 1 (30 degrees) if A button is pressed after count reaches 5 (70 degrees)
                if count == 6:
                    count = 1
                tempInt = temp_set(count)
        # Turn neopixels GREEN to indicate selection has been made
        cpb.pixels.fill(GREEN)
        sleep(1)
        # Once threshold is set, repetitively scan for temperature
        while True:
            scan_for_temp(tempInt)
            sleep(0.5)

    print("\n\n")
