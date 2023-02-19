""" Bluefruit_SafetyBeacon
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.1 Amelia Glenn 2/11/2022

Last modified:
Benjamin Esquieres 02/17/2023
Changes:
Formatting and comments, fix duty cycle code
"""

import board  # import board module to access board's pins
from analogio import AnalogIn  # import AnalogIn from analogio module to access analog input/output
import pwmio  # import pwmio module to generate Pulse-width Modulation signals

analog_input = AnalogIn(board.A3)  # analog_input is an analog input connected to pin A3
pwm_output = pwmio.PWMOut(board.A2)  # pwm_output is a PWM output (default frequency of 500Hz) connected to pin A2

"""The digitized value of the analog input ranges from 0 to 65535.
(The Bluefruit has 16-bit analog-to-digital conversion, yielding 65536 unique digital values.)
Note that analog output is not "true analog": it will be a pulse width modulated (PWM) square wave."""
MAX_ANALOG_VOLTAGE = 65535

while True:  # loop until program terminates, analogous to void loop() in Arduino
    "Write the digitized analog input value to the serial monitor. To view: Ctrl+Shift+M (PC) or Cmd+Shift+M (Mac)"

    """Light brightens"""
    for i in range(0, MAX_ANALOG_VOLTAGE, 15):  # for i = 0, 5, 10, ... , 65530
        duty_cycle = int((analog_input.value / MAX_ANALOG_VOLTAGE) * i)  # scale i by the voltage level reading from analog_input to calculate PWM duty cycle
        pwm_output.duty_cycle = duty_cycle  # set pwm_output duty cycle to set the brightness of the LED (increase duty cycle to increase brightness)
        print(f"Duty Cycle: {duty_cycle} ({int(duty_cycle * 100 / MAX_ANALOG_VOLTAGE)}%)")  # print duty cycle to serial monitor

    """Light dims"""
    for i in range(MAX_ANALOG_VOLTAGE, 0, -15):  # for i = 65535, 65530, 65525, ... , 5
        duty_cycle = int((analog_input.value / MAX_ANALOG_VOLTAGE) * i)
        pwm_output.duty_cycle = duty_cycle
        print(f"Duty Cycle: {duty_cycle} ({int(duty_cycle * 100 / MAX_ANALOG_VOLTAGE)}%)")
