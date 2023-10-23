## PitchPacer | Piezo Buzzer, Soft Pot, Onboard Light Sensor, Onboard Mic

### Use case: 

This is a demo of a wearable device that gives you immediate feedback regarding volume and timing while rehearsing a presentation.

### What it does: 

The system sets a timer based on where you have slid the ring on the softpot. It starts the timer when you cover the light sensor with your hand. The piezo buzzer sounds at the start, 1/3 way point, 2/3 way point, and end, in order to aid in timing. While the timer is going, the neopixels illuminate yellow if you're too quiet, red if you're too loud, or green if you're talking at a good volume.

### How it works:

The system has 3 main inputs: the Soft Potentiometer, Onboard Light Sensor, and Onboard Microphone.

The Soft Potentiometer is configured as an analog input, with one end receiving 3.3V from the CPB, the other end connected to GND, and the sliding ring being connected to A4. As you slide the ring back and forth, you change the amount of resistance, and therefore the voltage that is input to the Bluefruit, which converts the voltage to a value between 0 and 65535. This is then split into bins to determine the number of minutes for the timer.

The Onboard Light Sensor is built-in to the CPB and is configured in the software by importing cpb from adafruit_circuitplayground.bluefruit. This enables it to read in values between 0 and 320. When the value gets below 10 (dark), the timer starts.

The Onboard Microphone is also built-in to the CPB and configured the same way as the Light Sensor. This reads in a wide range of values (from 0 to the tens of thousands). It is set up to determine if the volume falls in three different ranges: quiet (yellow), good (green), loud (red).

The system has 2 main outputs: the Piezo Buzzer and Onboard Neopixels.

The Piezo Buzzer is a PWM output device. It is connected to the AUDIO pin (D0) and received a PWM output with a specified frequency and duty cycle. A 50% duty cycle (2**15 in the code) turns it on, and a 0% duty cycle (0 in the code) turns it off. A higher frequency corresponds to a higher pitch.

The Onboard neopixels are built-in to the CPB and configured using the same intialization as the other oboard I/O. These are given an RGB value to determine what color to illuminate.

### Peripherals:

**Digital Inputs:**
Onboard Button

**Analog Inputs:**
Soft Potentiometer
Onboard Light Sensor
Onboard Microphone

**"Analog" (PWM) Outputs:**
Piezo Buzzer

**Serial Communication:**
Onboard Neopixels

### Demo Video:

https://youtu.be/pR5_DngGJlY

This demo system and video were developed for the user-centered design course ENGR 0716/1716 The Art of Making: Hands-On System Design and Engineering at the University of Pittsburgh Swanson School of Engineering © 2023.

