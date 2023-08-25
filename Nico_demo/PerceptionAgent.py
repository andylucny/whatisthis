from agentspace import Agent, space
import numpy as np
import onnxruntime as ort
import cv2 as cv
import time

class PerceptionAgent(Agent):

    def __init__(self, nameImage, nameFeatures, namePoints):
        self.nameImage = nameImage
        self.nameFeatures = nameFeatures
        self.namePoints = namePoints
        super().__init__()

    def init(self):
        self.session = ort.InferenceSession("dino_deits8-224-final.onnx", providers=['CUDAExecutionProvider'])
        self.input_names = [input.name for input in self.session.get_inputs()] 
        self.output_names = [output.name for output in self.session.get_outputs()] 
        self.KFs = [ cv.KalmanFilter(4, 2, 0) for _ in range(6) ] 
        for KF in self.KFs:
            KF.transitionMatrix = cv.setIdentity(KF.transitionMatrix)
            KF.measurementMatrix = cv.setIdentity(KF.measurementMatrix)
        self.ticks = cv.getTickCount()
        self.hz = 0
        self.t = int(time.time())
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
        data_output = self.session.run(self.output_names, data_input)
        features = data_output[0][0]
        attentions = data_output[1][0]

        nh = attentions.shape[0]
        attentions = attentions[:, 0, 1:].reshape(nh, -1)
        patch_size = 8
        w_featmap, h_featmap = image_size[0] // patch_size, image_size[1] // patch_size
        attentions = attentions.reshape(nh, w_featmap, h_featmap)

        points = []
        for attention in attentions:
            attention /= np.max(attention)
            attention = np.asarray(attention*255,np.uint8)
            _, binary = cv.threshold(attention,0,255,cv.THRESH_BINARY|cv.THRESH_OTSU)
            
            disp = cv.hconcat([attention,binary])
            disp = cv.resize(disp,(patch_size*disp.shape[1],patch_size*disp.shape[0]),interpolation=cv.INTER_NEAREST)
            cv.imshow('attention',disp)
            cv.waitKey(1)
            
            indices = np.where(binary > 0)
            if len(indices[1]) > 0 and len(indices[0]) > 0:
                point = (np.average(indices[1])/w_featmap,np.average(indices[0])/h_featmap)
            else:
                point = (-1.0,-1.0)
            points.append(point)
            
        ticks = cv.getTickCount()
        dt = (ticks - self.ticks) / cv.getTickFrequency()
        self.ticks = ticks
        for i, KF in enumerate(self.KFs):
            KF.transitionMatrix[0,2] = dt
            KF.transitionMatrix[1,3] = dt
            prediction = KF.predict()
            if points[i][0] >= 0.0 and points[i][1] >= 0.0:
                correction = KF.correct(np.array(points[i],np.float32))
                points[i] = (correction[0][0],correction[1][0])
            else:
                points[i] = (prediction[0][0],prediction[1][0])
        
        self.hz += 1
        t = int(time.time())
        if t != self.t:
            fps = self.hz
            self.hz = 0
            self.t = t
            space(validity=2.5)['fps'] = fps
        
        space(validity=0.5)[self.nameFeatures] = features
        space(validity=0.5)[self.namePoints] = points
