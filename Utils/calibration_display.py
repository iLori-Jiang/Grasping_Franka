import sys
import os

_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(_root_path)
os.chdir(_root_path)
print('work_dir: ', _root_path)

from Grasping_Franka.Utils.calibration import check_trans_matrix_from_file

if __name__ == '__main__':
    # filename_npz = './Grasping_Franka/output/cali_data/2021-04-06-16:09:11.591813.npz'
    filename_npz = './Grasping_Franka/output/cali_data/2021-04-06-16:32:10.512707.npz'
    check_trans_matrix_from_file(filename_npz)
