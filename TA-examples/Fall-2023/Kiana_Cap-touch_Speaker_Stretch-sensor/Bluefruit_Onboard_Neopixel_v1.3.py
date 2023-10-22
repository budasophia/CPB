import board
import touchio
import audiopwmio
import time

# Create a capacitive touch pad
touch_pad = touchio.TouchIn(board.A0)

# Create an audio output object
audio = audiopwmio.PWMAudioOut(board.SPEAKER)

# Define the frequency for your tone (e.g., A440)
tone_frequency = 440.0

while True:
    if touch_pad.value:
        print("Touched!")
        # Play the tone when the copper tape is touched
        audio.frequency = int(tone_frequency)  # Set the frequency
        audio.play(volume=1.0)  # Play at full volume

        # Let the tone play for a brief duration (e.g., 0.5 seconds)
        time.sleep(0.5)

        # Stop the audio
        audio.stop()
