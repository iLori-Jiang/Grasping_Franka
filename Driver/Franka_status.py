import sys
import os
from deepclaw.driver.arms.franka.FrankaController import FrankaController

if __name__ == '__main__':
    _root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(_root_path)
    os.chdir(_root_path)
    print('work_dir: ', _root_path)
    FC = FrankaController('./Grasping_Franka/config/franka.yaml')

    # print('My Cartesian Pose: ', FC.getCartesianPose())

    allState = FC.get_state()
    print('My state: ', allState)
    # move_p position
    print('My current position in base: ', allState['TCP_Pose'])
    # move_j position
    print('My current joint space: ', FC.getJoint())
