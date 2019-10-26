import cv2

from game.framework import CVMap
from numpy import ndarray


class CVer:
    lower = 100
    higher = 200

    def do_cv(self, img:ndarray) -> CVMap:
        edge = cv2.Canny(img, self.lower, self.higher)
        return CVMap(edge)