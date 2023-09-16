import os
import sys
from agentspace import Agent, space
import pyttsx3
import time

def speak(text):
    space['speaking'] = True
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    filip = 3
    engine.setProperty('voice', voices[filip].id)
    engine.say(text)
    print('speaking on <'+text+'>')
    engine.runAndWait()
    print('speaking off')
    space['speaking'] = False

class SpeakerAgent(Agent):

    def __init__(self, nameText):
        self.nameText = nameText
        super().__init__()
        
    def init(self):
        space.attach_trigger(self.nameText,self)
        
    def senseSelectAct(self):
        text = space(default='')[self.nameText]
        speak(text)

if __name__ == "__main__":  
    text = sys.argv[1] if len(sys.argv) > 1 else "eee"
    speak(text)
    