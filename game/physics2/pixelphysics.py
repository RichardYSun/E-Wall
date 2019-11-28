from typing import Tuple

import cv2
import numpy as np
from numpy.core.multiarray import ndarray

from game.game import GameContext
from game.physics2.collisiontypes import COLLISION_STICK, COLLISION_SLIDE, COLLISION_BOUNCE
from game.physics2.physics import Physics
from game.physics2.objects.physicsobject import PhysicsObject
from game.physics2.objects.pixelobject import PixelObject
from game.util.vector2 import Vector2

Rect = Tuple[int, int, int, int]


def inter(a: Rect, b: Rect) -> Rect:
    return max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3])


def area(a: Rect) -> int:
    return (a[1] - a[0]) * (a[3] - a[2])


def check_pixel_collision(a: PixelObject, b: PixelObject) -> int:
    b_bounds = b.get_bounds()
    a_bounds = a.get_bounds()
    s = inter(a_bounds, b_bounds)

    if empty(s):
        return 0

    # if both rect, just use area
    if a.is_rect and b.is_rect:
        return area(s)

    if b.is_rect:  # swap so a is rect only
        a, b = b, a

    # one is image
    xmn, xmx, ymn, ymx = b_bounds
    b_hit = b.get_hitbox()
    b_sub = b_hit[s[2] - ymn:s[3] - ymn, s[0] - xmn:s[1] - xmn]
    if a.is_rect:  # select b rect from a rect
        if b.use_direct_img:
            return cv2.countNonZero(b_sub)
        raise Exception('unsupported hitbox type: use_direct_img=false')
    # both images, binary and
    if a.use_direct_img:
        xmn, xmx, ymn, ymx = a_bounds
        a_hit=a.get_hitbox()
        a_sub = a_hit[s[2] - ymn:s[3] - ymn, s[0] - xmn:s[1] - xmn]
        return cv2.countNonZero(cv2.bitwise_and(a_sub, b_sub))

    raise Exception('unsupported hitbox type: use_direct_img=false')


def empty(s: Rect) -> bool:
    return s[3] <= s[2] or s[1] <= s[0]


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

        hitbox = None

        if not obj.is_rect:
            if obj.use_direct_img:
                hitbox = obj.get_hitbox()
                # print(obj.get_bounds())
            else:
                if self.mat is None or self.mat.shape != edges.shape:
                    self.mat = np.zeros(edges.shape, dtype=edges.dtype)
                else:
                    cv2.rectangle(self.mat, (ymn - R, xmn - R), (ymx + R + 1, xmx + R + 1), 0, cv2.FILLED)
                obj.draw_hitbox(self.mat)

        screen_rect = (0, edges.shape[1], 0, edges.shape[0])

        for x in range(-R, R + 1):
            for y in range(-R, R + 1):
                test_rect = (xmn + x, xmx + x, ymn + y, ymx + y)
                s = inter(test_rect, screen_rect)
                if empty(s):
                    continue
                # print(s)
                img = edges[s[2]:s[3], s[0]:s[1]]

                if not obj.is_rect:
                    if obj.use_direct_img:
                        a = hitbox[s[2] - ymn - y:s[3] - ymn - y, s[0] - xmn - x:s[1] - xmn - x]
                        img = cv2.bitwise_and(a, img)
                    else:
                        img = cv2.bitwise_and(self.mat[s[2]:s[3], s[0]:s[1]], img)

                cnt = cv2.countNonZero(img)

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
            mag = vel.mag()
            vel = vel - best.proj(vel) * 2.0
            obj.vel = vel * mag / vel.mag()
        elif obj.collision_type == COLLISION_SLIDE:
            obj.translate(best)
            obj.vel = best.perp_vector().proj(obj.vel)
        elif obj.collision_type == COLLISION_STICK:
            obj.translate(best)
            obj.vel.x = obj.vel.y = 0
