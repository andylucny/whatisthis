import os
os.environ['PATH'] += "iCumSim\\bin;"

from agentspace import Agent, space, Trigger
from ListenerAgent import ListenerAgent
from TranscriptionAgent import TranscriptionAgent
from CameraAgent import CameraAgent
from PerceptionAgent import PerceptionAgent
from lips import LipsAgent
from ControlAgent import ControlAgent
from ViewerAgent import ViewerAgent
from pyicubsim import iCubApplicationName

import signal
import time

def quit():
    os._exit(0)
    
# exit on ctrl-c
def signal_handler(signal, frame):
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

iCubApplicationName('/objectnaming')

ListenerAgent('audio') # listen to audio
time.sleep(1)
TranscriptionAgent('audio','text') # transcribe audio into text
time.sleep(1)
LipsAgent('speaking') # moving lips during speaking
CameraAgent(0,'camera') # get image from camera
time.sleep(1)
PerceptionAgent('camera','features') # dino encoder
time.sleep(1)
ControlAgent('text','features','name','audio') # asociating and other voice command
ViewerAgent('camera','name') # view image from camera

class MonitoringAgent(Agent):
    def init(self):
        self.t0 = time.time()
        space.attach_trigger('audio',self,Trigger.NAMES)
        space.attach_trigger('text',self,Trigger.NAMES)
    def senseSelectAct(self):
        print(time.time()-self.t0,self.triggered())
        if self.triggered() == 'text':
            print('<',space['text'],'>')

#MonitoringAgent()

