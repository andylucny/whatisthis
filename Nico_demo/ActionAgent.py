from agentspace import Agent, space
import cv2 as cv
import time

class ActionAgent(Agent):

    def __init__(self, robot, namePoints):
        self.robot = robot
        self.namePoints = namePoints
        super().__init__()

    def init(self):
        space.attach_trigger(self.namePoints,self)

    def senseSelectAct(self):
        points = space[self.namePoints]
        if len(points) != 6:
            return
        
        delta_pixels = 0.2
        delta_degrees = 2.0
        angular_speed = 0.04
        x, y = points[2]
        if x < 0.5-delta_pixels:
            robot.changeAngle("head_z", delta_degrees, angular_speed)
        elif x > 0.5+delta_pixels:
            robot.changeAngle("head_z", -delta_degrees, angular_speed)
        if y < 0.5-delta_pixels:
            robot.changeAngle("head_y", delta_degrees, angular_speed)
        elif y > 0.5+delta_pixels:
            robot.changeAngle("head_y", -delta_degrees, angular_speed)

        time.sleep()