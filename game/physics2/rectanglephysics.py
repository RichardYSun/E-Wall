import math
from typing import List

import cv2
import numpy as np

from game.physics2.Physics import MapPhysics
from game.physics2.objects.PhysicsObject import PhysicsObject
from game.util.Vector2 import Vector2

R = 10


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

        xmx += 1
        ymx += 1

        obj_edges = obj.edges()

        best = Vector2(0, 0)
        mn = 1e9
        off = 1e9

        mat = np.zeros(edges.shape, dtype=edges.dtype)
        pts = np.array((
            (obj.pts[0].x, obj.pts[0].y),
            (obj.pts[1].x, obj.pts[1].y),
            (obj.pts[2].x, obj.pts[2].y),
            (obj.pts[3].x, obj.pts[3].y)
        ), dtype=int)
        cv2.fillConvexPoly(mat, pts, 255)

        for x in range(-R, R + 1):
            if xmx + x > edges.shape[1]:
                break;
            for y in range(-R, R + 1):
                if ymx + y > edges.shape[0]:
                    break;

                rect = cv2.bitwise_and(mat[ymn + y:ymx + y, xmn + x:xmx + x], edges[ymn + y:ymx + y, xmn + x:xmx + x])

                cnt = cv2.countNonZero(rect)
                if cnt < mn or (cnt == mn and abs(x) + abs(y) < off):
                    off = abs(x) + abs(y)
                    mn = cnt
                    best = Vector2(x, y)

        for i in range(4):
            obj.pts[i] += best

        # inter=cv2.findNonZero(edges[])

        if off != 0:
            obj.vx = obj.vy = 0

        # if off != 0:
        #     print(best.__str__())

        # disp = Vector2(0, 0);

        # for x in range(xmn, min(xmx + 1, edges.shape[1])):
        #     for y in range(ymn, min(ymx + 1, edges.shape[0])):
        #         pt = Vector2(x, y)
        #         if edges[y, x] and obj.inside(pt):
        #             dist = Vector2(1e5, 1e5)
        #             for i in range(4):
        #                 dist = min(dist, obj_edges[i].distance(pt))
        #
        #             disp += dist
        #
        #             for i in range(4):
        #                 obj.pts[i] += dist
        #
        #             cnt += 1

        # for i in range(4):
        #     obj.pts[i] += disp

        # for x in range(xmn, min(xmx + 1, edges.shape[1])):
        #     for y in range(ymn, min(ymx + 1, edges.shape[0])):
        #         pt = Vector2(x, y)
        #         if edges[y, x] and obj.inside(pt):
        #             dist = Vector2(1e5, 1e5)
        #             for i in range(4):
        #                 dist = min(dist, obj_edges[i].distance(pt))
        #
        #             contact_pt = pt - dist

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
