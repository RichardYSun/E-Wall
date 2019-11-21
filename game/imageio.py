import cv2
import pygame

from game.game import GameContext
from game.util import ParamWindow
from game.util.areaselectwindow import AreaSelectWindow
from game.util.moreimutils import imread


class ImageIO:

    def __init__(self, img_name='test2'):

        if img_name is None:
            self.img_src = None
            self.cap = cv2.VideoCapture(ParamWindow.get_int('camera number', 5, 0))
            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.img_src = imread('test/' + img_name + '.bmp')
            w = self.img_src.shape[1]
            h = self.img_src.shape[0]
        pygame.init()
        pygame.display.set_mode((w, h), pygame.RESIZABLE)

        self.cam_window = AreaSelectWindow(w, h, 'camera window', (255, 0, 0))

    def get_img(self) -> GameContext:
        if self.img_src is None:
            ret, img = self.cap.read()
            cv2.flip(img, 1, img)
            if ret is False:
                raise Exception('could not read image')
        else:
            img = self.img_src

        downscale = ParamWindow.get_int('downscale', 100, 100)
        w = int(downscale * img.shape[0] / 100)
        h = int(downscale * img.shape[1] / 100)

        ctx = GameContext(cv2.resize(img, (w, h)))
        ctx.downscale = downscale / 100.0
        return ctx

    def __del__(self):
        del self.cam_window
        self.cap.release()
