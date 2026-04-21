"""
--------------------------------------------------------------------------
Blink Program
--------------------------------------------------------------------------
License:  MIT 
Copyright 2026 - <Nicholas Melendez>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Blink Button Program that will
    -Blink the USR3 LED at 5hz (5 on/off cycles per second)
    -The program will utilize the Adafruit BBIO library
    
Abort Conditions:
    -Press Ctrl C to exit program
"""

# Imports to allow access to BBIO libraries
# Import time in order to allow for blinking 
# frequency manipulation
import Adafruit_BBIO.GPIO as GPIO
import time

#----------------------------
#   Main Script
#----------------------------


# The python variable "__name__" is provided by the language and can 
# - be used to determine how the file is being executed.  For example,
# - if the program is being executed on the command line:
# -   python3 simple_calc.py
# - then the "__name__" will be the string:  "__main__".  If the file 
# - is being imported into another python file:
# -   import simple_calc
# - the the "__name__" will be the module name, i.e. the string "simple_calc"
if __name__ == "__main__":

# Need to set up USR3 LED using as GPIO out
    GPIO.setup("USR3", GPIO.OUT)

# Loop while program is still active
    while True:
        
# Output High to start cycle and turn USR3 LED on
        GPIO.output("USR3", GPIO.HIGH)
        
# Delay by .1 seconds
        time.sleep(.1)
# Ouput Low to end cycle and turn USR3 LED off
        GPIO.output("USR3", GPIO.LOW)
# Delay by .1 seconds to achieve frequency of 5hz
        time.sleep(.1)