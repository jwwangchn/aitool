import cv2

def draw_text(img, text, position, color=(0, 0, 255)):
    cv2.putText(img, text, (int(position[0]), int(position[1])), cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1.0, color=color, thickness=2, lineType=8)

    return img