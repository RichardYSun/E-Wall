import math
from typing import List

from game.physics2.Physics import MapPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util.Vector2 import Vector2


class RectanglePhysics(MapPhysics):

    def apply_physics(self, obj: PhysicsObject, delta_t):
        edges = self.map.edges

        cnt = 0

        xmn = ymn = 1e9
        xmx = ymx = 0

        for i in range(4):
            xmn = min(xmn, int(obj.pts[i].x))
            xmx = max(xmx, int(obj.pts[i].x))
            ymn = min(ymn, int(obj.pts[i].y))
            ymx = max(ymx, int(obj.pts[i].y))

        obj_edges = obj.edges()

        for x in range(xmn, min(xmx + 1, edges.shape[1])):
            for y in range(ymn, min(ymx + 1, edges.shape[0])):
                pt = Vector2(x, y)
                if edges[y, x] and obj.inside(pt):
                    dist = Vector2(1e5, 1e5)
                    for i in range(4):
                        dist = min(dist, obj_edges[i].distance(pt))

                    for i in range(4):
                        obj.pts[i] += dist

                    cnt += 1

        if cnt != 0:
            obj.vx = obj.vy = 0

    # lines = self.map.lines_conv
    #
    # cnt = 0
    #
    # for i in lines:
    #     if obj.inter(i):
    #         dist = obj.distance(i)
    #         for j in range(4):
    #             obj.pts[j] -= dist
    #
    #         cnt += 1
    #
    # if cnt != 0:
    #     obj.vx = obj.vy = 0
