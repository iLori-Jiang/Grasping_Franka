import sys
import os

from deepclaw.driver.arms.ArmController import ArmController

import yaml
import numpy as np
from deepclaw.driver.arms.franka.FrankaController import FrankaController


if __name__ == '__main__':
    _root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(_root_path)
    os.chdir(_root_path)
    print('work_dir: ', _root_path)
    FC = FrankaController('./JHY/config/franka.yaml')
    print(FC.getJoint())

    '''
    joint_target = np.array([-0.0137566, 0.0150639, 0.06416, -2.50988, -0.00736516, 2.80153, -1.8411])
    FC.move_j(joint_target)
    pose = [0.5, 0, 0.4, 3.14, 0.0, 0.0]
    FC.move_p(pose)
    # speed_j
    joint_speed = [0, 0, 0, 0, 0, 0, 0.1]
    FC.speed_j(joint_speed)
    time.sleep(2)
    FC.stopSpeed()
    print('===========')
    '''

    FC.move_p([0.3, 0.5, 0.4, 3.14, 0.0, -3.14/4])
    '''
    print('My Cartesian Pose: ', FC.getCartesianPose())

    allState = FC.get_state()
    print('My state: ', allState)
    print('My current position in base: ', allState['TCP_Pose'])
    '''

    # 3D calibration
    # FC.move_p([0.4, 0.0, 0.2, 3.14 - 3.14/2, -3.14/2, 0.0])

    # 2D calibration
    # FC.move_p([0.3855246, -0.008349946, 0.085, 3.14, 0, 0])  # sample point
    # FC.move_p([0.3, 0.0, 0.7, 3.14, 0.0, 0.0]) # move out