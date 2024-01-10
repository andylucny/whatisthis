import numpy as np
from agentspace import Agent, space
import cv2 as cv
import time
#from sk import putText

class ViewerAgent(Agent):

    def __init__(self, nameImage, namePoints, nameFacePoint, nameName, minConfidence=6.0):
        self.nameImage = nameImage
        self.namePoints = namePoints
        self.nameFacePoint = nameFacePoint
        self.nameName = nameName
        self.minConfidence = minConfidence
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
            confidence = space(default=0)['confidence']
            color = (0,255,0) if confidence > self.minConfidence else (180,180,180)
            cv.putText(image,name,(image.shape[1]//3,image.shape[0]//2),0,2.0,color,3) # remove cv. for sk
            cv.putText(image,str(confidence),(image.shape[1]//3,image.shape[0]//2+25),0,0.8,color,1)
        
        points = space(default=[])[self.namePoints]
        for i, point in enumerate(points):
            if point[0] >= 0.0 and point[1] >= 0.0:
                pt = (int(point[0]*image.shape[1]),int(point[1]*image.shape[0]))
                if i == 2: # the best attention map index is 2
                    cv.circle(image,pt,3,(0,0,255),cv.FILLED)
                    #cv.putText(image,str(i),(pt[0],pt[1]-5),0,1.0,(0,0,255),1)

        face = space[self.nameFacePoint]
        if face is not None:
            pt = (int(face[0]*image.shape[1]),int(face[1]*image.shape[0]))
            cv.circle(image,pt,10,(255,0,255),cv.FILLED)
            #distance = np.linalg.norm((np.array(face)-np.array([0.5,0.5]))*np.array([1.0,0.1]))
            #cv.putText(image,f"{distance:1.1f}",(pt[0],pt[1]-10),0,1.0,(0,0,255),1)
        
        fps = space(default=0)['fps']
        cv.putText(image,str(fps),(image.shape[1]-80,30),0,1.0,(0,255,0),1)
       
        cv.imshow("camera",image)
        key = cv.waitKey(1)
        if key == ord('s'):
            cv.imwrite(str(time.time())+'.png',image)
