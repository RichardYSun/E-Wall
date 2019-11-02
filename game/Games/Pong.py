import cv2

from game.framework import Game, CVMap
from game.physics2.WallPhysics import WallPhysics
from game.physics2.objects.Circle import Circle
from game.physics2.objects.Rectangle import Rectangle
from game.physics2.PixelPhysics import PixelPhysics
from game.test import test
from game.util.Vector2 import Vector2

G = 1
ppm = 50

#class PongBall(Circle):


class Pong(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.ball = PongBall(mp.width / 2, mp.height / 2, 20)
        self.ball.vx = 100
        self.ball.vy = 100
        self.physics = PixelPhysics()
        self.physics.objects.append(self.ball)

    def update_map(self, new_map: CVMap):
        super().update_map(new_map)
        self.physics.update_map(new_map)

    def update_game(self, keys, delta_t: int):

        # self.wall.update(delta_t)
        self.physics.update(delta_t)

        for obj in self.physics.objects:
            obj.translate(Vector2(obj.vx * delta_t, obj.vy * delta_t))

        self.ball.draw_hitbox(self.map.game_img)


test(Pong, )
