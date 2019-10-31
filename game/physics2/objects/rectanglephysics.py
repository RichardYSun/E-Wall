from typing import List

from game.physics2.Physics import MapPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util.Vector2 import Vector2


class RectanglePhysics(MapPhysics):

    def apply_physics(self, obj: PhysicsObject, delta_t):
        lines = self.map.lines_conv

        cnt = 0

        for i in lines:
            if obj.inter(i):
                dist = obj.distance(i)
                for j in range(4):
                    obj.pts[j] -= dist

                cnt += 1

        if cnt:
            obj.vx = obj.vy = 0

        for i in lines:
            if obj.inter(i):
                close = obj.closest(i)
                obj.va[close] = 0
