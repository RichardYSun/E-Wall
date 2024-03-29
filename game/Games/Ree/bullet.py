import math

import cv2
import pygame
from numpy.core.multiarray import ndarray

from game.game import GameContext
from game.img.images import imread, load_py_img
from game.physics2.objects.pixelobject import PixelObject
from game.physics2.pixelphysics import check_pixel_collision
from game.util.vector2 import Vector2
import imutils


class Bullet(PixelObject):
    def __init__(self,
                 mp: GameContext,
                 pos: Vector2,
                 img: str,
                 damage: float,
                 vel: Vector2,
                 src,
                 size=None
                 ):
        pos = Vector2(pos.x, pos.y)
        super().__init__(pos)
        self.use_direct_img = True
        self.vel = vel
        self.damage = damage
        self.death_flag = False
        self.src = src

        cv_img = imread('ree/bullet/' + img, cv2.IMREAD_UNCHANGED)
        if size is None:
            size = cv_img.shape[1], cv_img.shape[0]
        else:
            cv_img = cv2.resize(cv_img, size)

        ang = math.atan2(vel.x, vel.y)
        cv_img = cv2.extractChannel(cv_img, 3)
        self.cv_img = imutils.rotate_bound(cv_img, ang)
        # ignore resizing of window cause ppl won't notice anyways
        p = mp.conv_img(load_py_img('ree/bullet/' + img).convert_alpha(), size)
        self.py_img = pygame.transform.rotate(p, ang * 180 / math.pi + 90)
        self.just_spawned = 0.5

    def get_hitbox(self):
        return self.cv_img

    def draw(self, mp: GameContext):
        mp.image_py(self.py_img, self.pos)

    def update(self, delta_t: float):
        self.pos += self.vel * delta_t
        if self.touching_wall:
            self.death_flag = True

        if check_pixel_collision(self, self.src) == 0:
            self.just_spawned = 0

        if self.just_spawned <= 0 and self.collision_escape_vector is not None:
            if self.collision_escape_vector.sq_mag() > 0:
                self.death_flag = True


class Living(PixelObject):
    def __init__(self, max_health: float, pos):
        super().__init__(pos)
        self.health = max_health
        self.max_health = max_health

    def damage(self, damage: float):
        self.health = max(-1,self.health-damage)

    def die(self):
        pass
