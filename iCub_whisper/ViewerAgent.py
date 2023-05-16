from agentspace import Agent, space
import cv2 as cv
import time

class ViewerAgent(Agent):

    def __init__(self, nameImage, nameName):
        self.nameImage = nameImage
        self.nameName = nameName
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameImage,self)
            
    def senseSelectAct(self):
        image = space[self.nameImage]
        if image is None:
            return
        image = cv.resize(image,(image.shape[1]//2,image.shape[0]//2))
        name = space(default='')[self.nameName]
        cv.putText(image,name,(image.shape[1]//3,image.shape[0]//2),0,2.0,(0,0,255),3)

        cv.imshow("camera",image)
        key = cv.waitKey(1)
        if key == ord('s'):
            cv.imwrite(str(time.time())+'.png',image)
