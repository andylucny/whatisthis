import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
from agentspace import Agent, space
from pyicubsim import iCubEmotion
from speak import speak
import time 
import re

def NearestNeighbor(query,keys,values):
    distances = np.linalg.norm(np.array(keys)-np.array(query),axis=1)
    index = np.argmin(distances)
    return values[index], 1.0/(distances[index]+0.0001)

class ControlAgent(Agent):

    def __init__(self, nameText, nameFeatures, nameName, nameAudio, loadKeysAndValues=False, minConfidence=0.0):
        self.nameText = nameText
        self.nameFeatures = nameFeatures
        self.nameName = nameName
        self.nameAudio = nameAudio
        self.loadKeysAndValues = loadKeysAndValues
        self.minConfidence = minConfidence
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
            self.values = np.arange(len(self.keys)) #list(np.loadtxt("values.npy"))
            self.names = []
            with open("names.txt", "rt") as f:
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
        self.emotion = iCubEmotion()
        checkpoint = "./LaMini/"  # LaMini-Flan-T5-248M
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
                self.keys.append(query)
                self.values.append(len(self.names))
                self.names.append(named)
                np.savetxt("keys.npy",np.array(self.keys))
                #np.savetxt("values.npy",np.array(self.values))
                with open("names.txt","w") as f:
                    for name in self.names:
                        f.write(name+'\n')
                speak('O.K.')
            elif self.match(r'.*what is this.*',text):
                if len(self.keys) > 0:
                    ind, confidence = NearestNeighbor(query,self.keys,self.values)
                    if ind >= 0 and ind < len(self.names): #confidence >= self.minConfidence and 
                        name = self.names[ind]
                        print('name',name,'ind',ind,'confidence',confidence)
                        space(validity=2.0)[self.nameName] = name
                        noaudio = torch.from_numpy(np.array([]))
                        space(priority=2.0)[self.nameAudio] = noaudio # do not listen to itself
                        speak('This is a '+name)
                        time.sleep(0.5)
                        space(priority=2.0)[self.nameAudio] = None # listen again
                    else:
                        print('confidence',confidence) 
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

