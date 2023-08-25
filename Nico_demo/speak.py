import os
import sys
from agentspace import Agent, space
import pyttsx3
import time

def speak(text):
    space['speaking'] = True
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    print('speaking on <'+text+'>')
    engine.runAndWait()
    print('speaking off')
    space['speaking'] = False

if __name__ == "__main__":  
    text = sys.argv[1] if len(sys.argv) > 1 else "eee"
    speak(text)
    