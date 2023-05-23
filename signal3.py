from scipy import signal
import numpy as np


def fir_filter(cutoff, fs, numtaps):
    nyquist_frequency = fs / 2
    normalized_cutoff = cutoff / nyquist_frequency
    return signal.firwin(numtaps, normalized_cutoff)
def test_filter(signal, filter):
    return signal.convolve(filter, signal, mode='same')
if __name__ == "__main__":
    fs = 1000 
    cutoff = 100   
    numtaps = 101 
    signal = np.sin(2 * np.pi * 50 * np.arange(fs) / fs) + np.sin(2 * np.pi * 150 * np.arange(fs) / fs)
    filter = fir_filter(cutoff, fs, numtaps)
    filtered_signal = test_filter(signal, filter)
