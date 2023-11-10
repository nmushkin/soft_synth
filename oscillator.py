import numpy as np
from enum import Enum, auto

class Waveform(Enum):
    SINE = auto()
    SQUARE = auto()
    SAW = auto()
    TRIANGLE = auto()

class Oscillator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.frequency = 440  # default frequency A4
        self.waveform = Waveform.SINE  # default waveform
        self.attack_time = 0.01
        self.release_time = 0.01

    def set_frequency(self, frequency):
        self.frequency = frequency
    
    def set_envelope(self, attack_time=0.01, release_time=0.01):
        self.attack_time = attack_time
        self.release_time = release_time

    def set_waveform(self, waveform):
        if waveform in [Waveform.SINE, Waveform.SQUARE, Waveform.SAW, Waveform.TRIANGLE]:
            self.waveform = waveform
        else:
            raise ValueError("Waveform type not supported. Choose 'sine', 'square', 'saw', or 'triangle'.")
    
    def _generate_wave(self, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        if self.waveform == Waveform.SINE:
            return np.sin(self.frequency * t * 2 * np.pi)
        elif self.waveform == Waveform.SQUARE:
            return np.sign(np.sin(self.frequency * t * 2 * np.pi))
        elif self.waveform == Waveform.SAW:
            return 2 * (t * self.frequency - np.floor(0.5 + t * self.frequency))
        elif self.waveform == Waveform.TRIANGLE:
            return 2 * np.abs(2 * (t * self.frequency - np.floor(0.5 + t * self.frequency))) - 1


    def apply_envelope(self, audio):
        attack_samples = int(self.sample_rate * self.attack_time)
        release_samples = int(self.sample_rate * self.release_time)
        envelope = np.ones_like(audio)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        envelope[-release_samples:] = np.linspace(1, 0, release_samples)
        return audio * envelope

    def play(self, duration):
        wave = self._generate_wave(duration)
        audio = wave * (2**15 - 1) / np.max(np.abs(wave))
        audio = self.apply_envelope(audio)  # Apply the envelope to each note
        audio = audio.astype(np.int16)
        return audio

