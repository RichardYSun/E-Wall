import cv2

from game.physics2.objects.PhysicsObject import PhysicsObject
from numpy import ndarray

from game.physics2.objects.PixelObject import PixelObject


class Circle(PixelObject):
    obj_type = 1

    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r

    def draw_hitbox(self, img: ndarray):
        cv2.circle(img, (int(self.x), int(self.y)), self.r, 255, cv2.FILLED)

    def get_bounds(self):
        x, y, r = int(self.x), int(self.y), self.r
        return x - r, x + r, y - r, y + r
