import cv2
import numpy as np
from numpy import ndarray

from game.physics.physics import Physics, PhysicsObject

def force(x):
    return x*x

class FastPhysics(Physics):
    def kustify(self, obj: PhysicsObject):
        img=obj.img(self.edges)
        inter = cv2.bitwise_and(self.edges,img)
        non=cv2.findNonZero(inter)
        if non is None:
            return
        cnt=0
        for p in non:
            p=(p[0][0],p[0][1])
            d = obj.distance(p)
            if d is not None:
                xx, yy = d
                obj.x += xx
                obj.y += yy
                cnt += 1

        if cnt == 0:
            return

        obj.vx = obj.vy = 0


