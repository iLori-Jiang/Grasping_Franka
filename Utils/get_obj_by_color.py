import sys
import os

_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(_root_path)
os.chdir(_root_path)
print('work_dir: ', _root_path)

# from deepclaw.driver.sensors.camera.Realsense_L515 import Realsense
from Grasping_Franka.Driver.realsense_wapper import Realsense
import cv2


def get_obj_bbox(img, y1, y2, x1, x2):
    crop = img[y1:y2, x1:x2]

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (4, 4))
    _, binary = cv2.threshold(blur, 130, 256, cv2.THRESH_BINARY)

    x, y, w, h = cv2.boundingRect(binary)

    x += x1
    y += y1

    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    # cv2.imshow('original', img)
    # cv2.imshow('crop', crop)
    # cv2.imshow('Gray image', gray)
    # cv2.imshow('Blur', blur)
    # cv2.imshow('binary', binary)
    # cv2.imshow('bbox', img)

    # cv2.waitKey(10)

    return x, y, w, h


def check_gripper_bbox(img, y1, y2, x1, x2):

    crop = img[y1:y2, x1:x2]

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (4, 4))
    _, binary = cv2.threshold(blur, 130, 256, cv2.THRESH_BINARY)

    x, y, w, h = cv2.boundingRect(binary)

    x += x1
    y += y1

    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    # cv2.imshow('original', img)
    # cv2.imshow('crop', crop)
    # cv2.imshow('Gray image', gray)
    # cv2.imshow('Blur', blur)
    # cv2.imshow('binary', binary)
    # cv2.imshow('bbox', img)

    # cv2.waitKey(10)

    return x, y, w, h


if __name__ == '__main__':

    """ Initialization """
    # camera and robot driver
    print('work_dir: ', _root_path)
    cam = Realsense(frame_width=1280, frame_height=720, fps=30, exposure=800, white_balance=3500, contrast=80, sharpness=80)

    _, img = cam.get_frame_cv()

    y1 = 269
    y2 = 542
    x1 = 475
    x2 = 799

    crop = img[y1:y2, x1:x2]

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (4, 4))
    _, binary = cv2.threshold(blur, 130, 256, cv2.THRESH_BINARY)

    x, y, w, h = cv2.boundingRect(binary)

    x += x1
    y += y1

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print("bbox: {}, {}, {}, {}".format(x, y, w, h))

    cv2.imshow('original', img)
    cv2.imshow('crop', crop)
    # cv2.imshow('Gray image', gray)
    # cv2.imshow('Blur', blur)
    cv2.imshow('binary', binary)
    cv2.imshow('bbox', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
