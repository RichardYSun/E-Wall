import math

from game.physics2.collisiontypes import COLLISION_BOUNCE
from game.physics2.objects.circle import Circle
from game.util.vector2 import Vector2


class Bullet:
    alive = True
    hitBox: Circle
    timer = 200
    inside = True

    def __init__(self, hitBox: Circle, speed, angle):
        self.hitBox = hitBox
        self.hitBox.collision_type = COLLISION_BOUNCE
        self.hitBox.vel = Vector2(speed * math.cos(angle), speed*math.sin(angle))