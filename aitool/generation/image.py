import numpy as np
import cv2


def generate_image(height=512, 
                   width=512, 
                   color=(255, 255, 255)):
    """generate specific size image with specific color

    Args:
        height (int, optional): image height. Defaults to 512.
        width (int, optional): image width. Defaults to 512.
        color (tuple, optional): image init color. Defaults to (255, 255, 255).

    Returns:
        np.array: generated image
    """
    if type(color) == tuple:
        b = np.full((height, width, 1), color[0], dtype=np.uint8)
        g = np.full((height, width, 1), color[1], dtype=np.uint8)
        r = np.full((height, width, 1), color[2], dtype=np.uint8)
        img = np.concatenate((b, g, r), axis=2)
    else:
        gray = np.full((height, width), color, dtype=np.uint8)
        img = gray

    return img