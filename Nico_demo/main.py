import os

from download import download_all
download_all()

from agentspace import Agent, space, Trigger

from CameraAgent import CameraAgent
from PerceptionAgent import PerceptionAgent
#from ActionAgent import ActionAgent
from ViewerAgent import ViewerAgent
#from ControlAgent import ControlAgent

from nicomotion.Motion import Motion
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

import signal
import time

def quit():
    del robot
    os._exit(0)
    
# exit on ctrl-c
def signal_handler(signal, frame):
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

CameraAgent(0,'camera') # get image from the right eye
time.sleep(1)
PerceptionAgent('camera','features','points') # dino model
time.sleep(1)
#ActionAgent(robot,'points') # turn to shown objects
#time.sleep(1)
ViewerAgent('camera','points','name') # view image from camera
#time.sleep(1)
#ControlAgent('text','features','name','audio',loadKeysAndValues=False)#,minConfidence=9.0) # asociating and other voice command

"""
class MonitoringAgent(Agent):
    def init(self):
        self.t0 = time.time()
        space.attach_trigger('audio',self,Trigger.NAMES)
        space.attach_trigger('text',self,Trigger.NAMES)
    def senseSelectAct(self):
        print(time.time()-self.t0,self.triggered())
        if self.triggered() == 'text':
            print('<',space['text'],'>')

MonitoringAgent()
"""
