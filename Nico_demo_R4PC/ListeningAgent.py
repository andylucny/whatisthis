from agentspace import Agent, space
import numpy as np
import time
import os
import re
from vocabulary import Vocabulary
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
import time

class ListeningAgent(Agent):

    def __init__(self, nameText, nameFeatures, nameIt, nameSpeak, device='cpu'): # cpu or cuda
        self.nameText = nameText
        self.nameFeatures = nameFeatures
        self.nameIt = nameIt
        self.nameSpeak = nameSpeak
        self.device = device
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
        Vocabulary.Load()

        checkpoint = "./LaMini/"  # LaMini-Flan-T5-248M
        if self.device == 'cuda':
            tokenizer = AutoTokenizer.from_pretrained(checkpoint)
            base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,device_map='auto',torch_dtype=torch.float32)
        else:
            tokenizer = AutoTokenizer.from_pretrained(checkpoint, device='cpu')
            base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,torch_dtype=torch.float32)
        self.pipe = pipeline('text2text-generation',model = base_model,tokenizer = tokenizer,max_length = 512,do_sample=True,temperature=0.3,top_p=0.95)

        space.attach_trigger(self.nameText,self)
        
    def senseSelectAct(self):  
        text = space(default="")[self.nameText]
        text = text.lower()
        if len(text) == 0:
            return
        print(text)
            
        if self.match(r'say (.*)',text):
            tobesaid = self.matched()[0]
            print(tobesaid,'should be said')
            space(validity=1.0)[self.nameSpeak] = tobesaid
        elif text == "smile":
            pass
        elif self.match(r'.*(this|it) is (a|the|) (.+)',text):
            named = self.matched()[2]
            if named == 'background' or named == 'pozadie':
                named = '_'
            print("mapping",named)
            key = space[self.nameFeatures]
            Vocabulary.Add(key,named)
            Vocabulary.Save()
            space(validity=1.0)[self.nameSpeak] = 'O.K.'
        elif self.match(r'.*what is this.*',text):
            space(validity=0.5)[self.nameIt] = True
        elif self.match(r'.*touch (the|) (L|l)(C|c).*',text):
            space(validity=0.5)['anim'] = "touchLCD"
        elif text != 'connect':
            #space(priority=100)['point'] = (-1,-1)
            #space(validity=1.0)[self.nameSpeak] = 'eee eee eee'
            print('request:',text)
            print("")
            t0 = time.time()
            generated_text = self.pipe("You are a robot with two hands and head, but without legs. Give a short answer if the following question is reasonable. Tell 'I have no idea' otherwise. "+text)
            t1 = time.time()
            print('LaMini: elapsed',t1-t0,'s')
            response = ''
            for sentence in generated_text:
                response += sentence['generated_text']
            response = response.replace("AI language model","artificial creature")
            response = response.replace("physical body","actual body")
            print('response:',response)
            space(validity=1.0)[self.nameSpeak] = response
            #space(priority=100)['point'] = None