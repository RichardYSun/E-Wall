import cv2
from numpy import ndarray
import numpy as np
import os

from game.util.areaselectwindow import AreaSelectWindow

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class ImageIO:

    def __init__(self, img_name='test2', proj_w=1000, proj_h=500):

        if img_name is None:
            self.img_src=None
            self.cap = cv2.VideoCapture(1)
            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.img_src = cv2.imread(ROOT_DIR + '/test_images/' + img_name + '.bmp')
            w = self.img_src.shape[1]
            h = self.img_src.shape[0]

        self.projector_window = AreaSelectWindow(proj_w, proj_h, 'projector window', (255, 0, 0))
        self.cam_window = AreaSelectWindow(w, h, 'camera window', (255, 0, 0))

    def show(self, img: ndarray):
        self.projector_window.show(img)

    def get_img(self):
        if self.img_src is None:
            ret, img = self.cap.read()
            cv2.flip(img, 1, img)
            if ret is False:
                raise Exception('could not read image')
        else:
            img = np.copy(self.img_src)

        sub = self.cam_window.get_sub_image(img)

        self.cam_window.show(img)

        return sub

    def __del__(self):
        del self.cam_window
        del self.projector_window
        self.cap.release()
