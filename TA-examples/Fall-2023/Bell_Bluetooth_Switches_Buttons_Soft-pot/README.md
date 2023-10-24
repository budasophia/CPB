## Wear your Heart on your Sleeve

### Use case + What it Does:

This is a simple Wearables project that allows users to broadcast their mood to surrounding Bluefruits (stakeholders?) using a soft potentiometer fashioned from a piece of conductive fabric and a small jewelry ring. By sliding the ring along the fabric, you can change the advertising color of the Bluefruit, from yellow for elation, to blue for melancholy; the list is variable and tailored to the user. For days when you're having difficulty expressing your emotions, or are simply too exhausted to communicate, it's nice to be able to quite literally wear your heart on your sleeve.  

### How it works:

Taking a look at your CPB, if you look inwards from the JST battery connector (black port directly across from the Micro USB jack) and orient it so that it faces south, you'll see an onboard slide switch with a small Bluetooth symbol next to it. There are two configurations: the left "broadcasting" configuration and the right "receiving" configuration.

- When the switch is in the left position, the Bluefruit is broadcasting data into its surrounding environment. The broadcasted data can take a number of different forms, for example, color, position, etc.

- When the switch is in the right position, the Bluefruit is monitoring its surrounding environment and pulling in data from neighboring Bluefruits.

Mark, one of your Maker Guest Stars (and one of my past TAs!) also has a built-in proximity sensor from last year that calculates how far away the receiving Bluefruit is from the broadcasting Bluefruit and reflects this distance by illuminating a number of neopixels that is proportional to the proximity of the broadcasting Bluefruit.

The Mood Cuff has a broadcasting Bluefruit embedded within the "cuff" itself. It will read in values from the soft potentiometer (sliding the ring will change the resistance of the potentiometer, which is what the Bluefruit reads in), convert them into array indexes, and choose from a list of various colors, which are meant to be indicative of the user's mood. The broadcasting Bluefruit will not only display the color on its onboard NeoPixels, but it will also advertise its color to nearby receiving Bluefruits. 

### Peripherals:

**Digital Inputs:**
Onboard Slide Switch

**Digital Outputs:**
Onboard Neopixels

**Analog Inputs:**
Soft Potentiometer

**"Analog" (PWM) Outputs:**
None

**Serial Communication:**
Bluetooth Low Energy (BLE) On-board

### Demo Video: 
https://youtu.be/GrCDLG4bVjI

This demo system and video were developed for the user-centered design course ENGR 0716/1716 The Art of Making: Hands-On System Design and Engineering at the University of Pittsburgh Swanson School of Engineering © 2023.

