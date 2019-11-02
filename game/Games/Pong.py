import cv2
import numpy as np

from game.framework import Game, CVMap
from game.physics2.WallPhysics import WallPhysics
from game.physics2.bouncephysics import BouncePhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.Rectangle import Rectangle
from game.physics2.PixelPhysics import PixelPhysics
from game.test import test
from game.util.Vector2 import Vector2

G = 1
ppm = 50


class PongBall(Circle):
    def on_collision(self, offset: Vector2):
        self.x += offset.x
        self.y += offset.y
        vel = Vector2(self.vx, self.vy)
        projed = offset.proj(vel)
        vel = vel - projed * 2.0
        self.vx = vel.x
        self.vy = vel.y


class Pong(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.ball = PongBall(mp.width / 2, mp.height / 2, 20)
        self.ball.vx = 200
        self.ball.vy = -200
        self.physics = BouncePhysics()
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
            self.ball.vy *= -1
        if ymn >= self.map.height:
            self.ball.translate(Vector2(self.map.height - ymx - 1, 0))
            self.ball.vy *= -1
        if xmn < 0:
            self.ball.x = self.map.width / 2
            self.ball.vx = 200
            self.ball.vy = -200
            self.score = (self.score[0] + 1, self.score[1])
        if xmx > self.map.width:
            self.ball.x = self.map.width / 2
            self.ball.vx = -200
            self.ball.vy = -200
            self.score = (self.score[0], self.score[1] + 1)

        self.physics.update(delta_t)

        for obj in self.physics.objects:
            obj.translate(Vector2(obj.vx * delta_t, obj.vy * delta_t))

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
