import time
import numpy as np
from rtlsdr import RtlSdr

sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 100e6
sdr.gain = 'auto'
start_freq = 90e6
end_freq = 110e6
step_freq = 100e3
for freq in np.arange(start_freq, end_freq, step_freq):
    sdr.center_freq = freq
    samples = sdr.read_samples(256*1024)    
sdr.close()
