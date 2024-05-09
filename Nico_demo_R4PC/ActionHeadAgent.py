from agentspace import Agent, space
import numpy as np
import cv2 as cv
import time
from scipy.optimize import curve_fit

headLimits = [ # head_y ... limit head_z
    [-50,  2],
    [-46, 13],
    [-40, 27],
    [-35, 30],
    [-30, 33],
    [-25, 40],
    [-20, 51],
    [-16, 89],
]

hx, hy = np.array(headLimits).T

def func(x,a,b,c,d,e,f):
    return a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f

coefs, _ = curve_fit(func, hx, hy)

def funcinstance(x):
    return np.int32(func(x,coefs[0],coefs[1],coefs[2],coefs[3],coefs[4],coefs[5]))

#print(funcinstance(hx))
#print(hy)

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
        
        limit_x = funcinstance(head_y)
        
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
        
        if head_y + delta_degrees_y <= -limit_x+1:
            delta_degrees_y = 0.0
        if head_y + delta_degrees_y >= limit_x-1:
            delta_degrees_y = 0.0
        
        angular_speed = 0.04
        limit = 2.0 
        
        if np.abs(delta_degrees_x) > limit:
            self.robot.changeAngle("head_z", delta_degrees_x, angular_speed)
        if np.abs(delta_degrees_y) > limit:
            self.robot.changeAngle("head_y", delta_degrees_y, angular_speed)

        time.sleep(max(np.abs(delta_degrees_x),np.abs(delta_degrees_y))/(1000*angular_speed))
        
