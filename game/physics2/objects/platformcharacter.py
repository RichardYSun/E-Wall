import math
from math import atan2
from typing import List

from game import keys
from game.physics2 import collisiontypes
from game.physics2.objects.pixelobject import PixelObject
from numpy import ndarray
import cv2

GROUNDED = 1
FALLING = 2
JUMPED = 3


class PlatformCharacter(PixelObject):
    rest_right: ndarray
    walk1_right: ndarray
    walk2_right: ndarray
    cur_img: ndarray
    walk_rate = 0.25
    flat_normal = math.pi / 6
    walk_speed = 1

    def __init__(self, pos):
        super().__init__(pos)
        self.rest_left = cv2.flip(self.rest_right, 1)
        self.walk1_left = cv2.flip(self.walk1_right, 1)
        self.walk2_left = cv2.flip(self.walk2_right, 1)
        self.walk_state = 0
        self.walk_time = 0
        self.cur_img = self.rest_right
        self.state = FALLING
        self.collision_type = collisiontypes.COLLISION_STICK

    def update(self, delta_t: float, down: List[bool]):
        v = self.collision_escape_vector
        prev_state = self.state
        if v.sq_mag() == 0:
            if self.vel.y > 0:
                self.state = FALLING
            else:
                self.state = JUMPED
        else:
            ang = atan2(v.x, v.y)
            self.state = GROUNDED

        if self.state == GROUNDED:
            if down[keys.LEFT]:
                self.vx = -self.walk_speed
            elif down[keys.RIGHT]:
                self.vx = self.walk_speed
            else:
                self.vx = 0
                self.walk_state = 0
                self.walk_time = 0



        else:
            pass

    def draw(self, game_img: ndarray):
        p = self.pos
        c = self.cur_img
        game_img[p.x:p.x + c.shape[0], p.y:p.y + c.shape[0]] = c

    def draw_hitbox(self, img: ndarray):
        p = self.pos
        c = self.cur_img
        c = cv2.extractChannel(c, 3)  # extract alpha channel
        img[p.x:p.x + c.shape[0], p.y:p.y + c.shape[0]] = c

    def get_bounds(self):
        p = self.pos
        s = self.cur_img.shape
        return p.x, p.x + s[0], p.y, p.y + s[1]
