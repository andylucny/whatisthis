import numpy as np
from agentspace import Agent, space
from pyicubsim import iCubEmotion
from speak import speak
import time 
import re

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def Attention(query,keys,values,d):
    keys_matrix = np.array(keys,np.float32)
    values_matrix = np.array(values,np.float32)
    c = softmax(query.dot(keys_matrix.T)/d)
    output = c.dot(values_matrix)
    return output

class ControlAgent(Agent):

    def __init__(self, nameText, nameFeatures, nameName):
        self.nameText = nameText
        self.nameFeatures = nameFeatures
        self.nameName = nameName
        super().__init__()

    def match(self,pattern,text):
        search = re.search(pattern,text)
        if search is None:
            self.groups = []
            return False
        else:
            self.groups = search.groups()
            return True
    
    def matched(self):
        return self.groups

    def init(self):
        self.keys = [] #list(np.loadtxt("keys.npy"))
        self.values = [] #list(np.loadtxt("values.npy"))
        self.names = [] #
        #with open("names.txt", "rt") as f:
        #    self.names = f.read().rstrip('\n').split('\n')
        self.emotion = iCubEmotion()
        self.fi = 0
        space.attach_trigger(self.nameText,self)
        
    def senseSelectAct(self):
        text = space(default='')[self.nameText]
        query = space[self.nameFeatures]
        if query is None:
            speak("I do not see")
            time.sleep(1)
            return

        text = text.lower()
        if len(text) > 0:
            print(text)
            if self.match(r'say (.*)',text):
                print(self.matched()[0],'should be said')
                speak(self.matched()[0])
            elif text == "smile":
                self.emotion.set('hap')
            elif self.match(r'.*this is (a|the) (.*)',text) and not "launch" in text:
                named = self.matched()[1]
                print("mapping",named)
                act = [np.cos(self.fi), np.sin(self.fi)]
                self.fi += 0.2
                self.keys.append(query)
                self.values.append(act)
                self.names.append(named)
                np.savetxt("keys.npy",np.array(self.keys))
                np.savetxt("values.npy",np.array(self.values))
                with open("names.txt","w") as f:
                    for name in self.names:
                        f.write(name+'\n')
                speak('O.K.')
            elif self.match(r'.*what is this.*',text):
                if len(self.keys) > 0:
                    act = Attention(query,self.keys,self.values,len(query)**0.5)
                    #print('act',act)
                    psi = np.arctan2(act[1],act[0])
                    #print('psi',psi)
                    ind = int(np.round(psi/0.2))
                    #print('ind',ind)
                    if ind >= 0 and ind < len(self.names):
                        name = self.names[ind]
                        print('name',name)
                        space(validity=2.0)[self.nameName] = name
                        space(validity=2.0, priority=2.0)[self.nameText] = '' # do not listen to itself
                        speak('A '+name)
                        #space(validity=2.0)[self.nameName] = name
                        #space(validity=2.0, priority=2.0)[self.nameText] = '' # do not listen to itself
                    else:
                        speak('I have no idea')
                else:
                    speak('I have no idea')
