import math
import pyaudio
import time

# Define constants for the audio
SAMPLE_RATE = 44100  # Hertz
VOLUME = 0.5  # Volume (range: 0.0 to 1.0)

# Define the frequencies for notes (in Hz)
NOTE_FREQS = {
    'C': 262,
    'E': 330,
    'G': 392,
    'A': 440,
    'REST': 0  # Rest
}

# Melody for "Also sprach Zarathustra" (simplified iconic opening)
MELODY = [
    'C', 'REST', 'C', 'REST', 'C', 'REST',
    'G', 'REST', 'A', 'REST', 'C', 'REST',
    'REST', 'REST', 'G', 'REST', 'C'
]
DURATIONS = [
    1.0, 0.5, 1.0, 0.5, 1.0, 0.5,  # Initial three Cs
    0.8, 0.4, 0.8, 0.4, 1.2, 0.6,  # Climactic G, A, and C
    1.0, 0.5, 1.0, 0.5, 2.0        # Rest and closing G to C
]

def generate_tone(frequency, duration):
    """Generate a tone at a given frequency and duration."""
    if frequency == 0:  # Handle REST
        time.sleep(duration)
        return b''

    samples = (int(SAMPLE_RATE * duration))
    wave = (VOLUME * math.sin(2 * math.pi * frequency * t / SAMPLE_RATE)
            for t in range(samples))
    return b''.join(int((s + 1) * 127.5).to_bytes(1, 'little') for s in wave)

def play_melody():
    """Play the melody."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt8,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True)

    for note, duration in zip(MELODY, DURATIONS):
        tone = generate_tone(NOTE_FREQS[note], duration)
        stream.write(tone)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    play_melody()

