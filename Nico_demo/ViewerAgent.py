from agentspace import Agent, space
import cv2 as cv
import time

class ViewerAgent(Agent):

    def __init__(self, nameImage, namePoints, nameName):
        self.nameImage = nameImage
        self.namePoints = namePoints
        self.nameName = nameName
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameImage,self)
            
    def senseSelectAct(self):
        image = space[self.nameImage]
        if image is None:
            return
        #image = cv.resize(image,(image.shape[1]//2,image.shape[0]//2))
        name = space(default='')[self.nameName]
        if len(name) > 0:
            cv.putText(image,name,(image.shape[1]//3,image.shape[0]//2),0,2.0,(0,255,0),3)
            confidence = space(default=0)['confidence']
            cv.putText(image,str(confidence),(image.shape[1]//3,image.shape[0]//2+25),0,0.8,(0,255,0),1)
        
        points = space(default=[])[self.namePoints]
        for i, point in enumerate(points):
            if point[0] >= 0.0 and point[1] >= 0.0:
                pt = (int(point[0]*image.shape[1]),int(point[1]*image.shape[0]))
                cv.circle(image,pt,3,(0,0,255),cv.FILLED)
                cv.putText(image,str(i),(pt[0],pt[1]-5),0,1.0,(0,0,255),1)

        fps = space(default=0)['fps']
        cv.putText(image,str(fps),(image.shape[1]-80,30),0,1.0,(0,255,0),1)
       
        cv.imshow("camera",image)
        key = cv.waitKey(1)
        if key == ord('s'):
            cv.imwrite(str(time.time())+'.png',image)
