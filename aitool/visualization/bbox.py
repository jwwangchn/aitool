import cv2
import numpy as np

import aitool


def draw_bbox(img, bbox, color=(0, 0, 255), line_width=2):
    """show rectangle (bbox)

    Args:
        img (np.array): input image
        bbox (list): [xmin, ymin, xmax, ymax]
        color (tuple, optional): draw color. Defaults to (0, 0, 255).
        line_width (int, optional): line width

    Returns:
        np.array: output image
    """
    cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, line_width)

    return img

def draw_confusion_matrix(img, gt_bboxes, pred_bboxes, with_gt_TP=False, line_width=2):
    colors = {'gt_TP':   (255, 255, 0),     # blue
              'pred_TP': (0, 255, 0),       # green
              'FP':      (0, 255, 255),     # yellow
              'FN':      (255, 0, 0)}       # red

    objects = aitool.get_confusion_matrix_indexes(gt_bboxes, pred_bboxes)

    if len(objects) == 0:
        return []
    
    for idx, gt_polygon in enumerate(objects['gt_polygons']):
        if idx in objects['gt_TP_indexes']:
            if with_gt_TP:
                color = colors['gt_TP'][::-1]
                img = aitool.draw_bbox(img, aitool.polygon2bbox(gt_polygon), color=color, line_width=line_width)
        else:
            color = colors['FN'][::-1]
            img = aitool.draw_bbox(img, aitool.polygon2bbox(gt_polygon), color=color, line_width=line_width)
        

    for idx, pred_polygon in enumerate(objects['pred_polygons']):
        if idx in objects['pred_TP_indexes']:
            color = colors['pred_TP'][::-1]
        else:
            color = colors['FP'][::-1]

        img = aitool.draw_bbox(img, aitool.polygon2bbox(pred_polygon), color=color, line_width=line_width)

    return img  