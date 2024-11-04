import sounddevice as sd
from scipy.io.wavfile import write
import os

def record_audio(filename="audio/recording.wav", duration=5, sample_rate=44100):
    print("Entering record_audio")  # Debug print

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        print("Recording...")
        # Record audio using sounddevice
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save the recording to a WAV file
        write(filename, sample_rate, recording)
        print(f"Audio saved to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Exiting record_audio")  # Debug print
