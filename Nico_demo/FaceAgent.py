import numpy as np
import cv2 as cv 
from agentspace import Agent, space
import time

class FaceAgent(Agent):

    def __init__(self,nameImage,nameFacePosition,nameFaceImage,nameFaceEmotion,nameFacePoint):
        self.nameImage = nameImage
        self.nameFacePosition = nameFacePosition
        self.nameFaceImage = nameFaceImage
        self.nameFaceEmotion = nameFaceEmotion
        self.nameFacePoint = nameFacePoint
        super().__init__()

    def init(self): 
        print("faceDetector: loading model")
        face_architecture = 'face/deploy.prototxt'
        face_weights = 'face/res10_300x300_ssd_iter_140000.caffemodel'
        self.net = cv.dnn.readNetFromCaffe(face_architecture,face_weights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
        #self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        #self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        print("faceDetector: model loaded")

        #print("emotionDetector: loading model")
        #self.net2 = cv.dnn.readNet('face/mobilenet_7.pbtxt','face/mobilenet_7.pb')
        #print("emotionDetector: model loaded")
        #self.labels = None
        #labelsFile = "face/labels.txt"
        #with open(labelsFile, 'rt') as f:
        #    self.labels = f.read().rstrip('\n').split('\n')

        space.attach_trigger(self.nameImage, self)

    def senseSelectAct(self):
        image = space[self.nameImage]
        if image is None:
            return

        height = 300
        width = 300
        mean = (104.0, 177.0, 123.0)
        threshold = 0.5
        h, w = image.shape[:2] 

        # convert to RGB
        rgb = cv.cvtColor(image,cv.COLOR_BGR2RGB)

        # blob preparation
        blob = cv.dnn.blobFromImage(cv.resize(image,(width,height)),1.0,(width,height),mean)

        # passing blob through the network to detect and pridiction
        self.net.setInput(blob)
        detections = self.net.forward()

        # loop over the detections
        rects = []
        faces = []
        for i in range(detections.shape[2]):
            # extract the confidence and prediction
            confidence = detections[0, 0, i, 2]
            # filter detections by confidence greater than the minimum
            if confidence > threshold:
                # compute the (x, y)-coordinates of the bounding box for the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype(np.int32)
                if startX < 0:
                    startX = 0
                if startY < 0:
                    startY = 0
                if endX > w:
                    endX = w
                if endY > h:
                    endY = h
                if (startY+1 < endY) and (startX+1 < endX):
                    rects.append((startX, startY, endX, endY, confidence))
                    face = np.copy(image[startY:endY,startX:endX,:])
                    faces.append(face)
        
        result = np.copy(image)

        if len(rects) > 0:
            
            # select the best face
            best = np.argmin([rect[4] for rect in rects])

            startX, startY, endX, endY, confidence = rects[best]
            cv.rectangle(result, (startX, startY), (endX, endY), (0, 0, 255), 2)
            text = "{:.2f}%".format(confidence * 100)
            cv.putText(result, text, (startX, startY-5), 0, 1.0, (0, 0, 255), 2)
            
            ## transform the image to suitable input of the MobileNet DNN
            #blob = cv.dnn.blobFromImage(faces[best], 1.0, (224, 224), (123.68, 116.779, 103.939), True, False)
            ## put the input to the network
            #self.net2.setInput(blob)
            ## launch the network and get the produced output
            #scores = self.net2.forward()[0]
            ## process the output typical for softmax classifier
            #emotion = np.argmax(scores) # 0..6 see labels.txt

            # display the detected emotion
            #label = self.labels[emotion]
            #print(label)
            #cv.putText(result, label, (10,50), cv.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv.LINE_AA)

            # output the find info to the blackboard
            rect = ((startX+endX)/2/w,(startY+endY)/2/h,(endX-startX-1)/w,(endY-startY-1)/h)
            #space(validity=0.2)[self.nameFacePosition] = rect
            #space(validity=0.2)[self.nameFaceImage] = faces[best]
            #space(validity=0.2)[self.nameFaceEmotion] = emotion
            #space(validity=0.2)[self.nameFaceEmotion+"Label"] = label
            point = rect[:2]
            #print('face',point)
            space(validity=0.5)[self.nameFacePoint] = point

        cv.imshow("faces",result)
        cv.waitKey(1)
        
        time.sleep(0.2)
