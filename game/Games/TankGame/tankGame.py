import cv2
import math
import imutils
import keys as key
from framework import Game, CVMap
import cv2.ndarray as ndarray

TurnSpeed = 0.1
PlayerSpeed = 0.1


class TankGame(Game):
    tanks = []
    bullets = []

    def __init__(self):
        self.tanks.append(Tank(100, 100, 0, 0))

    def update_game(self, keys, delta_t: int):
        self.takeInput(keys)
        self.movePieces()
        self.drawPeices(self.map.game_img)
        return self.map.edges

    def update_map(self, new_map: CVMap):
        pass

    def takeInput(self, keys: [bool]):
        if keys[key.RIGHT]:
            self.tanks[0].angle -= TurnSpeed
            self.tanks[0].rotateRight()
        if keys[key.LEFT]:
            self.tanks[0].angle += TurnSpeed
            self.tanks[0].rotateLeft()
        if keys[key.DOWN]:
            self.tanks[0].speed = -PlayerSpeed
        if keys[key.UP]:
            self.tanks[0].speed = PlayerSpeed

    def movePieces(self):
        for tank in self.tanks:
            tank.px += tank.speed * math.cos(tank.angle)
            tank.py += tank.speed * math.sin(tank.angle)

    def drawPieces(self, game_img: ndarray):
        for tank in self.tanks:
            tank.draw(game_img)
        for bullet in self.bullets:
            bullet.draw(game_img)


class Tank:
    px, py = 0.0
    angle = 0.0  # radians
    speed = 0.0
    sprite: cv2.ndarray

    def __init__(self, px, py, speed, angle, type: int):
        self.px = px
        self.py = py
        self.angle = angle
        self.speed = speed
        if type == 1:
            sprite = cv2.imread('player.jpg')
        elif type == 2:
            sprite = cv2.imread('blue.jpg')
        elif type == 3:
            sprite = cv2.imread('red.jpg')

    def rotateRight(self):
        self.sprite = imutils.rotate_bound(self.image, -TurnSpeed)

    def rotateLeft(self):
        self.sprite = imutils.rotate_bound(self.image, TurnSpeed)

    def draw(self, game_img: ndarray):
        game_img[self.px: self.px + self.sprite.shape[0], self.py: self.py + self.sprite.shape[1]] = self.sprite
