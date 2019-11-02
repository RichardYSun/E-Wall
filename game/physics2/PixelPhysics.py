import cv2
import numpy as np

from game.physics2.Physics import MapPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.physics2.objects.PixelObject import PixelObject
from game.util.Vector2 import Vector2


class PixelPhysics(MapPhysics):

    def __init__(self, R=10):
        super().__init__()
        self.R = R

    def apply_physics(self, obj: PhysicsObject, delta_t):
        edges = self.map.edges

        if isinstance(obj, PixelObject):
            # obj: PixelObject
            xmn, xmx, ymn, ymx = obj.get_bounds()

            best = Vector2(0, 0)
            mn = 1e9
            off = 1e9

            mat = np.zeros(edges.shape, dtype=edges.dtype)
            obj.draw_hitbox(mat)

            R = self.R

            for x in range(-R, R + 1):
                if xmx + x > edges.shape[1]:
                    break
                for y in range(-R, R + 1):
                    if ymx + y > edges.shape[0]:
                        break

                    rect = cv2.bitwise_and(mat[ymn + y:ymx + y, xmn + x:xmx + x],
                                           edges[ymn + y:ymx + y, xmn + x:xmx + x])

                    cnt = cv2.countNonZero(rect)
                    if cnt < mn or (cnt == mn and abs(x) + abs(y) < off):
                        off = abs(x) + abs(y)
                        mn = cnt
                        best = Vector2(x, y)

            obj.translate(best)

            if off != 0:
                obj.vx = obj.vy = 0
