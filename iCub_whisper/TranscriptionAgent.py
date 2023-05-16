from agentspace import Agent, space
import whisper

class TranscriptionAgent(Agent):

    def __init__(self, nameAudio, nameText):
        self.nameAudio = nameAudio
        self.nameText = nameText
        super().__init__()
        
    def init(self):
        self.audio_model = whisper.load_model("base.en").to('cuda')
        space.attach_trigger(self.nameAudio,self)
 
    def senseSelectAct(self):
        audio_data = space[self.nameAudio]
        if audio_data is not None:
            result = self.audio_model.transcribe(audio_data,language='english')
            space(validity=1.0)[self.nameText] = result['text']
            #print(result['text'])

