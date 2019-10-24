import cv2

from .framework import CVMap


class CVer:
    def __init__(self):
        self.lower = 100
        self.higher = 200
        pass

    def do_cv(self, img) -> CVMap:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, self.lower, self.higher)
        return CVMap(edge)
