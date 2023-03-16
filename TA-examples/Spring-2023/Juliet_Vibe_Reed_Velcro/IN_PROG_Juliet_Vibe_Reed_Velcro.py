#Author: Juliet Varblow, Last modified 03/15/2023
#reed switch, vibe board, conductive velcro

#import necessary libraries first
import time #time: used to delay in code
import board #board: used to communicate with the CPB board
import digitalio #digitalio: used to configure CPB GPIO Pins
import touchio #import touch functionality

#initialize digital output to vibe board, on pin D10
vibe=digitalio.DigitalInOut(board.D10)
vibe.direction=digitalio.Direction.OUTPUT

#initialize reed switch as an input
switch=digitalio.DigitalInOut(board.D9)
switch.switch_to_input(
    pull=digitalio.Pull.DOWN
)

#initialize conductive velcro
velcro_pad=board.A4
velcro=touchio.TouchIn(velcro_pad)

#setting up vibration board (vibe board) to buzz
while True:
    if (switch.value and velcro.value) == False:
        vibe.value=True
    else
        vibe.value=False
