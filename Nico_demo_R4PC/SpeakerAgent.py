import os
import sys
from agentspace import Agent, space, Trigger
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
        space.attach_trigger(self.nameText,self,Trigger.NAMES_AND_VALUES)
        
    def senseSelectAct(self):
        #text = space(default='')[self.nameText]
        _, text = self.triggered()
        speak(text,self.language)
        ## repeat eee
        #if text == 'eee':
        #    time.sleep(0.3)
        #    if space(default='')[self.nameText] == '':
        #        space(validity=0.1)[self.nameText] = text

if __name__ == "__main__":  
    text = sys.argv[1] if len(sys.argv) > 1 else "ahoj"
    language = sys.argv[2] if len(sys.argv) > 2 else "sk"
    speak(text,language)
    time.sleep(1)
    agent = SpeakerAgent('text','en')
    time.sleep(1)
    space['text']='three times speaking'
    space['text']='three times speaking'
    space['text']='three times speaking'
    time.sleep(10)
    space(validity=0.1)['text']='eee'
    time.sleep(5)
    space['text']='the last time speaking'
    time.sleep(7)
    agent.stop()
