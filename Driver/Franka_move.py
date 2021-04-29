import sys
import os

from deepclaw.driver.arms.ArmController import ArmController

import yaml
import numpy as np
from deepclaw.driver.arms.franka.FrankaController import FrankaController


if __name__ == '__main__':
    _root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(_root_path)
    os.chdir(_root_path)
    print('work_dir: ', _root_path)
    FC = FrankaController('./Grasping_Franka/config/franka.yaml')
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

    FC.move_p([0.35, 0.5, 0.4, 3.14, 0, 0.785])
    print(FC.getJoint())

    FC.move_j([0.016889297269194355,-0.9558921143950705,-0.006456802549563263,-2.1330765712441857,-0.00542805631322928,1.1762153487693685,-1.558628718536133])
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