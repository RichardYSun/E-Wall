from math import sqrt

from game.Object import GameObject
from typing import Tuple
import numpy as np
from numpy import ndarray


# interface for physics object
class PhysicsObject(GameObject):
    vx = 0
    vy = 0

    # returns shortest vector to surface
    def distance(self, point: Tuple[float, float]) -> Tuple[float, float]:
        pass


class Circle(PhysicsObject):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r

    def distance(self, point: Tuple[float, float]):
        px, py = point
        dx, dy = px - self.x, py - self.y
        dsqr = (dx * dx + dy * dy)
        if dsqr <= (self.r * self.r):
            m = sqrt(dsqr)
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


class ShittyPhysics(Physics):
    physical: ndarray

    def update_map(self, edges: ndarray):
        super().update_map(edges)
        self.physical = np.argwhere(edges > 0)

    def kustify(self, obj: PhysicsObject):
        tx, ty = 0, 0
        cnt = 0
        for p in self.physical:
            p = (p[1], p[0])
            d = obj.distance(p)
            if d is not None:
                xx, yy = d
                tx += xx
                ty += yy
                cnt += 1

        if cnt == 0:
            return

        tx /= cnt
        ty /= cnt

        obj.x += tx
        obj.y += ty
        obj.vx=obj.vy=0
