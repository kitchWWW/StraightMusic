import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = ( np.sin(2*np.pi*np.arange(fs*duration)*f/fs) ).astype(np.float32)
samples = samples * volume

f = 1.0
samples2 = ( np.sin(2*np.pi*np.arange(fs*duration)*f/fs) ).astype(np.float32)

print len(samples)
samples2 = np.arange(duration * fs) / fs 

samples2 = samples2 * 1


print len(samples2)

print samples
print samples2

res = np.multiply(samples2,samples)

plt.plot(res)
plt.show()

scaled = np.int16(res/np.max(np.abs(res)) * 32767)

write('test.wav', 44100, scaled)
