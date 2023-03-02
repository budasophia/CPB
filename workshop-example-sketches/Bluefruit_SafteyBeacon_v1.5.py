""" Bluefruit_SafteyBeacon_v1.5.py
Developed for The Art of Making: An Introduction to Hands-On System Design and Engineering
University of Pittsburgh Swanson School of Engineering
v1.1 Amelia Glenn 2/11/2022

Latest version: v1.5

Last modified: Joseph Samosky 03/01 - 03/02/2023
Changed print statement to print maximum duty cycle reached during one brighten-dim cycle
Set increment/decrement value used in for loops to 10, which results in an ~1 Hz flash rate
Updated comments. Updated serial monitor comments in v1.5
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

    """Light brightens"""
    for i in range(0, MAX_ANALOG_VOLTAGE, 10):  # for i = 0, 10, 20, ... , 65530   Step size of 10 determined by iterative trials to achieve an ~ 1 Hz flashing rate
        duty_cycle = int((analog_input.value / MAX_ANALOG_VOLTAGE) * i)  # scale i by the voltage level reading from analog_input to calculate PWM duty cycle
        pwm_output.duty_cycle = duty_cycle  # set pwm_output duty cycle to set the brightness of the LED (increase duty cycle to increase brightness)

    # Print the maximum duty cycle to the serial monitor so you can see how the maximum value changes (along with the LED brightness) as you turn the potentiometer
    # To view the serial monitor in Mu click the Serial icon at the top of the editor window
    print(f"Maximum Duty Cycle: {pwm_output.duty_cycle}/{MAX_ANALOG_VOLTAGE} ({(pwm_output.duty_cycle * 100 / MAX_ANALOG_VOLTAGE):.0f}%)")

    """Light dims"""
    for i in range(MAX_ANALOG_VOLTAGE, 0, -10):  # for i = 65535, 65525, 65515, ... , 5
        duty_cycle = int((analog_input.value / MAX_ANALOG_VOLTAGE) * i)  # scale i by the voltage level reading from analog_input to calculate PWM duty cycle
        pwm_output.duty_cycle = duty_cycle  # set pwm_output duty cycle to set the brightness of the LED (decrease duty cycle to decrease brightness)
# Write your code here :-)
