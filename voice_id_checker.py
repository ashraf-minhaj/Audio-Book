"""
pyttsx3 voice id check
author: ashraf minhaj
mail: ashraf_minhaj@yahoo.com
"""

import pyttsx3                             #import pyttsx3
engine = pyttsx3.init()                    #initialize pyttsx3 engine
voices = engine.getProperty('voices')      #check for voices

#0 male, 1 female
engine.setProperty('voice', voices[1].id)  #changing index changes voices
engine.say('Yo bro! Do you like my voice?')
engine.runAndWait()