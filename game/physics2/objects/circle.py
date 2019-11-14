import cv2
import pygame

from game.physics2.objects.physicsobject import PhysicsObject
from numpy import ndarray

from game.physics2.objects.pixelobject import PixelObject
from game.util.vector2 import Vector2


class Circle(PixelObject):
    colour = (0, 0, 255)
    obj_type = 1

    def __init__(self, pos: Vector2, r):
        super().__init__(pos)
        self.r = r

    # def draw_hitbox(self, img: ndarray):
    #     cv2.circle(img, self.pos.as_int_tuple(), self.r, 255, cv2.FILLED)

    def draw_hitbox(self, surface):
        pygame.draw.circle(surface, self.colour, self.pos.as_int_tuple(), self.r, 0)

    def get_bounds(self):
        x, y = self.pos.as_int_tuple()
        r = self.r
        return x - r, x + r, y - r, y + r
