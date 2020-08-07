import numpy as np
import cv2
import pycocotools.mask as maskUtils


def segm2rbbox(segms):
    """convert segms to rbbox

    Args:
        segms (coco format): input segmentation

    Returns:
        list: pointobb and thetaobb
    """
    mask = maskUtils.decode(segms).astype(np.bool)
    gray = np.array(mask*255, dtype=np.uint8)
    
    contours = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    if contours != []:
        cnt = max(contours, key = cv2.contourArea)
        rect = cv2.minAreaRect(cnt)
        x, y, w, h, theta = rect[0][0], rect[0][1], rect[1][0], rect[1][1], rect[2]
        theta = theta * np.pi / 180.0
        thetaobb = [x, y, w, h, theta]
        pointobb = thetaobb2pointobb([x, y, w, h, theta])
    else:
        thetaobb = [0, 0, 0, 0, 0]
        pointobb = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    return thetaobb, pointobb

def thetaobb2pointobb(thetaobb):
    """convert thetaobb to pointobb

    Args:
        thetaobb (list): [cx, cy, w, h, theta (rad/s)]

    Returns:
        list: [x1, y1, x2, y2, x3, y3, x4, y4]
    """
    box = cv2.boxPoints(((thetaobb[0], thetaobb[1]), (thetaobb[2], thetaobb[3]), thetaobb[4] * 180.0 / np.pi))
    box = np.reshape(box, [-1, ]).tolist()
    pointobb = [box[0], box[1], box[2], box[3], box[4], box[5], box[6], box[7]]

    return pointobb