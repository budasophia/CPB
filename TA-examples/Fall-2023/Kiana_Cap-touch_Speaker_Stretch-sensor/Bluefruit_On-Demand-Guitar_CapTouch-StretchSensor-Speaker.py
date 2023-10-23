import board  # you always need to import these
import time  # two to make sure your board functions
import adafruit_thermistor  # this is for the on-board temperature sensor
import neopixel  # this is for your on-board and off-board neopixels
import analogio
import touchio
import digitalio
import audiobusio

#-----------------------------------------------------------------------------
# This is where you make instances of your inputs and outputs (think arduino!)
#-----------------------------------------------------------------------------
light = analogio.AnalogIn(board.LIGHT)
bpm = 110  # Beats per minute, change this to suit your tempo
try:  # for the drum machine
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

# Make the input capacitive touchpads
capPins = (board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.TX)

touchPad = []
for i in range(4):
    touchPad.append(touchio.TouchIn(capPins[i]))

# The seven files assigned to the touchpads
audiofiles = [
    "g.wav",
    "b.wav",
    "high-e.wav",
    "d.wav"
]
audio = AudioOut(board.SPEAKER)

def play_file(filename):
    print("playing file " + filename)
    file = open(filename, "rb")
    wave = WaveFile(file)
    audio.play(wave)
    time.sleep(bpm / 200)  # Sixteenth note delay (eighth = 480, quarter = 240)


# Stretch sensor setup (make sure to connect your stretch sensor)
stretch_sensor = analogio.AnalogIn(board.A6)

# Define a threshold value for stretch sensor activation
stretch_threshold = 47000

# The main loop you put your code into
while True:
    for i in range(4):
        # Read the stretch sensor value
        stretch_value = stretch_sensor.value
        print(stretch_value)
        time.sleep(0.1)

        # Check if the stretch sensor value is above the threshold and touchpad is touched
        if touchPad[i].value and stretch_value > stretch_threshold:
            play_file(audiofiles[i])
