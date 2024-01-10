from agentspace import Agent, space
import numpy as np
import time
import os
import re
from vocabulary import Vocabulary
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

class ListeningAgent(Agent):

    def __init__(self, nameText, nameFeatures, nameIt, nameSpeak):
        self.nameText = nameText
        self.nameFeatures = nameFeatures
        self.nameIt = nameIt
        self.nameSpeak = nameSpeak
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
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,device_map='auto',torch_dtype=torch.float32)
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
            print("mapping",named)
            key = space[self.nameFeatures]
            Vocabulary.Add(key,named)
            Vocabulary.Save()
            space(validity=1.0)[self.nameSpeak] = 'O.K.'
        elif self.match(r'.*what is this.*',text):
            space(validity=0.5)[self.nameIt] = True
        else:
            print('request:',text)
            print("")
            generated_text = self.pipe("Give a short answer if the following question is reasonable. Tell 'I have no idea' otherwise. "+text)
            response = ''
            for sentence in generated_text:
                response += sentence['generated_text']
            print('response:',response)
            space(validity=1.0)[self.nameSpeak] = response
