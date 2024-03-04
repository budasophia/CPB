## CPB TA Demo - Capacitive Touch with a Flower Craft

### Use case: 
Demo of using Capacitive touch to make a "wearable flower craft" light up

### What it does: 
The onboard neopixels light up when you touch the conductive materials. They light purple when you touch the copper tape on the flower petals and green when you touch the conductive fabric at the stem.

### How it works:
The system has 2 main inputs: the copper tape at pin A1, and the conductive fabric at pin A6. They are both configured to digital inputs with onboard capacitive touch. The pins A1 and A6 are configured as touchpads and are connected to the conductive material so that when you touch the material, it reads if the pin is touched. 
The system has one main output: on-board neopixels. If pin A1 or pin A6 reads in as being touched the onboard neopixels will turn on with the given RGB value for that pin. 

### Peripherals:

**Digital Inputs:**
On-board Capacitive Touch

**Serial Communication:**
On-board Neopixels

### Demo Video: 
https://www.youtube.com/watch?v=y2TmjlMetl8 
