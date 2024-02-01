from agentspace import Agent, space
import numpy as np
import cv2 as cv
import time

class ActionHeadAgent(Agent):

    def __init__(self, robot, namePoint):
        self.robot = robot
        self.namePoint = namePoint
        super().__init__()

    def init(self):
        self.robot.setAngle("head_z",0.0,0.05)
        self.robot.setAngle("head_y",-25.0,0.05)
        time.sleep(2.0)
        space.attach_trigger(self.namePoint,self)

    def senseSelectAct(self):
        point = space[self.namePoint]
        if point is None:
            return
        
        x, y = point
        
        head_x = self.robot.getAngle("head_z")
        head_y = self.robot.getAngle("head_y")
        
        reset_x, reset_y = False, False
        if np.abs(head_x) > 40:
            if np.random.rand() > 0.95:
                reset_x = True
        else:
            if np.random.rand() > 0.995:
                reset_x = True
        if head_y > 20: #15
            if np.random.rand() > 0.95:
                reset_y = True
        else:
            if np.abs(head_x) > 5:
                if np.random.rand() > 0.995:
                    reset_y = True
        
        if reset_x:
            delta_degrees_x = -head_x
            #print("RESET X")
        else:
            delta_degrees_x = np.arctan2((0.5-x)*np.tan(20*np.pi/180),0.5)*180/np.pi
        if reset_y:
            delta_degrees_y = -head_y - 25
            #print("RESET Y")
        else:
            delta_degrees_y = np.arctan2((0.5-y)*np.tan(20*np.pi/180),0.5)*180/np.pi
        
        angular_speed = 0.04
        limit = 2.0 
        
        if np.abs(delta_degrees_x) > limit:
            self.robot.changeAngle("head_z", delta_degrees_x, angular_speed)
        if np.abs(delta_degrees_y) > limit:
            self.robot.changeAngle("head_y", delta_degrees_y, angular_speed)

        time.sleep(max(np.abs(delta_degrees_x),np.abs(delta_degrees_y))/(1000*angular_speed))
        
