import cv2 as cv
from agentspace import Agent, space

import subprocess

def setCameraControls(id,controls):
    command = [ "v4l2-ctl", "-d", f"/dev/video{id}" ]
    for control in controls.keys():
        value = controls[control]
        command += [ "-c", f"{control}={value}" ]
        _ = subprocess.check_output(command)

class CameraAgent(Agent):

    def __init__(self, id, nameImage):
        self.id = id
        self.nameImage = nameImage
        super().__init__()
        
    def init(self):
        setCameraControls(self.id,{'zoom_absolute':350,'tilt_absolute':0,'pan_absolute':0})
        camera = cv.VideoCapture(self.id,cv.CAP_DSHOW)
        fps = 30 
        camera.set(cv.CAP_PROP_FPS,fps)
        while True:
            # Grab a frame
            ret, img = camera.read()
            if not ret:
                self.stop()
                return
            
            # sample it onto blackboard
            space(validity=0.1)[self.nameImage] = img
 
    def senseSelectAct(self):
        pass

