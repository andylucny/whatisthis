from agentspace import Agent, space
import numpy as np
import speech_recognition as sr
import torch

class ListenerAgent(Agent):

    def __init__(self, nameAudio):
        self.nameAudio = nameAudio
        super().__init__()
        
    def init(self):
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.pause_threshold = 0.1#0.8
        r.non_speaking_duration = 0.1
        r.dynamic_energy_threshold = False
        with sr.Microphone(sample_rate=16000) as source:
            while True:
                audio = r.listen(source)
                torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                space(validity=2.0)[self.nameAudio] = torch_audio
 
    def senseSelectAct(self):
        pass

