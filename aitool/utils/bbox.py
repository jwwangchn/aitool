import aitool


def drop_invalid_bboxes(bboxes, min_area=2, min_side=2):
    """drop the invalid bboxes

    Args:
        bboxes (list): list of bboxes, (coco format, [xmin, ymin, xmax, ymax])
        min_area (int, optional): min area of bboxes. Defaults to 2.
        min_side (int, optional): min side of bboxes. Defaults to 2.
    
    Return:
        list: list of keep bboxes (coco format, [xmin, ymin, xmax, ymax])
    """
    results = []
    for bbox in bboxes:
        cx, cy, w, h = aitool.xyxy2cxcywh(bbox)

        if w * h < min_area:
            continue

        if w < min_side or w < min_side:
            continue
        
        results.append([int(_) for _ in bbox])
    
    return results
    
    