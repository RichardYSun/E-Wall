import cv2

from game import Game, GameContext
from game.physics2.collisiontypes import COLLISION_BOUNCE
from game.physics2.objects.Circle import Circle
from game.physics2.PixelPhysics import PixelPhysics
from game.physics2.standardphysics import StandardPhysics
from game.physics2.wallphysics import WallPhysics
from game.util.vector2 import Vector2
from game.util.line import Line

from Games.TankGame.bullet import Bullet
from Games.TankGame.tank import Tank
import keys as key

TurnSpeed = 0.1
PlayerSpeed = 5
BulletSpeed = 15
BulletCooldown = 30

class TankGame2(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)

        self.std_physics = StandardPhysics(gravity=None)
        self.pixel_physics = PixelPhysics()
        self.wall_physics = WallPhysics()

        self.spawn1 = Vector2(mp.width / 4, mp.height / 2)
        self.spawn2 = Vector2(mp.width * 3 / 4, mp.height / 2)

        self.players = []
        self.bullets = []

        self.players[0] = Tank(self.spawn1, 40, 40)
        self.players[1] = Tank(self.spawn2, 40, 40)

        for tank in self.players:
            self.std_physics.objects.append(tank)
            self.pixel_physics.objects.append(tank)
            self.wall_physics.objects.append(tank)

        self.bulletCooldowns = [0, 0]

    def update_map(self, new_map: GameContext):
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

        for cooldown in self.bulletCooldowns:
            cooldown += 1


    def checkShot(self):
        for tank in self.players:
            for bullet in self.bullets:
                if tank.hitBox.distance(Line(bullet.hitBox.x, bullet.hitBox.y, 1, 1)) < bullet.hitBox.r:
                    tank.alive = False
                    bullet.alive = False
                    self.remove(bullet)
                    self.remove(tank)

    def remove(self, obj):
        self.std_physics.objects.remove(obj);
        self.pixel_physics.objects.remove(obj);
        self.wall_physics.objects.remove(obj);

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

        # ATM, only player 1 controls implemented, so set the "enter" key for player 1
        if keys[key.ENTER]:
            if self.bulletCooldowns[0] >= BulletCooldown:
                bulletSpawn = Vector2(self.players[0].hitBox.pts[1].x, self.players[0].hitBox.pts[1].y)
                bullet = Bullet(Circle(bulletSpawn, 3), BulletSpeed, self.players[0].angle)

                self.std_physics.objects.append(bullet)
                self.pixel_physics.objects.append(bullet)
                self.wall_physics.objects.append(bullet)

                self.bulletCooldowns[0] = 0
