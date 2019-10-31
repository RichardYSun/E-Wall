import cv2
import math
import keys as key
from framework import Game, CVMap

TurnSpeed = 0.1
PlayerSpeed = 0.1


class TankGame(Game):
    tanks = []

    def __init__(self):
        self.tanks.append(Tank(100, 100, 0, 0))

    def update_game(self, keys, delta_t: int):
        self.takeInput(keys)
        self.movePieces()
        return self.map.edges

    def update_map(self, new_map: CVMap):
        pass

    def takeInput(self, keys: [bool]):
        if keys[key.RIGHT]:
            self.tanks[0].angle -= TurnSpeed
        if keys[key.LEFT]:
            self.tanks[0].angle += TurnSpeed
        if keys[key.DOWN]:
            self.tanks[0].speed = -PlayerSpeed
        if keys[key.UP]:
            self.tanks[0].speed = PlayerSpeed

    def movePieces(self):
        for tank in self.tanks:
            tank.px += tank.speed * math.cos(tank.angle)
            tank.py += tank.speed * math.sin(tank.angle)


class Tank:
    px, py = 0.0
    angle = 0.0  # radians
    speed = 0.0

    def __init__(self, px, py, speed, angle):
        self.px = px
        self.py = py
        self.angle = angle
        self.speed = speed
