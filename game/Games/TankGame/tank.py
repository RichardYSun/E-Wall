import math

import cv2
from numpy import ndarray

from game.physics2.collisiontypes import COLLISION_SLIDE
from game.physics2.objects.rectangle import Rectangle
from game.util.vector2 import Vector2

PlayerSpeed = 5.0
TurnSpeed = 0.1
class Tank:
    speed = 0.0
    angle = 0.0
    sprite: ndarray
    sprite_radius = 32
    alive = True
    hitBox : [Rectangle] = None

    def __init__(self, hitBox: Rectangle, type: int):
        self.hitBox = hitBox
        self.hitBox.collision_type = COLLISION_SLIDE
        self.angle = 0.0
        self.speed = 0.0
        self.hitBox.vel = Vector2(0,0)
        if type == 1:
            self.sprite = cv2.imread('player.jpg')
        elif type == 2:
            self.sprite = cv2.imread('blue.jpg')
        elif type == 3:
            self.sprite = cv2.imread('red.jpg')

    def setSpeed(self, speed :int):
        if speed == 0:
            self.hitBox.vel = Vector2(0,0)
        elif speed == 1:
            self.hitBox.vel = Vector2(PlayerSpeed * math.cos(self.angle), PlayerSpeed * math.sin(self.angle))
        elif speed == -1:
            self.hitBox.vel = Vector2(-PlayerSpeed * math.cos(self.angle), -PlayerSpeed * math.sin(self.angle))

    def rotateRight(self):
        self.hitBox.rotate(-TurnSpeed, Vector2(self.hitBox.x, self.hitBox.y))

    def rotateLeft(self):
        self.hitBox.rotate(TurnSpeed, Vector2(self.hitBox.x, self.hitBox.y))
