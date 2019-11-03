import math

import cv2
import numpy as ndarray
import imutils
from physics2.objects.circle import Circle
from physics2.collisiontypes import COLLISION_BOUNCE
from physics2.objects.rectangle import Rectangle
from util.vector2 import Vector2


class Bullet:
    alive = True
    hitBox: Circle
    timer = 200

    def __init__(self, hitBox: Circle, speed, angle):
        self.hitBox = hitBox
        self.hitBox.collision_type = COLLISION_BOUNCE
        self.hitBox.vel = Vector2(speed * math.cos(angle), speed*math.sin(angle))