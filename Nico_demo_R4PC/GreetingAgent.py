import numpy as np
from agentspace import Agent, space
import time 

class GreetingAgent(Agent):

    def __init__(self, nameFacePoint, namePoint, nameText, language='sk'):
        self.nameFacePoint = nameFacePoint
        self.namePoint = namePoint
        self.nameText = nameText
        self.language = language
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameFacePoint,self)
        
    def senseSelectAct(self):
        point = space[self.nameFacePoint]
        if point is None:
            return
        
        if np.random.uniform(0.0,1.0) <= 0.8:
            return
            
        t0 = time.time()
        while True:
            space(validity=0.5,priority=2.0)[self.namePoint] = point
            time.sleep(0.25)
            
            distance = np.linalg.norm(np.array(point)-np.array([0.5,0.5]))
            print(f'distance: {distance:1.2f} point: ({point[0]:1.2f},{point[1]:1.2f})')
            if distance < 0.1:
                greeting = "Dobrý deň!" if self.language == 'sk' else "Nice to meet you"
                space(validity=1.0,priority=2.0)[self.nameText] = greeting
                space(validity=0.6,priority=2.0)[self.namePoint] = (0.5,0.75)
                time.sleep(0.5)
                space(validity=1.1,priority=2.0)[self.namePoint] = (0.5,0.5)
                time.sleep(1.0)
                space(validity=0.6,priority=2.0)[self.namePoint] = (0.5,0.25)
                time.sleep(60+np.random.uniform(-10,50))
                return
                
            point = space[self.nameFacePoint]
            if point is None:
                return
                
            t1 = time.time()
            if t1-t0 > 7.0:
                time.sleep(np.random.uniform(0,300)+300)
                return
