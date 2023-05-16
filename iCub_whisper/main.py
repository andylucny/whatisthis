import os
os.environ['PATH'] += "iCumSim\\bin;"

from agentspace import Agent, space
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
ControlAgent('text','features','name') # asociating and other voice command
ViewerAgent('camera','name') # view image from camera
