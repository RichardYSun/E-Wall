import numpy as np
from numpy import ndarray

from game.physics.physics import Physics, PhysicsObject


class ShittyPhysics(Physics):
    physical: ndarray

    def update_map(self, edges: ndarray):
        super().update_map(edges)
        self.physical = np.argwhere(edges !=0)

    def kustify(self, obj: PhysicsObject):
        #tx, ty = 0, 0
        cnt = 0
        for p in self.physical:
            p = (p[1], p[0])
            d = obj.distance(p)
            if d is not None:
                xx, yy = d
                obj.x += xx
                obj.y += yy
                cnt += 1

        if cnt == 0:
            return


        obj.vx=obj.vy=0