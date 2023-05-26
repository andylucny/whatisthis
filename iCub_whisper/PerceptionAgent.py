from agentspace import Agent, space
import numpy as np
import onnxruntime as ort
import cv2 as cv

class PerceptionAgent(Agent):

    def __init__(self, nameImage, nameFeatures):
        self.nameImage = nameImage
        self.nameFeatures = nameFeatures
        super().__init__()

    def init(self):
        self.session = ort.InferenceSession("dino_deits8.onnx", providers=['CUDAExecutionProvider'])
        self.input_names = [input.name for input in self.session.get_inputs()] # ['x.1']
        self.output_names = [output.name for output in self.session.get_outputs()] # ['1158']
        space.attach_trigger(self.nameImage,self)
 
    def senseSelectAct(self):
        frame = space[self.nameImage]
        if frame is None:
            return

        image_size = (224, 224)
        blob = cv.dnn.blobFromImage(frame, 1.0/255, image_size, (0, 0, 0), swapRB=True, crop=True)
        blob[0][0] = (blob[0][0] - 0.485)/0.229
        blob[0][1] = (blob[0][1] - 0.456)/0.224
        blob[0][2] = (blob[0][2] - 0.406)/0.225
        
        data_input = { self.input_names[0] : blob }
        data_output = self.session.run(self.output_names, data_input)[0]
        features = data_output[0]
        #print(features[0])
        
        space(validity=0.5)[self.nameFeatures] = features
