# Write your code here :-)
import board  # you always need to import these
import time  # two to make sure your board functions
import adafruit_thermistor  # this is for the on-board temperature sensor
import neopixel  # this is for your on-board and off-board neopixels
from rainbowio import colorwheel
import analogio
import simpleio
import touchio
import digitalio
import array
import math
import audiobusio
import pulseio
import pwmio

#-----------------------------------------------------------------------------
# This is where you make instances of your inputs and outputs (think arduino!)
#-----------------------------------------------------------------------------
board_pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
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
# Color of the peak pixel.
PEAK_COLOR = (100, 0, 255)
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)
NUM_SAMPLES = 160

# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


# Scale input_value between output_min and output_max, exponentially.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / (input_max - input_min)
    return output_min + math.pow(normalized_input_value, SCALE_EXPONENT) * (
        output_max - output_min
    )


# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(float(sample - minbuf) * (sample - minbuf) for sample in values)

    return math.sqrt(samples_sum / len(values))


def mean(values):
    return sum(values) / len(values)


def volume_color(volume):
    return 200, volume * (255 // 10), 0



mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
sample_rate=16000, bit_depth=16)
samples = array.array("H", [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + 10
input_ceiling = input_floor + 500
peak = 0

# setting up buttons
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

buzzer = pwmio.PWMOut(board.AUDIO)
OFF = 0
ON = 2**15

# -----------------------------------------------------------------------
# Select which demo to run! Put a 1 next to the demo you want to run
# Make sure all other demos = 0 when you run! Only one at a time!
light_sensor_demo = 1
sound_meter_demo = 0
# -----------------------------------------------------------------------

# The main loop you put your code into
while True:
    if light_sensor_demo:
        print(light.value)
        mic.record(samples, len(samples))
        magnitude = normalized_rms(samples)
        print(magnitude)
        c = log_scale(
            constrain(magnitude, input_floor, input_ceiling),
            input_floor,
            input_ceiling,
            0,
            10,
        )
        board_pixels.fill(0)
        if light.value >= 500:
            board_pixels[9] = (0, 255, 255)
            buzzer.duty_cycle = ON
        elif magnitude >= 1100:
            board_pixels[9] = (255, 0, 0)
            break
        board_pixels.show()
        time.sleep(0.01)