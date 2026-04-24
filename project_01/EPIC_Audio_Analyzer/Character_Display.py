"""
--------------------------------------------------------------------------
Character_Display Driver
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
import Adafruit_CharLCD as LCD
import Adafruit_BBIO.GPIO as GPIO

# --- Constants ---
LCD_RS        = "P2_4"
LCD_EN        = "P2_6"
LCD_D4        = "P2_8"
LCD_D5        = "P2_10"
LCD_D6        = "P2_17"
LCD_D7        = "P2_18"
LCD_COLUMNS   = 16
LCD_ROWS      = 2

class Character_Display:
    """ Interface for the 16x2 Character LCD """

    def __init__(self):
        """ Initialize the LCD hardware """
        
        self.lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7,
                                        LCD_COLUMNS, LCD_ROWS)
        self.lcd.clear()
        self.show_message("System Ready\nIdle Mode")

    def show_message(self, text):
        """ Display a string on the LCD """
        
        self.lcd.clear()
        self.lcd.message(text)

    def display_freq(self, freq):
        self.lcd.clear()
        if freq == 0:
            self.lcd.message("Freq: 0 Hz\nStatus: Silent")
        elif freq < 1000:
            # Standard Hz display
            self.lcd.message("Freq: {:.1f} Hz\nRange: Low".format(freq))
        else:
            # kHz display for higher ranges (e.g., 15.4 kHz)
            self.lcd.message("Freq: {:.2f} kHz\nRange: High".format(freq / 1000.0))

    def clear(self):
        """ Clear the display """
        self.lcd.clear()

# End Class