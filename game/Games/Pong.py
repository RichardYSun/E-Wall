import cv2
import numpy as np

from game.framework import Game, CVMap
from game.physics2.collisiontypes import COLLISION_BOUNCE
from game.physics2.objects.circle import Circle
from game.physics2.pixelphysics import PixelPhysics
from game.test import test
from game.util.Vector2 import Vector2

G = 1
ppm = 50


class Pong(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.ball = Circle(Vector2(mp.width / 2, mp.height / 2), 20)
        self.ball.collision_type = COLLISION_BOUNCE
        self.ball.vel = Vector2(200, 200)
        self.physics = PixelPhysics()
        self.physics.objects.append(self.ball)
        self.score = (0, 0)

    def update_map(self, new_map: CVMap):
        super().update_map(new_map)
        self.physics.update_map(new_map)

    def update_game(self, keys, delta_t: int):
        # bounce off top and bottom
        xmn, xmx, ymn, ymx = self.ball.get_bounds()
        if ymn < 0:
            self.ball.translate(Vector2(0, -ymn + 1))
            self.ball.vel.y *= -1
        if ymn >= self.map.height:
            self.ball.translate(Vector2(self.map.height - ymx - 1, 0))
            self.ball.vel.y *= -1
        if xmn < 0:
            self.ball.pos.x = self.map.width / 2
            self.ball.vel = Vector2(200, 200)
            self.score = (self.score[0] + 1, self.score[1])
        if xmx > self.map.width:
            self.ball.pos.x = self.map.width / 2
            self.ball.vel = Vector2(200, 200)
            self.score = (self.score[0], self.score[1] + 1)

        self.physics.update(delta_t)

        for obj in self.physics.objects:
            obj.translate(obj.vel * delta_t)

        self.ball.draw_hitbox(self.map.game_img)

        self.draw_score()

    def draw_score(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        pos = (self.map.height // 2, 200)
        colour = (0, 255, 0)
        fontScale = 2
        thickness = 2

        cv2.putText(self.map.game_img, str(self.score[0]) + " " + str(self.score[1]), pos, font, fontScale, colour,
                    thickness, cv2.LINE_AA)


test(Pong, None)
