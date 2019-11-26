import cv2
import pygame

from game.game import GameContext
from game.util import ParamWindow
from game.util.areaselectwindow import AreaSelectWindow
from game.img.images import imread


class ImageIO:
    cap = None

    def __init__(self, img_name='test2'):

        if img_name is None:
            self.img_src = None
            if ImageIO.cap is None:
                ImageIO.cap = cv2.VideoCapture(ParamWindow.get_int('camera number', 5, 0))
            self.cap=ImageIO.cap
            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.img_src = imread('test/' + img_name )
            w = self.img_src.shape[1]
            h = self.img_src.shape[0]

        print('Input size:', w, h)

        pygame.display.set_mode((w, h), pygame.RESIZABLE)

        self.cam_window = AreaSelectWindow(w, h, 'camera window', (255, 0, 0))

    def get_img(self) -> GameContext:
        if self.img_src is None:
            ret, img = self.cap.read()
            if ret is False:
                raise Exception('could not read image')

            flip = ParamWindow.get_int('flip image', 1, 1)
            if flip:
                cv2.flip(img, 1, img)
        else:
            img = self.img_src.copy()

        self.cam_window.show(img)
        img = self.cam_window.get_sub_image(img)

        ctx = GameContext(img)
        return ctx

    def __del__(self):
        del self.cam_window
        if self.cap is not None:
            self.cap.release()
