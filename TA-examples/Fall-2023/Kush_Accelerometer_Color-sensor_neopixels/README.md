## Digital Paint Mixer

### Use case: 

Help users learn how RGB values work analogous to mixing paint

### What it does: 

Captures two separate colors indicated by a light and sound countdown and a camera capture sound, and then mixes their rgb values when the apparatus is shaken accompanied by a swirling water sound and the swirling of the neopixel input indicators

### How it works:

Color Sensor captures input, and sets it to one of two inputs corresponding to onboard buttons. Does countdown and then reads in input
Accelerometer detects if apparatus is shaken, and if so, swirls the onboard neopixels and plays a swirling sound
The RGB tuples for the inputs are added and then outputted to the neopixels, with the output set as both inputs afterwards

### Peripherals:

**Digital Inputs:**
Onboard buttons

**Digital Outputs:**

**Analog Inputs:**
Color Sensor
Accelerometer

**"Analog" (PWM) Outputs:**
Speaker

**Serial Communication:**
Neopixels

### Demo Video: 
https://youtu.be/KlpYZOj_yqE

This demo system and video were developed for the user-centered design course ENGR 0716/1716 The Art of Making: Hands-On System Design and Engineering at the University of Pittsburgh Swanson School of Engineering © 2023.

