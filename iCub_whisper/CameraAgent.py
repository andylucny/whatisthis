import cv2 as cv
from agentspace import Agent, space

class CameraAgent(Agent):

    def __init__(self, id, nameImage):
        self.id = id
        self.nameImage = nameImage
        super().__init__()
        
    def init(self):
        camera = cv.VideoCapture(self.id)
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

