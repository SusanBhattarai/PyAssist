import sounddevice as sd
from scipy.io.wavfile import write
import wavio
fs = 44100  # Sample rate
seconds = 5  # Duration of recording
print("RECORDING")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
print("STOPPED")
wavio.write("raw_audio.wav", myrecording, fs,sampwidth=2) # Save as WAV file 
