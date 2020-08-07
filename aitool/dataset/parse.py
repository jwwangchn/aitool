import numpy as np
import tqdm
from pycocotools.coco import COCO
import pycocotools.mask as maskUtils

import mmcv
import aitool


class PklParserBase():
    """parse the pkl file (generated by mmdetection)
    """
    def __init__(self,
                 pkl_file,
                 ann_file,
                 score_threshold=0.05):
        self.score_threshold = score_threshold

        if isinstance(pkl_file, str):
            results = mmcv.load(pkl_file)
        elif isinstance(pkl_file, (list, tuple)):
            results = pkl_file
        else:
            raise TypeError(f'do not support the pkl file type: {type(pkl_file)}')

        coco = COCO(ann_file)
        self.img_ids = coco.get_img_ids()
        self.cat_ids = coco.get_cat_ids()
        self.img_fns = []

        print("begin to convert pkl file to specific format")
        self.objects = dict()
        for idx, img_id in tqdm.tqdm(enumerate(self.img_ids)):
            info = coco.load_imgs([img_id])[0]
            img_name = aitool.get_basename(info['file_name'])
            self.img_fns.append(img_name)
            result = results[idx]

            self.objects[img_name] = self._convert_items(result)

    def _convert_items(self, result):
        """convert the result (single image) in pkl file to specific format (default: Faster R-CNN, bbox) 

        Args:
            result (tuple): detection result of single image

        Return:
            list: converted objects
        """
        objects = []

        for label in range(len(result)):
            bboxes = result[label]
            for i in range(bboxes.shape[0]):
                data = dict()
                data['bbox'] = aitool.xyxy2xywh(bboxes[i][:4])
                data['score'] = float(bboxes[i][4])
                data['category_id'] = self.cat_ids[label]
                objects.append(data)

        return objects

    def __call__(self, image_fn):
        if image_fn in self.objects.keys():
            return self.objects[image_fn]
        else:
            print("{} is not in pkl".format(image_fn))
            return []


class PklParserMask(PklParserBase):
    def _convert_items(self, result):
        """convert the result (single image) in pkl file to specific format (Mask R-CNN, bbox + mask) 

        Args:
            result (tuple): detection result of single image

        Return:
            list: converted objects
        """
        objects = []

        det, seg = result
        for label in range(len(det)):
            bboxes = det[label]
            if isinstance(seg, tuple):
                segms = seg[0][label]
            else:
                segms = seg[label]

            for i in range(bboxes.shape[0]):
                data = dict()
                data['bbox'] = aitool.xyxy2xywh(bboxes[i][:4])
                data['score'] = float(bboxes[i][4])
                data['category_id'] = self.cat_ids[label]
                if isinstance(segms[i]['counts'], bytes):
                    segms[i]['counts'] = segms[i]['counts'].decode()
                data['segmentation'] = segms[i]
                objects.append(data)

        return objects