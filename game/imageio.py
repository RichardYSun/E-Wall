import cv2
import pygame

from game.game import GameContext
from game.util import ParamWindow
from game.util.areaselectwindow import AreaSelectWindow
from game.img.images import imread


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
        print('display size', w,h)
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

        ctx = GameContext(img)
        return ctx

    def __del__(self):
        del self.cam_window
        self.cap.release()
