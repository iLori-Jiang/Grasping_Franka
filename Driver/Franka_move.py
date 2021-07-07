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

    # -----look this
    # FC.move_p([0.420997, 0.123974, 0.350515, 3.14, -0.0, 2.037585010536264])

    # FC.move_p([0.5437009, -0.01225163, 0.360596, 3.14, 0.0, 1.539121572633681])


