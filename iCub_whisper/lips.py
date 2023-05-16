from agentspace import Agent, space
from pyicubsim import iCubApplicationName, iCubEmotion 
import time
import random

class LipsAgent(Agent):

    def __init__(self,name):
        self.name = name
        super().__init__()
        
    def init(self):
        self.emotion = iCubEmotion()
        self.openmouth = False
        self.attach_timer(0.25)
 
    def senseSelectAct(self):
        speaking = space(default=False)[self.name]
        if speaking:
            #print("speaking")
            if random.random() < 0.7:
                self.emotion.set('neu')
            else:
                self.emotion.set('sur')
                self.openmouth = True
        else:
            if self.openmouth:
                self.emotion.set('neu')
                self.openmouth = False

if __name__ == "__main__":
    iCubApplicationName('/lipsMover')
    LipsAgent('speaking')
    time.sleep(1.5)
    space['speaking'] = True
    time.sleep(3)
    space['speaking'] = False

