import os

from download import download_all
download_all()

from agentspace import Agent, space, Trigger

from CameraAgent import CameraAgent
from PerceptionAgent import PerceptionAgent
from ActionAgent import ActionAgent
from ViewerAgent import ViewerAgent
from ControlAgent import ControlAgent
from SpeakerAgent import SpeakerAgent

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

CameraAgent(0,'camera') # get image from the right eye
time.sleep(1)
PerceptionAgent('camera','features','points') # dino model
time.sleep(1)
ActionAgent(robot,'points') # turn to shown objects
time.sleep(1)
ControlAgent('text','features','name',loadKeysAndValues=True) # asociating 
time.sleep(1)
ViewerAgent('camera','points','name') # view image from camera
time.sleep(1)
SpeakerAgent('name') # speach synthesis

def enter(text=''):
    space['text'] = text

# enter('hruska')
