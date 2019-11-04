import cv2
from numpy import ndarray
import numpy as np
import os

from game.util import ParamWindow
from game.util.areaselectwindow import AreaSelectWindow
from game.util.imreader import imread


class ImageIO:

    def __init__(self, img_name='test2', proj_w=1000, proj_h=500):

        if img_name is None:
            self.img_src = None
            self.cap = cv2.VideoCapture(ParamWindow.get_int('camera number', 5, 0))
            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.img_src = imread('test\\' + img_name + '.bmp')
            w = self.img_src.shape[1]
            h = self.img_src.shape[0]

        self.projector_window = AreaSelectWindow(proj_w, proj_h, 'projector window', (255, 0, 0))
        self.cam_window = AreaSelectWindow(w, h, 'camera window', (255, 0, 0))

    def show(self, img: ndarray):
        proj_w = ParamWindow.get_int('proj width', 2000, 1000)
        proj_h = ParamWindow.get_int('proj height', 2000, 500)
        img = cv2.resize(img, (proj_w, proj_h))
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

        game_w = ParamWindow.get_int('game map width', 1600, 500)
        game_h = ParamWindow.get_int('game map height', 1900, 250)
        sub = cv2.resize(sub, (game_w, game_h))

        self.cam_window.show(img)

        return sub

    def __del__(self):
        del self.cam_window
        del self.projector_window
        self.cap.release()
