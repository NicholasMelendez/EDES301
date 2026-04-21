"""
--------------------------------------------------------------------------
Audio_Analyze Driver
--------------------------------------------------------------------------
License:   MIT
Copyright 2026 <Nicholas Melendez>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
""" 
import numpy as np

# --- Constants ---
SAMPLE_RATE    = 44100  # Standard CD Quality
FFT_SIZE       = 4096   # N (Number of samples per window)
NOISE_FLOOR    = 5000    # Minimum magnitude to register as "sound"

class AudioAnalyzer:
    """ Audio Analysis Class using FFT """

    def __init__(self, sample_rate=SAMPLE_RATE, fft_size=FFT_SIZE):
        """ Initialize variables for FFT analysis """
        
        self.fs = sample_rate
        self.n = fft_size
        
        # Pre-calculate the frequency values for each bin
        self.freq_bins = np.fft.rfftfreq(self.n, d=1/self.fs)

    def get_dominant_frequency(self, raw_data):
        """ 
        Perform FFT and return the peak frequency in Hz 
        Returns: float (Frequency in Hz) or None if below noise floor
        """
        # Convert byte data to 16-bit integers
        samples = np.frombuffer(raw_data, dtype=np.int16)

        # Apply Hanning Window to reduce spectral leakage into other bins
        windowed_samples = samples * np.hanning(len(samples))

        # Compute Real FFT
        fft_result = np.fft.rfft(windowed_samples)
        magnitudes = np.abs(fft_result)

        # Find the bin with the highest magnitude
        peak_index = np.argmax(magnitudes)
        peak_mag = magnitudes[peak_index]

        if peak_mag > NOISE_FLOOR:
            
            # Return the center frequency of that bin
            return self.freq_bins[peak_index]
        
        return None

# End Class