from math import sqrt

from game.Object import GameObject
from typing import Tuple
import numpy as np
from numpy import ndarray
import cv2


# interface for physics object
class PhysicsObject(GameObject):
    vx = 0
    vy = 0

    # returns shortest vector to surface
    def distance(self, point: Tuple[float, float]) -> Tuple[float, float]:
        pass

    def img(self, shp) -> ndarray:
        pass


class Circle(PhysicsObject):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r

    def img(self, edg:ndarray) -> ndarray:
        img = np.zeros(edg.shape, dtype=edg.dtype)
        cv2.circle(img, (int(self.x), int(self.y)), self.r, 255, cv2.FILLED)
        return img

    def distance(self, point: Tuple[float, float]):
        px, py = point
        dx, dy = px - self.x, py - self.y
        dsqr = (dx * dx + dy * dy)

        if dsqr <= (self.r * self.r):
            m = sqrt(max(dsqr, 0.1))
            k = (self.r - m) / m
            return k * -dx, k * -dy


# base class for physics with a edge map
class Physics:
    edges: np.array

    def update_map(self, edges: ndarray):
        self.edges = edges
        pass

    def kustify(self, obj: PhysicsObject):
        pass
