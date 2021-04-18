import os
import sys

_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_root_path)
os.chdir(_root_path)
print('work_dir: ', _root_path)

import time
import csv
from datetime import datetime
import yaml

import numpy as np
import cv2 as cv

# import gripper_control as gripper
from Grasping_Franka.Driver.CH340 import ComSwitch

# from deepclaw.driver.sensors.camera.Realsense_L515 import Realsense
from Grasping_Franka.Driver.realsense_wapper import Realsense
from deepclaw.driver.arms.franka.FrankaController import FrankaController
from Grasping_Franka.Utils.get_obj_by_color import get_obj_bbox
from deepclaw.modules.calibration.Calibration2D import Calibration2D


def read_cfg(path):
    with open(path, 'r') as stream:
        out = yaml.safe_load(stream)
    return out


def load_cam_T_base_matrix(file_path):
    H = np.loadtxt(file_path, delimiter=',')

    cam_T_base_R = H[:3, :3]
    cam_T_base_t = H[:3, 3:].squeeze(1)

    return cam_T_base_R, cam_T_base_t


def location_transformation(crop_bounding, hand_eye):
    bbox = [0, 0, 0, 0]
    temp = [0.5, 0]
    time.sleep(0.5)

    ''' Load image '''
    isObject = False
    while (isObject == False):
        depth_img, color_img = cam.get_frame_cv()

        bbox = get_obj_bbox(color_img, crop_bounding[0], crop_bounding[1], crop_bounding[2], crop_bounding[3])

        cv.rectangle(color_img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

        obj_center_row = int(bbox[1] + bbox[3] / 2)
        obj_center_col = int(bbox[0] + bbox[2] / 2)
        # print("row: {}, col: {}".format(obj_center_row, obj_center_col))
        if (bbox[2] * bbox[3] >= check_threshold):
            isObject = True
            cv.circle(color_img, (obj_center_col, obj_center_row), 2, (0, 255, 0), 2)

            ''' Visualization '''
            cv.imshow('result', color_img)
            cv.waitKey(10)

            temp = hand_eye.cvt(obj_center_col, obj_center_row)
            break
        else:
            print("No object detected!")
            time.sleep(2)

    ''' Compute target coordinate in camera frame '''
    if bbox[3] >= bbox[2]:
        angle = initial_angle
    else:
        angle = initial_angle - 1.57

    # grasp pose in euler angle
    target_in_base = [temp[0], temp[1], effector_offset, 3.14, 0, angle]

    return target_in_base


if __name__ == '__main__':
    """ Initialization """
    # camera and robot driver
    print('work_dir: ', _root_path)
    cam = Realsense(frame_width=1280, frame_height=720, fps=30)
    cfg = read_cfg('./Grasping_Franka/config/2D_grasping.yaml')
    arm = FrankaController('./Grasping_Franka/config/franka.yaml')
    # cs = ComSwitch()  # gripper

    ''' Loading config '''
    initial_pose = cfg['initial_position']  # should be outside the grasping area
    initial_pose[2] += -0.17
    initial_pose[5] += -1.57
    drop_position = cfg['drop_position']
    drop_position[2] += -0.17
    drop_position[5] += -1.57
    check_position = cfg['check_position']
    check_position[2] += -0.17
    check_position[5] += -1.57

    grasp_pre_offset = cfg['grasp_prepare_offset']
    effector_offset = cfg['effector_offset']  # distance between the flange and the center of gripper, positive value
    effector_offset += -0.14
    initial_angle = cfg['initial_angle']
    initial_angle += -1.57

    check_threshold = cfg['check_threshold']

    attmp_num = cfg['attmp_num']  # total grasp number

    crop_bounding = cfg['grasping_area']
    cali_path = './configs/basic_config/cali2D.yaml'
    hand_eye = Calibration2D(cali_path)
    print("Calibration2D complete")

    print("Moving to initial position...")
    arm.move_p(initial_pose, 0.8, 0.8)
    print("Moving to initial position... Done")

    stored_exception = None

    ''' Ready to store the data '''
    csv_filename = "./Grasping_Franka/output/result/" + str(datetime.now()).replace(' ', '-') + ".csv"
    csv_header = ['num', 'if_success']

    with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

    ''' Starting Grasping '''
    # arm.move_p(check_position) # Test
    current_num = 0  # recording the grasping attempt
    while current_num < attmp_num:

        try:
            if stored_exception:
                break

            ''' Get the location of the object '''
            target_in_base = location_transformation(crop_bounding=crop_bounding, hand_eye=hand_eye)

            ''' Exerting grasping '''
            prepare_pos = target_in_base.copy()  # pose: perpendicular to the plane
            prepare_pos[2] = prepare_pos[2] + grasp_pre_offset
            arm.move_p(prepare_pos)

            # cs.open()
            arm.gripperOpen()
            arm.move_p(target_in_base, velocity=0.1, accelerate=0.1)
            # cs.close()
            arm.gripperGrasp()
            time.sleep(0.5)

            ''' Move to check position '''
            lift_up = target_in_base.copy()
            lift_up[2] = check_position[2]
            arm.move_p(lift_up)
            arm.move_p(check_position)

            ''' Perform success check '''
            _, color_check = cam.get_frame_cv()
            bbox_check = get_obj_bbox(color_check, crop_bounding[0], crop_bounding[1], crop_bounding[2],
                                      crop_bounding[3])

            data = []

            cv.imshow('result', color_check)
            cv.waitKey(10)

            print("current area = %f" % (bbox_check[2] * bbox_check[3]))
            print("threshold area = %f" % check_threshold)

            if (bbox_check[2] * bbox_check[3] < check_threshold):
                print("Grasping SUCCESS in attempt {}".format(current_num))
                data.append(str(current_num))
                data.append(str(1))  # Success
            else:
                print("Grasping FAIL in attempt {}".format(current_num))
                data.append(str(current_num))
                data.append(str(0))  # Fail

            with open(csv_filename, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)

            ''' Move to drop position and drop object '''
            drop_up = drop_position.copy()
            drop_up[2] = check_position[2]
            arm.move_p(drop_up)
            arm.move_p(drop_position)
            # cs.open()
            arm.gripperOpen()

            ''' Back to initial position '''
            depart_pos = drop_position.copy()
            depart_pos[2] = depart_pos[2] + grasp_pre_offset
            arm.move_p(depart_pos)
            arm.move_p(initial_pose)

            current_num += 1

        except KeyboardInterrupt:
            stored_exception = sys.exc_info()

    cv.destroyAllWindows()
