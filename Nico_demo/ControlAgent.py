import numpy as np
from agentspace import Agent, space
import time 

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def Attention(query,keys,values,d):
    keys_matrix = np.array(keys,np.float32)
    values_matrix = np.array(values,np.float32)
    cossim = query.dot(keys_matrix.T)
    c = softmax(cossim/d)
    output = c.dot(values_matrix)
    return output, np.max(cossim)/len(query)

class ControlAgent(Agent):

    def __init__(self, nameText, nameFeatures, nameName, loadKeysAndValues=False, minConfidence=0.0):
        self.nameText = nameText
        self.nameFeatures = nameFeatures
        self.nameName = nameName
        self.loadKeysAndValues = loadKeysAndValues
        self.minConfidence = minConfidence
        super().__init__()

    def init(self):
        self.keys = []
        self.values = []
        self.names = []
        if self.loadKeysAndValues:
            self.keys = list(np.loadtxt("keys.npy"))
            self.values = list(np.loadtxt("values.npy"))
            self.names = []
            with open("names.txt", "rt", encoding='utf8') as f:
                self.names = f.read().rstrip('\n').split('\n')
            if len(self.keys) != len(self.values) or len(self.values) != len(self.names):
                print('learning from scratch')
                self.keys = []
                self.values = []
                self.names = []
            else:
                print(len(self.keys),'keys, values and names loaded')
        else:
            print('learning from scratch')
        self.fi = 0
        space.attach_trigger(self.nameFeatures,self)
        
    def senseSelectAct(self):
        text = space(default='')[self.nameText]
        query = space[self.nameFeatures]
        if query is None:
            # I do not see
            time.sleep(1)
            return

        if len(text) > 0:
            text = text.lower()
            print(text)
            act = None
            for name, value in zip(self.names,self.values):
                if name == text:
                    act = value
                    break
            if act is None:
                act = [np.cos(self.fi), np.sin(self.fi)]
                self.fi += 0.2
            self.keys.append(query)
            self.values.append(act)
            self.names.append(text)
            np.savetxt("keys.npy",np.array(self.keys))
            np.savetxt("values.npy",np.array(self.values))
            with open("names.txt","w") as f:
                for name in self.names:
                    f.write(name+'\n')
            print('O.K.')
            space[self.nameText] = None
        else:
            if len(self.keys) > 0:
                act, confidence = Attention(query,self.keys,self.values,len(query)**0.5)
                psi = np.arctan2(act[1],act[0])
                ind = int(np.round(psi/0.2))
                if confidence >= self.minConfidence and ind >= 0 and ind < len(self.names):
                    error = abs(psi - np.round(psi/0.2))
                    sz = np.linalg.norm(psi)
                    error0 = np.linalg.norm(act-self.values[ind])
                    name = self.names[ind]
                    #print('name',name,'confidence',confidence) #'ind',ind,'error',error0,error,'sz',sz)
                    space(validity=2.0)[self.nameName] = name
                    space(validity=2.0)['confidence'] = confidence
                else:
                    #print('confidence',confidence)
                    # I have no idea
                    pass
