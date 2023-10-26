## Weather Sweater

### Use case: 

When you leave your home, sometimes the temperature outside is cold enough for a sweater and other times it's too hot. Checking the temperature can take time, and requires some internal thought for people to decide if it's too hot to wear a sweater. This can be especially troublesome when leaving the house in a rush.

### What it does: 

The Weather Sweater is a BlueTooth enabled sweater that behaves in accordance to the current temperature outside. If the temperature outside is too high, and the sweater is fully zipped up, the sweater will alert the user that it's too hot to wear a sweater. Otherwise the sweater will simply tell the user that they are perfectly finw wearing the sweater. The user can also connect the outdoor CPB to their phone via the Bluefruit Connect App to get a constant reading of the outdoor temperature (in Celsius)

### How it works:

The sweater's built in CPB first lets the user select the threshold temperature from a value between 30 to 70 (counting by 10s) to decide what temperature in degreees fahrenheit is too hot to wear the sweater. Once the user selects their desired threshold, the CPB waits for a BlueTooth advertisement to begin connecting. Meanwhile another CPB mounted outside a house is concstantly reading the temperature via it's onboard temperature sensor, once the user approaches close enough to the outdoor CPB, and zips up the sweater (the zipper acts as a digital input) the sweater reads the last recorded temperature from the outdoor CPB via UART transmission over BlueTooth, and then plays an audio file based on whether the recorded temperature is higher or lower than the set threshold. Audio is played via a STEMMA speaker hooked up to the CPB on the sweater and mounted on the shoulder of the sweater so the user can hear the audio clearly.

### Peripherals:

**Digital Inputs:** Zipper on Sweater acts as a Switch with a Pull Down Resistor to GND

**Digital Outputs:** None

**Analog Inputs: Onboard Temperature Sensor**

**"Analog" (PWM) Outputs:** STEMMA Speaker for Audio Output

**Serial Communication:** Onboard NeoPixels

### Video
https://youtu.be/8KztE3DbX6A

This demo system and video were developed for the user-centered design course ENGR 0716/1716 The Art of Making: Hands-On System Design and Engineering at the University of Pittsburgh Swanson School of Engineering © 2023.

