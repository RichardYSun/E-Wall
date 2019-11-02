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


class PongBall(Circle):
    def on_collision(self, offset: Vector2):
        self.x += offset.x
        self.y += offset.y
        vel = Vector2(self.vx, self.vy)
        if vel.sq_mag()==0:
            return
        projed = offset.proj(vel)
        vel = vel - projed * 2.0
        self.vx = vel.x
        self.vy = vel.y


class Pong(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)
        self.ball = PongBall(mp.width / 2, mp.height / 2, 20)
        self.ball.vx = 0
        self.ball.vy = -200
        self.physics = PixelPhysics()
        self.physics.objects.append(self.ball)

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

        self.physics.update(delta_t)

        for obj in self.physics.objects:
            obj.translate(Vector2(obj.vx * delta_t, obj.vy * delta_t))

        self.ball.draw_hitbox(self.map.game_img)


test(Pong, None)
