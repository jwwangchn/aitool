import cv2
import matplotlib.pyplot as plt


def show_coco_mask(coco, image_file, anns, output_file=None):
    img = cv2.imread(image_file)
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