import numpy as np
from agentspace import Agent, space
import time 

def validName(name):
    letter_count = 0
    for char in name:
        if char.isalpha() or char.isdigit():
            letter_count += 1
    return letter_count > 0

class NamingAgent(Agent):

    def __init__(self, nameName, nameConfidence, nameQuery, nameIt, nameText, nameKey, minConfidence=6.0):
        self.nameName = nameName
        self.nameConfidence = nameConfidence
        self.nameQuery = nameQuery
        self.nameIt = nameIt
        self.nameText = nameText
        self.nameKey = nameKey
        self.minConfidence = minConfidence
        super().__init__()

    def init(self):
        self.lastName = ""
        self.lastTimestamp = 0
        self.noObject = 0
        self.confirm = 0
        self.confirmName = ""
        space.attach_trigger(self.nameConfidence,self)
        space.attach_trigger(self.nameIt,self)
        
    def senseSelectAct(self):
        confidence = space(default=0.0)[self.nameConfidence]
        name = space(default="")[self.nameName]
        if name == '':
            return
        query = space[self.nameQuery]
        timestamp = time.time()
        order = space(default=False)[self.nameIt]
        will = False

        if confidence > self.minConfidence:
            if self.lastName != name or timestamp - self.lastTimestamp > 60+np.random.uniform(-20,20):
                will = True
                
        else:
            self.noObject += 1
            if self.noObject > 5:
                self.noObject = 0
                self.lastName = ""

        if will:
            if self.confirm == 0:
                self.confirmName = name
                self.confirm = 1
            elif self.confirmName != name:
                self.confirm = 0
            else:
                self.confirm += 1
        else:
            self.confirm = 0
        
        if (will and self.confirm >= 3) or order:
            self.lastName = name
            self.lastTimestamp = timestamp
            if validName(name):
                if confidence <= self.minConfidence:
                    response = "To je možno "+name+", ale nie som si istý."
                else:
                    print('confidence',confidence)
                    response = "Toto je "+name+"."
                space(validity=1.0)[self.nameText] = response
                space[self.nameKey] = query
                time.sleep(3)
