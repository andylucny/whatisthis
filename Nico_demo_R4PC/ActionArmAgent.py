from agentspace import Agent, space
import numpy as np
import time

def loadAnimation(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        dofs = eval(lines[0])
        poses = []
        for line in lines[1:]:
            pose = eval(line[:-1])
            poses.append(pose)

        timeindex = np.where(np.array(dofs) == 'timestamp')[0][0]
        timestamps = []
        for pose in poses:
            timestamps.append(pose[timeindex])

        timestamps = np.array(timestamps,np.float64)/1000.0 #[s]
        durations = [timestamps[0]] + list(timestamps[1:]-timestamps[:-1])

        return dofs, poses, durations

    print(filename,"does not exist")
    return None, None, None

def move_to_position_through_time(robot, target_positions, duration):
    if duration == 0:
        return
    # calculate current angular speed
    import copy
    # get the current positions of all joints to move
    current_positions = copy.deepcopy(target_positions)
    for joint in current_positions:
        current_positions[joint] = robot.getAngle(joint)
    speed_to_reach = {
        k: abs(
            (float(current_positions[k]) - float(target_positions[k])) / float(1260*duration)
        )
        for k in current_positions
    }
    for joi in target_positions:
        robot.setAngle(
            joi,
            float(target_positions[joi]),
            speed_to_reach[joi],
        )

def play_movement(robot, dofs, poses, durations):
    for pose,duration in zip(poses,durations):
        # Move all joints in the subset to the postion
        command = {dof : angle for dof, angle in zip(dofs, pose) if dof != 'timestamp' }
        move_to_position_through_time(robot, command, duration)
        time.sleep(duration)
        
def set_standard_arm_position(robot):
    dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_thumb_z', 'r_thumb_x', 'r_indexfinger_x', 'r_middlefingers_x']
        +  ['l_shoulder_z', 'l_shoulder_y', 'l_arm_x', 'l_elbow_y', 'l_wrist_z', 'l_wrist_x', 'l_thumb_z', 'l_thumb_x', 'l_indexfinger_x', 'l_middlefingers_x']
    pose = [-8.0, -15.0, 16.0, 74.0, -24.0, 35.0, -71.0, -104.0, -180.0, -180.0]
        +  [-8.0, -15.0, 16.0, 74.0, -24.0, 35.0, -71.0, -104.0, -180.0, -180.0]
    command = {dof : angle for dof, angle in zip(dofs, pose)}
    duration = 1.0
    move_to_position_through_time(robot, command, duration)
    time.sleep(duration)
    
class ActionArmAgent(Agent):

    def __init__(self, robot, nameAnim):
        self.robot = robot
        self.nameAnim = nameAnim
        super().__init__()
        
    def init(self):
        set_standard_arm_position(self.robot)
        space.attach_trigger(self.nameAnim,self)

    def senseSelectAct(self):
        anim = space[self.nameAnim]
        dofs, poses, durations = loadAnimation(anim+'.txt')
        if dofs is not None:
            # enable torque
            for dof in dofs:
                if dof != 'timestamp':
                    self.robot.enableTorque(dof)

            # go to initialposition
            command0 = {dof : angle for dof, angle in zip(dofs, poses[0]) if dof != 'timestamp' }
            move_to_position_through_time(self.robot,command0,0.5)
            
            # replay the animation
            durations = [ duration * 2 for duration in durations ] # slow down 2x
            play_movement(self.robot, dofs, poses, durations)
    
            time.sleep(1)
