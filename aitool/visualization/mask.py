import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_coco_mask(coco, image_file, anns, output_file=None):
    if isinstance(image_file, str):
        img = cv2.imread(image_file)
    elif isinstance(image_file, np.ndarray):
        img = image_file.copy()
    else:
        raise("Wrong input image type!", type(image_file))

    plt.figure(figsize=(8, 8))
    plt.imshow(img)
    
    coco.showAnns(anns)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    if output_file:
        plt.savefig(output_file, bbox_inches='tight', dpi=600, pad_inches=0.0)
        plt.clf()
    else:
        plt.show()