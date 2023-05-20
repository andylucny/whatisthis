from agentspace import Agent, space
import whisper

class TranscriptionAgent(Agent):

    def __init__(self, nameAudio, nameText):
        self.nameAudio = nameAudio
        self.nameText = nameText
        super().__init__()
        
    def init(self):
        self.audio_model = whisper.load_model("base.en").to('cuda')
        print('ready to transcript')
        space.attach_trigger(self.nameAudio,self)
 
    def senseSelectAct(self):
        audio_data = space[self.nameAudio]
        if audio_data is not None:
            if len(audio_data) > 0:
                print('transcripting...')
                result = self.audio_model.transcribe(audio_data,language='english')
                print('...transcripted')
                space(validity=1.0)[self.nameText] = result['text']
                #print(result['text'])

