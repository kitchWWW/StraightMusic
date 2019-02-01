import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


freqF = 87.307


fs = 44100       # sampling rate, Hz, must be integer
totalDuration = 540 # in seconds
totalRes = np.zeros(fs*totalDuration)

def genSinWave(dur,freq):
	duration = float(dur)   # in seconds, may be float
	f = float(freq)        # sine frequency, Hz, may be float
	samples = ( np.sin(2*np.pi*np.arange(fs*duration)*f/fs) ).astype(np.float32)
	return samples

def genWaveEnvelope(fadeIn,sustain,fadeOut):
	fadeIn = np.arange(float(fadeIn) * fs) / fs 
	sustain = np.ones(sustain* fs)
	fadeOut = np.arange(float(fadeOut) * fs,0,-1) / fs 
	p1 = np.append(fadeIn,sustain)
	p2 = np.append(p1,fadeOut)
	return p2

def addToTotal(waveData,startPoint):
	global totalRes
	emptyBefore = np.zeros(startPoint * fs)
	emptyAfter = np.zeros(((totalDuration - startPoint) * fs) - len(waveData))
	addLayer = np.append(emptyBefore,waveData)
	addLayer = np.append(addLayer,emptyAfter)
	totalRes = np.add(totalRes,addLayer)

def genWave(freq,fadeIn,sustain,fadeOut):
	return np.multiply(genSinWave(fadeIn+sustain+fadeOut,freq),genWaveEnvelope(fadeIn,sustain,fadeOut))

for i in range(100):
	addToTotal(genWave(freqF,15,10,2),5)




scaled = np.int16(totalRes/np.max(np.abs(totalRes)) * 32767)

write('test.wav', 44100, scaled)
