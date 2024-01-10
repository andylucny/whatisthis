import numpy as np
from agentspace import Agent, space
import time 
from vocabulary import Vocabulary

class ControlAgent(Agent):

    def __init__(self, nameFeatures, nameName, nameConfidence, nameQuery):
        self.nameFeatures = nameFeatures
        self.nameName = nameName
        self.nameConfidence = nameConfidence
        self.nameQuery = nameQuery
        super().__init__()

    def init(self):
        space.attach_trigger(self.nameFeatures,self)
        
    def senseSelectAct(self):
        query = space[self.nameFeatures]
        if query is None:
            # I do not see
            time.sleep(1)
            return

        name, confidence = Vocabulary.Query(query)
        if name is not None:
            space(validity=2.0)[self.nameName] = name
            space(validity=2.0)[self.nameConfidence] = confidence
            space(validity=2.0)[self.nameQuery] = query
