# EPIC_Audio_Analyzer

Welcome to the official repsotiroy for the EPIC_Audio_Analyzer!


If you have not already finished putting all of your components
onto your breadboard, please see my Hackster Page [Hackster.io](https://www.hackster.io/nm123/edes-301-epic-audio-analyzer-cc994b?auth_token=6399cccf68739bcc7e2da50530170805)



Before you download the software files, please make sure to run these lines of code in your terminal:

*sudo apt-get update

*sudo apt-get install libasound2-dev python3-pip

*pip3 install pyaudio numpy

*sudo /usr/bin/python3 -m pip install adafruit-blinka Adafruit_BBIO adafruit-charlcd pyaudio numpy


In order to run the EPIC_Audio_Analyzer, please download all the python files:

*Audio_Analyze.py

*button.py

*Character_Display.py

*Microphone.py

*main.py


and load them onto your EPIC_Audio_Analyzer directory/folder.

After making sure all the python folders are installed in the same directory/folder, change into the EPIC_Audio_Analyzer directory/folder.

Run: python3 main.py and Enjoy!

**One important note:**

In order to change the rate at which the LCD updates, please see the constant "LCD_UPDATE_RATE". The time input is in seconds.
