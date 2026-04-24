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
NOISE_FLOOR    = 1000   # Minimum magnitude to register as "sound"

class AudioAnalyzer:
    def __init__(self, sample_rate=SAMPLE_RATE, chunk_size=FFT_SIZE):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
       
        self.window = np.hanning(chunk_size)
       
        self.threshold = 0.5

    def get_dominant_frequency(self, data):
       
        audio_data = np.frombuffer(data, dtype=np.int16).astype(float)
        audio_data = audio_data - np.mean(audio_data) 
        
       
        if len(audio_data) != len(self.window):
            current_window = np.hanning(len(audio_data))
        else:
            current_window = self.window
        audio_data = audio_data * current_window
        
       
        magnitude = np.abs(np.fft.rfft(audio_data))
        frequencies = np.fft.rfftfreq(len(audio_data), 1.0 / self.sample_rate)
       
        magnitude[frequencies < 30] = 0 
        
        
        peak_index = np.argmax(magnitude)
        peak_mag = magnitude[peak_index]
        
    
        if peak_mag < 1.0: 
            return 0.0
            
        peak_freq = frequencies[peak_index]
     
        return peak_freq
# End Class