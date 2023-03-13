# Author: Bronco York
# Email: broncoyork@pitt.edu
# Date: 03/13/2023
# Version: 1.0
# Written for ENGR 0716/1716, the Art of Making, at the University of Pittsburgh

# Circuit Python demo of the Flora Colorimeter and Bluefruit on-board accelerometer

# Demo: Color sensor glove
# Setup:
# 1. Connect Flora Colorimeter to Bluefruit using the on-board SCL and SDA pins and power/ground. When powered, the Colorimeter's white light will illuminate.
# 2. Upload this code to the Bluefruit
# 3. Ensure that the Colorimeter is properly connected to the board and can communicate over I2C (check serial monitor)
# 4. Place the Colorimeter, white light down, against the object whose color you want to measure
# 5. Double tap the Bluefruit (adjust sensitivity as needed) and the colorimeter will read the color in RGB and output the same RGB value to the on-board neopixel ring

# import necessary libraries
import time
import board # library for on-board pin definitions
import adafruit_tcs34725 # library flora color sensor
import neopixel
import busio # library for I2C functions
import adafruit_lis3dh #library for the on-board Bluefruit accelerometer, which is the LIS3DH

# initialize the on-board accelerometer
i2c_accel = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA) #create an I2C bus object (i2c_accel) for the internal I2C bus used by the on-board accelerometer
accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c_accel, address=0x19) # create an object used for the accelerometer connected to the i2c_accel bus object
accelerometer.range = adafruit_lis3dh.RANGE_2_G #set the range of the accelerometer to be 2Gs (can be set to 2G, 4G, 8G, or 16G ranges)

# used for the built-in accelerometer detect bump function, the function will trigger when 2 bumps are detected with a threshold of 60 (check documentation about threshold)
accelerometer.set_tap(2, 60)

# initialize the colorimeter
i2c_board = board.I2C()  # create an I2C bus object (i2c_board) connected to the SCL and SDA pins on the Bluefruit (external pins on the perimeter)
color_sensor = adafruit_tcs34725.TCS34725(i2c_board) # create an object connected to the colorimeter on the i2c_board bus

num_pixels = 10; # Define number of pixels to use (this is the number of pixels onboard the Bluefruit)
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.5, auto_write=False) # create the pixels object connected to the onboard NeoPixels

# Main loop for color sensor accelerometer glove
while True:
    # wait for I2C connection
    while not i2c_board.try_lock():
        print("No I2C connection found on board pins")
        time.sleep(1000)

    # the colorimeter will read the color and output the color to the neopixels only when the Bluefruit is double tapped (detected by the on-board accelerometer)
    if accelerometer.tapped:
        color = color_sensor.color # read in color value from the sensor
        color_rgb = color_sensor.color_rgb_bytes # from the RGB color value from the sensor

        # print color values to the serial monitor
        print(
            "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
                color, color_rgb
            )
        )
        # Read the color temperature and lux of the sensor and print to the serial monitor
        temp = color_sensor.color_temperature
        lux = color_sensor.lux
        print("Temperature: {0}K Lux: {1}\n".format(temp, lux))

        pixels.fill(color_rgb) # set NeoPixel color to the RGB value read by the colorimeter
        pixels.show(); # once the NeoPixel color is set, refresh the NeoPixel to show the updated color

    # Delay for 200ms (0.2 seconds) and repeat.
    time.sleep(0.2)
