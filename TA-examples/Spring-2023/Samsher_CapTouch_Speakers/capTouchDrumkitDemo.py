# Write your code here :-)
import board  # you always need to import these
import time  # two to make sure your board functions
import touchio
import digitalio

####################################
## CHOOSE YOUR SPEAKER ##
# make this variable True if you want to use the onboard speaker, False if you are using an external speaker
onboard = True

## CHOOSE YOUR TEMPO ##
bpm = 110  # Beats per minute, change this to suit your tempo
noteLength = 480 # Sixteenth note = 960, eighth = 480, quarter = 240
######################################

#-----------------------------------------------------------------------------
# This is where you make instances of your inputs and outputs (think arduino!)
#-----------------------------------------------------------------------------
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
speaker_enable.value = onboard

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
    time.sleep(bpm / noteLength)  # Sixteenth note delay = 960, eighth = 480, quarter = 240

# -----------------------------------------------------------------------

# The main loop you put your code into
while True:
    for i in range(7):
        if touchPad[i].value:
            play_file(audiofiles[i])
