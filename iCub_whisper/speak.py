import os
import sys
from agentspace import Agent, space

def speak(text):
    os.environ["ESPEAK_DATA_PATH"] = "." 
    space['speaking'] = True
    os.system('espeak -z "'+text+'"')
    space['speaking'] = False

if __name__ == "__main__":  
    text = sys.argv[1] if len(sys.argv) > 1 else "eee"
    speak(text)
    