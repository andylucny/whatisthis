from agentspace import Agent, space
import numpy as np
import time

def loadAnimation(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        concerned_dofs = eval(lines[0])
        recorded_poses = []
        for line in lines[1:]:
            recorded_pose = eval(line[:-1])
            recorded_poses.append(recorded_pose)

        timeindex = np.where(np.array(dofs) == 'timestamp')[0][0]
        timestamps = []
        for pose in poses:
            timestamps.append(pose[timeindex])

        timestamps = np.array(timestamps,np.float64)/1000.0 #[s]
        durations = [timestamps[0]] + list(timestamps[1:]-timestamps[:-1])

        return concerned_dofs, recorded_poses, durations

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
    
class ActionArmAgent(Agent):

    def __init__(self, robot, nameAnim):
        self.robot = robot
        self.nameAnim = nameAnim
        super().__init__()
        
    def init(self):
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
            move_to_position_through_time(command0,0.5)
            
            # replay the animation
            durations = [ duration * 2 for duration in durations ] # slow down 2x
            play_movement(self.robot, dofs, poses, durations)
    
            time.sleep(1)
