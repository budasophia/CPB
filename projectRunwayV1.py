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

#-----------------------------------------------------------------------------
# This is where you make instances of your inputs and outputs (think arduino!)
#-----------------------------------------------------------------------------
board_pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)  # ([the neopixels you want to control], [how many], [brightness])
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
# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

# Make the input capacitive touchpads
capPins = (board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.TX)

touchPad = []
for i in range(7):
    touchPad.append(touchio.TouchIn(capPins[i]))
# The seven files assigned to the touchpads
audiofiles = [
    "bd_tek.wav",
    "elec_hi_snare.wav",
    "elec_cymbal.wav",
    "elec_blip2.wav",
    "bd_zome.wav",
    "bass_hit_c.wav",
    "drum_cowbell.wav",
]
audio = AudioOut(board.SPEAKER)


def play_file(filename):
    print("playing file " + filename)
    file = open(filename, "rb")
    wave = WaveFile(file)
    audio.play(wave)
    time.sleep(bpm / 960)  # Sixteenth note delay (eighth = 480, quarter = 240)


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


mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
samples = array.array("H", [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + 10
input_ceiling = input_floor + 500
peak = 0

# setting up buttons
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)  # this is important!! This debounces a button and makes it trigger reliably
button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

# -----------------------------------------------------------------------
# Select which demo to run! Put a 1 next to the demo you want to run
# Make sure all other demos = 0 when you run! Only one at a time!
temperature_sensor_demo = 0
rainbow_cycle_demo = 0
light_sensor_demo = 0
drum_machine_demo = 1  # touch the A1-A7 pads to hear a sound!
sound_meter_demo = 0
button_demo = 0
# -----------------------------------------------------------------------

# The main loop you put your code into
while True:
    if temperature_sensor_demo:
        temp_c = thermistor.temperature
        print("Temp= %F" % (temp_c))
        if temp_c < 29:
            # it is cold, so the neopixels are BLUE
            board_pixels.fill((0, 0, 150))  # (R, G, B)
        else:
            # it is warm, so the neopixels are RED
            board_pixels.fill((150, 0, 0))
        time.sleep(1)
    if rainbow_cycle_demo:
        for j in range(255):
            for i in range(10):
                rc_index = (i * 256 // 10) + j * 5
                board_pixels[i] = colorwheel(rc_index & 255)
        board_pixels.show()
        time.sleep(1)
    if light_sensor_demo:
        peak = simpleio.map_range(light.value, 2000, 62000, 0, 9)
        print(light.value)
        print(int(peak))

        for i in range(0, 9, 1):
            if i <= peak:
                board_pixels[i] = (0, 255, 0)
            else:
                board_pixels[i] = (0, 0, 0)
            board_pixels.show()
            time.sleep(0.01)
    if drum_machine_demo:
        for i in range(7):
            if touchPad[i].value:
                play_file(audiofiles[i])
    if sound_meter_demo:
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
        for i in range(10):
            if i < c:
                board_pixels[i] = volume_color(i)
            # Light up the peak pixel and animate it slowly dropping.
            if c >= peak:
                peak = min(c, 10 - 1)
            elif peak > 0:
                peak = peak - 1
            if peak > 0:
                board_pixels[int(peak)] = PEAK_COLOR
        board_pixels.show()
    if button_demo:
        if button_A.value:  # button is pushed
            board_pixels.fill((0, 53, 148))
        else:
            board_pixels.fill(0)
        if button_B.value:  # button is pushed
            board_pixels.fill((255, 184, 28))
        else:
            board_pixels.fill(0)
        time.sleep(0.001)
