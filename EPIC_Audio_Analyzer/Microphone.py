"""
--------------------------------------------------------------------------
Microphone Driver
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
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUE/;/l;NTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""
import pyaudio

# --- Constants ---
FORMAT         = pyaudio.paInt16 
CHANNELS       = 1
RATE           = 44100
CHUNK_SIZE     = 2048


class Microphone:
    """ USB Microphone Hardware Interface """

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.device_index = None
        
        # Find Microphone ID
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if "USB" in info.get('name').upper():
                self.device_index = i
                print(f"Found USB Mic at Index {i}: {info.get('name')}")
                break
        
        if self.device_index is None:
            print("CRITICAL ERROR: No USB Microphone detected!")

    def start_stream(self):
        if self.stream is None and self.device_index is not None:
            try:
                self.stream = self.p.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=self.device_index,
                    frames_per_buffer=CHUNK_SIZE
                )
            except Exception as e:
                print(f"Failed to open stream: {e}")
                
    def stop_stream(self):
        """ Close the port to save power/CPU """
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def get_data(self):
        """ Pull raw bytes from the buffer """
        if self.stream:
            try:
                return self.stream.read(CHUNK_SIZE, exception_on_overflow=False)
            except Exception as e:
                return None
        return None

    def cleanup(self):
        """ Full teardown of the audio system """
        self.stop_stream()
        self.p.terminate()

# End Class