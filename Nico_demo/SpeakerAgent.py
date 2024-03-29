import os
import sys
from agentspace import Agent, space
import pyttsx3
import time

def speak(text, language='sk'):
    space['speaking'] = True
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    speaker = 3 if language == 'sk' else 2 # 3 is slovak Filip, 0 is David, 1 Markus, 2 Hazel
    engine.setProperty('voice', voices[speaker].id)
    engine.say(text)
    print('speaking on <'+text+'>')
    engine.runAndWait()
    print('speaking off')
    space['speaking'] = False

class SpeakerAgent(Agent):

    def __init__(self, nameText, language='sk'):
        self.nameText = nameText
        self.language = language
        super().__init__()
        
    def init(self):
        space.attach_trigger(self.nameText,self)
        
    def senseSelectAct(self):
        text = space(default='')[self.nameText]
        speak(text,self.language)

if __name__ == "__main__":  
    text = sys.argv[1] if len(sys.argv) > 1 else "eee"
    language = sys.argv[2] if len(sys.argv) > 2 else "sk"
    speak(text,language)
    