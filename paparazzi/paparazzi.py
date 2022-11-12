#AOM Paparazzi code!
import time
import board
from rainbowio import colorwheel
import neopixel
import audiobusio
import simpleio
import digitalio

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.05, auto_write=False)

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
audio = AudioOut(board.SPEAKER)

def play_file(filename):
    print("playing file " + filename)
    file = open(filename, "rb")
    wave = WaveFile(file)
    audio.play(wave)

play_file("freezeframe.wav")
time.sleep(1)

while True:
    play_file("click.wav")
    pixels.fill((150,150,150))
    pixels.show()
    time.sleep(0.25)
    pixels.fill(0)
    pixels.show()
    time.sleep(1)
    play_file("clickclick.wav")
    pixels.fill((150,150,150))
    pixels.show()
    time.sleep(0.15)
    pixels.fill(0)
    pixels.show()
    time.sleep(0.25)
    pixels.fill((150,150,150))
    pixels.show()
    time.sleep(0.2)
    pixels.fill(0)
    pixels.show()
    time.sleep(1.75)
