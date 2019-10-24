import cv2

from game.framework import CVMap


class CVer:
    def __init__(self):
        self.lower = 100
        self.higher = 200
        pass

    def do_cv(self, img) -> CVMap:
        edge = cv2.Canny(img, self.lower, self.higher)
        return CVMap(edge)
