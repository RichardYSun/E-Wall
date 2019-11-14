import math
from math import atan2
from typing import List

from game import keys
from game.physics2 import collisiontypes
from game.physics2.objects.pixelobject import PixelObject
from numpy import ndarray
import cv2
import numpy as np

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
    walk_speed = 35

    def __init__(self, pos):
        super().__init__(pos)
        self.rest_left = cv2.flip(self.rest_right, 1)
        self.walk_right = [self.rest_right, self.walk1_right, self.rest_right, self.walk2_right]
        self.walk_left = [cv2.flip(x, 1) for x in self.walk_right]
        self.walk_state = 0
        self.walk_time = 0
        self.cur_img = self.rest_right
        self.state = FALLING
        self.collision_type = collisiontypes.COLLISION_STICK

    def update(self, delta_t: float, down: List[bool]):
        v = self.collision_escape_vector
        prev_state = self.state
        if self.touching_bottom:
            self.state=GROUNDED
        else:
            if v.sq_mag() == 0:
                if self.vel.y > 0:
                    self.state = FALLING
                else:
                    self.state = JUMPED
            else:
                ang = atan2(v.x, v.y)
                self.state = GROUNDED

        if prev_state == GROUNDED and self.state!=GROUNDED:
            self.vel.x = 0
            self.walk_state = 0
            self.walk_time = 0
            self.cur_img = self.walk_left[self.walk_state]
        if self.state == GROUNDED:
            if prev_state != GROUNDED:
                self.vel.x = 0
                self.walk_state = 1
                self.walk_time = self.walk_rate

            if down[keys.LEFT]:
                self.vel.x = -self.walk_speed
                self.update_walk(delta_t)
                self.cur_img = self.walk_left[self.walk_state]
            elif down[keys.RIGHT]:
                self.vel.x = self.walk_speed
                self.update_walk(delta_t)
                self.cur_img = self.walk_right[self.walk_state]
            else:  # reset walking
                self.vel.x = 0
                self.walk_state = 0
                self.walk_time = 0
                self.cur_img = self.walk_left[self.walk_state]
        else:
            pass

    def update_walk(self, delta_t: float):
        self.walk_time += delta_t
        if self.walk_time >= self.walk_rate * 4:
            self.walk_time = 0
        self.walk_state = int(self.walk_time / self.walk_rate)

    def draw(self, game_img: ndarray):
        x, y = self.pos.as_int_tuple()
        c = self.cur_img
        c = c[:, :, :3]
        game_img[y:y + c.shape[0], x:x + c.shape[1]] = c

    def draw_hitbox(self, img: ndarray):
        x, y = self.pos.as_int_tuple()
        c = self.cur_img
        c = cv2.extractChannel(c, 3)  # extract alpha channel
        img[y:y + c.shape[0], x:x + c.shape[1]] = c

    def get_bounds(self):
        x, y = self.pos.as_int_tuple()
        s = self.cur_img.shape
        return x, x + s[1], y, y + s[0]