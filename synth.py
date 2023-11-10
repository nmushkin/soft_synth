# Frequencies for the melody of "Hot Cross Buns"
from scipy.io.wavfile import write
import numpy as np
from oscillator import Oscillator, Waveform


hot_cross_buns_melody = [
    329.63,  # E
    293.66,  # D
    261.63,  # C
    329.63,  # E
    293.66,  # D
    261.63,  # C
    261.63,  # C
    261.63,  # C
    261.63,  # C
    293.66,  # D
    293.66,  # D
    293.66,  # D
    293.66,  # D
    329.63,  # E
    293.66,  # D
    261.63   # C
]

# Create the Oscillator instance
osc = Oscillator()

# A placeholder for the full melody
full_melody = np.array([], dtype=np.int16)

# Play the melody once using each Waveform
for i in Waveform:
    osc.set_waveform(i)
    # Play each note in the melody
    for freq in hot_cross_buns_melody:
        osc.set_frequency(freq)
        # Add each note to the full melody
        # Here, each note's duration is 0.5 second
        full_melody = np.concatenate((full_melody, osc.play(.5)))

# Save the full melody to a file
melody_wav_file = './data/hot_cross_buns.wav'
write(melody_wav_file, osc.sample_rate, full_melody)