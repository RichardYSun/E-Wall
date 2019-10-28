import cv2
from numpy import ndarray


class Projector:
    window_name = 'projector'

    def __init__(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def show(self, img: ndarray):
        cv2.imshow(self.window_name, img)

class Camera:
    window_name='camera'
    def __init__(self, img_src=None):
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)


    def update(self, img_in: ndarray):
        cv2.imshow(self.window_name, img_in)
