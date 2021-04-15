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
from CH340 import ComSwitch

# from deepclaw.driver.sensors.camera.Realsense_L515 import Realsense
from realsense_wapper import Realsense
from deepclaw.driver.arms.franka.FrankaController import FrankaController
from get_obj_by_color import get_obj_bbox, check_gripper_bbox

from deepclaw.driver.arms.ArmController import ArmController

def read_cfg(path):
    with open(path, 'r') as stream:
        out = yaml.safe_load(stream)
    return out


def load_cam_T_base_matrix(file_path):
    H = np.loadtxt(file_path, delimiter=',')

    cam_T_base_R = H[:3, :3]
    cam_T_base_t = H[:3, 3:].squeeze(1)

    return cam_T_base_R, cam_T_base_t


def location_transformation():
    time.sleep(0.5)

    ''' Load image '''
    depth_img, color_img = cam.get_frame_cv()

    bbox = get_obj_bbox(color_img, y1, y2, x1, x2)

    cv.rectangle(color_img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

    obj_center_row = int(bbox[1] + bbox[3] / 2)
    obj_center_col = int(bbox[0] + bbox[2] / 2)
    # print("row: {}, col: {}".format(obj_center_row, obj_center_col))

    cv.circle(color_img, (obj_center_col, obj_center_row), 2, (0, 255, 0), 2)

    ''' Visualization '''
    cv.imshow('result', color_img)
    cv.waitKey(10)

    ''' Compute target coordinate in camera frame '''
    target_in_cam_z = depth_img[obj_center_row, obj_center_col] * cam.depth_scale
    target_in_cam_x = np.multiply(obj_center_col - cam.intrinsics['cx'], target_in_cam_z / cam.intrinsics['fx'])
    target_in_cam_y = np.multiply(obj_center_row - cam.intrinsics['cy'], target_in_cam_z / cam.intrinsics['fy'])

    print("Target in camera frame:\n", [target_in_cam_x, target_in_cam_y, target_in_cam_z])

    target_in_cam = np.array([target_in_cam_x, target_in_cam_y, target_in_cam_z])
    target_in_base = R.dot(target_in_cam) + t

    print("Target in base frame:\n", target_in_base)

    return target_in_base


def print_detection_info(res):
    print("Detection number: ", res.size())
    print("----------------------------------")
    for r in res:
        print("classid: ", r.classid)


if __name__ == '__main__':
    """ Initialization """
    # camera and robot driver
    print('work_dir: ', _root_path)
    cam = Realsense(frame_width=1280, frame_height=720, fps=30)
    cfg = read_cfg('./Grasping_Franka/config/grasping _colorseg.yaml')
    arm = FrankaController('./Grasping_Franka/config/franka.yaml')
    # cs = ComSwitch()    # gripper

    ''' Loading config '''
    initial_pose = cfg['initial_position']  # should be outside the grasping area
    # check_position = cfg['check_position']
    drop_position = cfg['drop_position']

    grasp_pre_offset = cfg['grasp_prepare_offset']
    effector_offset = cfg['effector_offset']  # distance between the flange and the center of gripper, positive value

    check_threshold = cfg['check_threshold']

    attmp_num = cfg['attmp_num']  # total grasp number

    cropping_area_temp = cfg['grasping_area']

    y1 = cropping_area_temp[0]
    y2 = cropping_area_temp[1]
    x1 = cropping_area_temp[2]
    x2 = cropping_area_temp[3]

    ''' Load calibration matrix '''
    R, t = load_cam_T_base_matrix(cfg['matrix_path'])
    print("Load R, t from file:\nR:\n", R, "\nt:\n", t)

    print("Moving to initial position...")
    arm.move_p(initial_pose)
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
    current_num = 0     # recording the grasping attempt
    while current_num < attmp_num:

        try:
            if stored_exception:
                break

            ''' Get the location of the object '''
            target_in_base = location_transformation()

            ''' Exerting grasping '''
            prepare_pos = [target_in_base[0], target_in_base[1], target_in_base[2] + grasp_pre_offset + effector_offset,
                           3.14, 0, 0]  # pose: perpendicular to the plane
            arm.move_p(prepare_pos)

            # cs.open()
            arm.gripperOpen()
            arm.move_p([target_in_base[0], target_in_base[1], target_in_base[2] + effector_offset, 3.14, 0, 0])
            # cs.close()
            arm.gripperGrasp()
            time.sleep(0.5)

            ''' Move to check position '''
            # arm.move_p(check_position)
            arm.move_p(initial_pose)

            ''' Perform success check '''
            _, color_check = cam.get_frame_cv()
            bbox_check = get_obj_bbox(color_check, y1, y2, x1, x2)

            data = []

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

            '''
            with open(csv_filename, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            '''

            ''' Move to drop position and drop object '''
            arm.move_p(drop_position)
            # cs.open()
            arm.gripperOpen()

            ''' Back to initial position '''
            arm.move_p(initial_pose)

            current_num += 1

        except KeyboardInterrupt:
            stored_exception = sys.exc_info()

    cv.destroyAllWindows()
