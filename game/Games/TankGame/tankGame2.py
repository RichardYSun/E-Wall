import cv2

from game import Game, GameContext
from physics2.collisiontypes import COLLISION_BOUNCE
from physics2.objects.Circle import Circle
from physics2.PixelPhysics import PixelPhysics
from physics2.standardphysics import StandardPhysics
from physics2.wallphysics import WallPhysics
from test import test
from util.vector2 import Vector2
from util.line import Line

from Games.TankGame.bullet import Bullet
from Games.TankGame.tank import Tank
import keys as key


TurnSpeed = 0.1
PlayerSpeed = 5

class TankGame2(Game):

    def __init__(self, mp : GameContext):
        super().__init__(mp)

        self.std_physics = StandardPhysics(gravity = None)
        self.pixel_physics = PixelPhysics()
        self.wall_physics = WallPhysics()

        self.spawn1 = Vector2(mp.width / 4, mp.height /2)
        self.spawn2 = Vector2(mp.width * 3/4, mp.height/2)

        self.players = []
        self.bullets = []

        self.players[0] = Tank(self.spawn1, 40, 40)
        self.players[1] = Tank(self.spawn2, 40, 40)

        for tank in self.players:
            self.std_physics.objects.append(tank)
            self.pixel_physics.objects.append(tank)
            self.wall_physics.objects.append(tank)

    def update_map(self, new_map : GameContext):
        super().update_map(new_map)

        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)
        self.std_physics.update_map(new_map)

    def update_game(self, keys, delta_t: int):
        # make sure to call update for all physics the game is using
        self.pixel_physics.update(delta_t)
        self.wall_physics.update(delta_t)
        self.std_physics.update(delta_t)

        self.checkShot()
        self.takeInput(keys)

        for tank in self.players:
            tank.hitBox.draw_hitbox(self.map.game_img)

        for bullet in self.bullets:
            bullet.hitBox.draw_hitbox(self.map.game_img)

    def checkShot(self):
        for tank in self.players:
            for bullet in self.bullets:
                if tank.hitBox.distance(Line(bullet.hitBox.x, bullet.hitBox.y,1,1)) < bullet.hitBox.r:
                    tank.alive = False
                    bullet.alive = False
                    self.remove(bullet)
                    self.remove(tank)

    def remove(self, obj):
        pass

    def takeInput(self, keys: [bool]):
        if keys[key.RIGHT]:
            self.players[0].angle -= TurnSpeed
            self.players[0].rotateRight()
        if keys[key.LEFT]:
            self.players[0].angle += TurnSpeed
            self.players[0].rotateLeft()

        if keys[key.UP]:
            self.players[0].setSpeed(1)
        elif keys[key.DOWN]:
            self.players[0].setSpeed(-1)
        else:
            self.players[0].setSpeed(0)


