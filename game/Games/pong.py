import cv2
import numpy as np

from game.game import Game, CVMap
from game.physics2.collisiontypes import COLLISION_BOUNCE
from game.physics2.objects.circle import Circle
from game.physics2.pixelphysics import PixelPhysics
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.util.vector2 import Vector2

G = 1
ppm = 50


class Pong(Game):

    def __init__(self, mp: CVMap):
        super().__init__(mp)  # make sure to call superclass initializer

        # we will use two physics in this game
        self.pixel_physics = PixelPhysics()  # PixelPhysics handles collisions of the camera image with the game objects
        self.wall_physics = WallPhysics()  # WallPhysics makes the objects bounce off walls
        # since this is pong, we want to disable the left and right walls
        self.wall_physics.left=False
        self.wall_physics.right=False

        # we create the ball
        # Vector2(mp.width / 2, mp.height / 2) means the ball is in the center of the screen
        # 20 is the radius
        self.ball = Circle(Vector2(mp.width / 2, mp.height / 2), 20)
        self.ball.collision_type = COLLISION_BOUNCE  # this makes the ball bouncy
        self.ball.vel = Vector2(200, 200)  # make the ball begin moving
        self.pixel_physics.objects.append(self.ball)  # apply pixel physics to ball
        self.wall_physics.objects.append(self.ball)  # apply wall physics to ball

        self.score = (0, 0)

    # this is called when there is a new frame available from camera
    def update_map(self, new_map: CVMap):
        super().update_map(new_map)  # make sure to call super

        # make sure to call update_map for all the physics you're using
        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)

    def update_game(self, keys, delta_t: int):
        # bounce off top and bottom
        xmn, xmx, ymn, ymx = self.ball.get_bounds()
        if xmn < 0:
            self.ball.pos.x = self.map.width / 2
            self.ball.vel = Vector2(200, 200)
            self.score = (self.score[0] + 1, self.score[1])
        if xmx > self.map.width:
            self.ball.pos.x = self.map.width / 2
            self.ball.vel = Vector2(200, 200)
            self.score = (self.score[0], self.score[1] + 1)

        # make sure to call update for all physics the game is using
        self.pixel_physics.update(delta_t)
        self.wall_physics.update(delta_t)

        for obj in self.pixel_physics.objects:
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
