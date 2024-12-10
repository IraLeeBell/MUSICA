import math
import pyaudio
import time

# Define constants for the audio
SAMPLE_RATE = 44100  # Hertz
VOLUME = 0.5  # Volume (range: 0.0 to 1.0)

NOTE_FREQS = {
    'C': 262, 'E': 330, 'G': 392, 'F': 349, 'D': 294, 'A': 440, 'REST': 0
}

MELODY = [
    'E', 'G', 'A', 'F', 'REST', 'D', 'C', 'E',
    'G', 'A', 'REST', 'C', 'D', 'G', 'A', 'F'
]

DURATIONS = [
    0.8, 0.6, 0.8, 0.6, 0.2, 0.8, 0.6, 0.6,
    0.8, 0.6, 0.2, 0.6, 0.6, 0.8, 0.8, 1.0
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

