import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
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

    def __init__(self, nameText, nameFeatures, nameName, nameAudio, loadKeysAndValues=False):
        self.nameText = nameText
        self.nameFeatures = nameFeatures
        self.nameName = nameName
        self.nameAudio = nameAudio
        self.loadKeysAndValues = loadKeysAndValues
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
        self.keys = []
        self.values = []
        self.names = []
        if self.loadKeysAndValues:
            self.keys = list(np.loadtxt("keys.npy"))
            self.values = list(np.loadtxt("values.npy"))
            self.names = []
            with open("names.txt", "rt") as f:
                self.names = f.read().rstrip('\n').split('\n')
            if len(self.keys) != len(self.values) or len(self.values) != len(self.names):
                self.keys = []
                self.values = []
                self.names = []
            else:
                print(len(self.keys),'keys, values and names loaded')
        self.emotion = iCubEmotion()
        self.fi = 0
        checkpoint = "./model/"  # LaMini-Flan-T5-248M
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,device_map='auto',torch_dtype=torch.float32)
        self.pipe = pipeline('text2text-generation',model = base_model,tokenizer = tokenizer,max_length = 512,do_sample=True,temperature=0.3,top_p=0.95)
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
            elif self.match(r'.*(this|it) is (a|the|) (.+)',text) and not "launch" in text:
                named = self.matched()[2]
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
                    psi = np.arctan2(act[1],act[0])
                    ind = int(np.round(psi/0.2))
                    if ind >= 0 and ind < len(self.names):
                        error = abs(psi - np.round(psi/0.2))
                        sz = np.linalg.norm(psi)
                        error0 = np.linalg.norm(act-self.values[ind])
                        name = self.names[ind]
                        print('name',name,'ind',ind,'error',error0,error,'sz',sz)
                        space(validity=2.0)[self.nameName] = name
                        noaudio = torch.from_numpy(np.array([]))
                        space(priority=2.0)[self.nameAudio] = noaudio # do not listen to itself
                        speak('This is a '+name)
                        time.sleep(0.5)
                        space(priority=2.0)[self.nameAudio] = None # listen again
                    else:
                        speak('I have no idea')
                else:
                    speak('I have no idea')
            elif self.match(r'(E|e)xplain.*',text):
                print(text)
                print("")
                generated_text = self.pipe(text)
                response = ''
                for sentence in generated_text:
                    response += sentence['generated_text']
                print(response)
                speak(response)

