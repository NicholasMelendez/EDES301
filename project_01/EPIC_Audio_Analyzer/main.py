"""
--------------------------------------------------------------------------
Main Driver
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

import time
import Adafruit_BBIO.GPIO as GPIO
import Microphone as Microphone
import Audio_Analyze as Audio_Analyzer
import Character_Display as Character_Display
import button as Button

# --- Constants ---
BUTTON_PIN = "P2_25"      # Update pin as needed
STATE_IDLE        = 0     # Idle state
STATE_ACTIVE      = 1     # Active state
QUIT_HOLD_TIME    = 3.0   # Seconds to hold button to exit
NOISE_TIMEOUT     = 10    # Seconds of silence before stopping mic
LCD_UPDATE_RATE   = .9    # Update screen only every 900ms
class EPIC_Audio_Analyzer:
    def __init__(self):
        # Initialize Hardware Drivers
        self.mic = Microphone.Microphone()
        self.analyzer = Audio_Analyzer.AudioAnalyzer()
        self.display = Character_Display.Character_Display()
        self.button = Button.Button(BUTTON_PIN)
        self.state = STATE_IDLE
        self.running = True
        self.last_sound_time = time.time()
        self.last_lcd_update = time.time()
        self.button_press_start = None
        
        self.display.show_message("EPIC AA Online!\nPress Button!:)")

    def toggle_state(self):
        """ Switches between Idle and Active modes """
        if self.state == STATE_IDLE:
            self.display.show_message("Initializing...\nMic: ON")
            self.mic.start_stream()
            self.state = STATE_ACTIVE
        else:
            self.mic.stop_stream()
            self.display.show_message("EPIC AA Online!\nPress Button!")
            self.state = STATE_IDLE
        

        time.sleep(0.3)

    def run(self):

        time.sleep(0.2)
        print("System Ready. Press button to start.")

        try:
            while self.running:
                now = time.time()

                is_pressed = (GPIO.input(BUTTON_PIN) == GPIO.LOW)
                
                
                if is_pressed:
                    if self.button_press_start is None:
                        self.button_press_start = now
                    

                    if (now - self.button_press_start) >= QUIT_HOLD_TIME:
                        self.display.show_message("Shutting Down...\nGoodbye!")
                        time.sleep(1.5)
                        self.cleanup()
                        sys.exit() 
                else:
                    if self.button_press_start is not None:
                        duration = now - self.button_press_start

                        if 0.05 < duration < QUIT_HOLD_TIME:
                            self.toggle_state()
                        self.button_press_start = None

           
                if self.state == STATE_ACTIVE:
                    raw_audio = self.mic.get_data()
                  
                    peak_hz = self.analyzer.get_dominant_frequency(raw_audio)


                    if peak_hz is not None:
                        if (now - self.last_lcd_update) > LCD_UPDATE_RATE:
                            self.display.display_freq(peak_hz)
                            self.last_lcd_update = now
                            
                           
                            if peak_hz > 0:
                                self.last_sound_time = now
    
    
                        
                      
                        silence_duration = now - self.last_sound_time
                        if silence_duration >= NOISE_TIMEOUT:
                            self.display.show_message("Sleep time :p\n Goodbye!")
                            time.sleep(3)
                            self.cleanup()
                    else:
                        self.last_sound_time = now
                
                time.sleep(0.02)
        except Exception as e:
            print(f"Error: {e}")
            self.cleanup()
        except KeyboardInterrupt:
            self.cleanup()
    def cleanup(self):
        """ Safe shutdown of all hardware """
        self.running = False
        self.display.show_message("Done!")
        self.mic.cleanup()
        GPIO.cleanup()
        print("System Offline.")

if __name__ == "__main__":
    epic_audio_analyzer = EPIC_Audio_Analyzer()
    epic_audio_analyzer.run()