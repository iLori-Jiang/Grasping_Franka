import sys
import os

'''
output should be:
work_dir:  /home/doyle/Me336/ME336-2021Spring
work_dir:  /home/doyle/Me336/ME336-2021Spring
work_dir:  /home/doyle/Me336/ME336-2021Spring
'''

_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_root_path)
os.chdir(_root_path)
print('work_dir: ', _root_path)

import time
import yaml
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.spatial.transform import Rotation as R

from deepclaw.modules.end2end.yolov5.YOLO5 import Yolo5
# from deepclaw.driver.sensors.camera.Realsense_L515 import Realsense
from realsense_wapper import Realsense


if __name__ == '__main__':
    # camera and robot driver
    print('work_dir: ', _root_path)
    '''
    camera = Realsense('./JHY/config/camera_rs_d435.yaml')

    frame = camera.get_frame()
    color = frame.color_image[0]
    depth_img = frame.depth_image[0]
    '''

    camera = Realsense(frame_width=1280, frame_height=720, fps=30)
    depth, color = camera.get_frame_cv()

    cv2.imshow("img", color)
    cv2.waitKey(1000)

    crop = color[178:542, 433:891]
    cv2.imshow("crop", crop)
    cv2.waitKey(10000)

    cv2.destroyAllWindows()
