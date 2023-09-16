import os

from download import download_all
download_all()

from agentspace import Agent, space, Trigger

from GuiAgent import GuiAgent
from CameraAgent import CameraAgent
from PerceptionAgent import PerceptionAgent
from ActionAgent import ActionAgent
from ViewerAgent import ViewerAgent
from ControlAgent import ControlAgent
from SpeakerAgent import SpeakerAgent
from NamingAgent import NamingAgent
from FaceAgent import FaceAgent
from GreetingAgent import GreetingAgent

from nicomotion.Motion import Motion
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

import signal
import time

def quit():
    try:
        del robot
    except:
        pass
    os._exit(0)
    
# exit on ctrl-c
def signal_handler(signal, frame):
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

minConfidence = 6.2

GuiAgent('features','name it','key')
time.sleep(1)
CameraAgent(0,'camera',350) # get image from the right eye
time.sleep(1)
CameraAgent(2,'wide camera',170) # get image from the left eye
PerceptionAgent('camera','features','points','point') # dino model
time.sleep(1)
ActionAgent(robot,'point') # turn to shown objects
time.sleep(1)
ControlAgent('features','name','confidence','query') # asociating 
time.sleep(1)
ViewerAgent('camera','points','face point','name',minConfidence) # view image from camera
time.sleep(1)
SpeakerAgent('text') # speach synthesis
time.sleep(1)
NamingAgent('name','confidence','query','name it','text','key',minConfidence) # when to speak
time.sleep(1)
FaceAgent('wide camera','face position','face','emotion','face point') # face detector
time.sleep(1)
GreetingAgent('face point','point','text')