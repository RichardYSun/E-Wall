import cv2
from numpy import ndarray
import numpy as np
import os

from game.util.AreaSelectWindow import AreaSelectWindow

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
tmp = cv2.imread(ROOT_DIR + '/test_images/test2.bmp')


class ImageIO:
    proj_img: ndarray = None

    def __init__(self, img_src: ndarray = tmp, proj_w=1000, proj_h=500):
        self.img_src = img_src

        if img_src is None:
            self.cap = cv2.VideoCapture(0)
            w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        else:
            w = img_src.shape[1]
            h = img_src.shape[0]

        self.proj_w = proj_w
        self.proj_h = proj_h

        self.projector_window = AreaSelectWindow(proj_w, proj_h, 'projector window', (255, 0, 0))
        self.cam_window = AreaSelectWindow(w, h, 'camera window', (255, 0, 0))

    def show(self, img: ndarray):
        if self.proj_img is None:
            self.proj_img = np.zeros((self.proj_w, self.proj_h), img.dtype)

        p = self.projector_window

        self.proj_img[ p.l:p.r,p.t:p.b] = img

        self.projector_window.show(self.proj_img)

    def get_img(self):
        if self.img_src is None:
            ret, img = self.cap.read()
            if ret is False:
                raise Exception('could not read image')
        else:
            img = np.copy(self.img_src)

        sub = self.cam_window.get_sub_image(img)

        w = self.projector_window.b - self.projector_window.t
        h = self.projector_window.r - self.projector_window.l

        scaled = cv2.resize(sub, (w, h))

        self.cam_window.show(img)

        return scaled

    def __del__(self):
        del self.cam_window
        del self.projector_window
        self.cap.release()
