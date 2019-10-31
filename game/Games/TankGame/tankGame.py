import cv2
import math
import imutils
import keys as key
from Games.TankGame.tank import Tank
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
            self.tanks[0].rotateRight(TurnSpeed)
        if keys[key.LEFT]:
            self.tanks[0].angle += TurnSpeed
            self.tanks[0].rotateLeft(TurnSpeed)
        if keys[key.DOWN]:
            self.tanks[0].speed = -PlayerSpeed
        if keys[key.UP]:
            self.tanks[0].speed = PlayerSpeed

    def movePieces(self):
        self.deadTanks()

        for tank in self.tanks:
            if tank.alive:
                tank.px += tank.speed * math.cos(tank.angle)
                tank.py += tank.speed * math.sin(tank.angle)

    def drawPieces(self, game_img: ndarray):
        for tank in self.tanks:
            tank.draw(game_img)
        for bullet in self.bullets:
            bullet.draw(game_img)

    def deadTanks(self):
        for tank in self.tanks:
            for bullet in self.bullets:
                if tank.contains(bullet):
                    tank.alive = False
                    bullet.alive = False
        if not self.tanks[0].alive:
            self.gameOver(0)
        elif not self.tanks[1].alive:
            self.gameOver(1)

    def gameOver(self, loser : int):
        pass