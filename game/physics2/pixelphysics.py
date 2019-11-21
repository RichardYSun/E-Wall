import cv2
import numpy as np
from numpy.core.multiarray import ndarray

from game.game import GameContext
from game.physics2.collisiontypes import COLLISION_STICK, COLLISION_SLIDE, COLLISION_BOUNCE
from game.physics2.physics import Physics
from game.physics2.objects.physicsobject import PhysicsObject
from game.physics2.objects.pixelobject import PixelObject
from game.util.vector2 import Vector2


class PixelPhysics(Physics):
    def __init__(self):
        super().__init__()
        self.mat: ndarray = None

    def apply_physics(self, obj: PhysicsObject, delta_t):
        if not isinstance(obj, PixelObject):
            raise Exception('Cannot apply pixelphysics to object that is not a pixelobject')

        xmn, xmx, ymn, ymx = obj.get_bounds()

        best = Vector2(0, 0)
        mn = 1e9
        off = 1e9

        edges = self.map.edges
        R = obj.collision_escape_radius
        self.mat = np.zeros(edges.shape, dtype=edges.dtype)
        if self.mat is None or self.mat.shape != edges.shape:
            self.mat = np.zeros(edges.shape, dtype=edges.dtype)
        else:
            cv2.rectangle(self.mat, (ymn - R, xmn - R), (ymx + R + 1, xmx + R + 1), 0, cv2.FILLED)

        obj.draw_hitbox(self.mat)

        for x in range(-R, R + 1):
            if xmx + x > edges.shape[1]:
                break
            for y in range(-R, R + 1):
                if ymx + y > edges.shape[0]:
                    break

                rect = cv2.bitwise_and(self.mat[ymn + y:ymx + y, xmn + x:xmx + x],
                                       edges[ymn + y:ymx + y, xmn + x:xmx + x])

                cnt = cv2.countNonZero(rect)
                if cnt < mn or (cnt == mn and x * x + y * y < off):
                    off = x * x + y * y
                    mn = cnt
                    best = Vector2(x, y)

        obj.collision_escape_vector = best

        if best.sq_mag() == 0:
            return

        if obj.collision_type == COLLISION_BOUNCE:
            obj.translate(best)
            vel = obj.vel
            obj.vel = vel - best.proj(vel) * 2.0
        elif obj.collision_type == COLLISION_SLIDE:
            obj.translate(best)
            obj.vel = best.perp_vector().proj(obj.vel)
        elif obj.collision_type == COLLISION_STICK:
            obj.translate(best)
            obj.vel.x = obj.vel.y = 0
