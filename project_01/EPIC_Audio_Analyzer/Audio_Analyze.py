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
NOTE_NAMES     = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
class AudioAnalyzer:
    def __init__(self, sample_rate=SAMPLE_RATE, chunk_size=FFT_SIZE):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
       
        self.window = np.hanning(chunk_size)
       


    def get_dominant_frequency(self, data):
        if data is None: return 0.0
        
        audio_data = np.frombuffer(data, dtype=np.int16).astype(float)
        
        
        if (np.max(audio_data) - np.min(audio_data)) / 32768.0 < 0.005: 
            return 0.0
            
        audio_data = (audio_data / 32768.0) - np.mean(audio_data)
        magnitude = np.abs(np.fft.rfft(audio_data * self.window))
        frequencies = np.fft.rfftfreq(len(audio_data), 1.0 / self.sample_rate)
        
        magnitude[frequencies < 50] = 0 
        max_mag = np.max(magnitude)
        
        if max_mag < 0.05: 
            return 0.0

       
        threshold = max_mag * 0.4 
        possible_peaks = np.where(magnitude > threshold)[0]
        
        if len(possible_peaks) > 0:
            return frequencies[possible_peaks[0]]
            
        return 0.0
        

    def get_closest_pitch(self, freq):
        if freq <= 50: 
            return "None", 0, 0
            
        n = 12 * np.log2(freq / 440.0)
        n_rounded = int(round(n))
        cents_error = int((n - n_rounded) * 100)
        
        midi_number = n_rounded + 69
        note_name = NOTE_NAMES[midi_number % 12]
        octave = (midi_number // 12) - 1
        
        return note_name, octave, cents_error
         

# End Class