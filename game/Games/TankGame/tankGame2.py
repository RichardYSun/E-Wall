from game import keys
from game.Games.TankGame.bullet import Bullet
from game.Games.TankGame.tank import Tank
from game.game import Game, GameContext
from game.physics2.objects.circle import Circle
from game.physics2.objects.rectangle import Rectangle
from game.physics2.pixelphysics import PixelPhysics
from game.physics2.standardphysics import StandardPhysics
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.util.line import Line
from game.util.vector2 import Vector2
import math
import cv2

BulletSpeed = 100
BulletCooldown = 30

class TankGame2(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)

        self.std_physics = StandardPhysics(gravity=None)
        self.pixel_physics = PixelPhysics()
        self.wall_physics = WallPhysics()

        self.spawn1 = Vector2(mp.width / 4, mp.height / 2)
        self.spawn2 = Vector2(mp.width * 3 / 4, mp.height / 2)

        self.players = []*2
        self.bullets = []

        self.players.append(Tank(Rectangle(self.spawn1, 20, 20)))
        self.players.append(Tank(Rectangle(self.spawn2, 20, 20)))

        bulletSpawn = Vector2(self.players[0].hitBox.pos.x, self.players[0].hitBox.pos.y)
        bullet = Bullet(Circle(bulletSpawn, 8), BulletSpeed, self.players[0].angle)
        self.bullets.append(bullet)
        self.std_physics.objects.append(bullet.hitBox)
        self.pixel_physics.objects.append(bullet.hitBox)
        self.wall_physics.objects.append(bullet.hitBox)

        for tank in self.players:
            self.std_physics.objects.append(tank.hitBox)
            self.pixel_physics.objects.append(tank.hitBox)
            self.wall_physics.objects.append(tank.hitBox)

        self.bulletCooldowns = [0, 0]

        self.up1 = False;
        self.left1 = False;
        self.down1 = False;
        self.right1 = False;
        self.up2 = False;
        self.left2 = False;
        self.down2 = False;
        self.right2 = False;

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)

        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)
        self.std_physics.update_map(new_map)

    def update_game(self, keys_down, delta_t: int):
        # make sure to call update for all physics the game is using
        self.pixel_physics.update(delta_t)
        self.wall_physics.update(delta_t)
        self.std_physics.update(delta_t)

        self.checkShot()
        self.checkKeys()

        for tank in self.players:
            tank.hitBox.draw_hitbox(self.map.game_img)
            cv2.line(self.map.game_img, (int(tank.hitBox.pos.x), int(tank.hitBox.pos.y)), (int(tank.hitBox.pos.x + 12*math.cos(tank.angle)),
                        int(tank.hitBox.pos.y + 12*math.sin(tank.angle))), (69,42,210), 4)

        for bullet in self.bullets:
            bullet.timer -= 1

            if bullet.timer < 0:
                bullet.alive = False
                continue

            bullet.hitBox.draw_hitbox(self.map.game_img)

        for i in range(len(self.bullets), 0):
            if not self.bullets[i].alive:
                self.remove(self.bullets[i])

        for cooldown in self.bulletCooldowns:
            cooldown += 1

    def checkShot(self):
        for tank in self.players:
            for bullet in self.bullets:
                if tank.hitBox.circle_collision(bullet.hitBox):
                    tank.alive = False
                    bullet.alive = False
                    self.remove(bullet)
                    self.remove(tank)

    def remove(self, obj):
        self.std_physics.objects.remove(obj)
        self.pixel_physics.objects.remove(obj)
        self.wall_physics.objects.remove(obj)

    def checkKeys(self):
        if self.right1:
            self.players[0].angle += self.players[0].turnSpeed
            self.players[0].rotateLeft()
        if self.left1:
            self.players[0].angle -= self.players[0].turnSpeed
            self.players[0].rotateRight()

        if self.up1:
            self.players[0].setSpeed(1)
        elif self.down1:
            self.players[0].setSpeed(-1)
        else:
            self.players[0].setSpeed(0)

    def key_down(self, key_down: int):
        if key_down == keys.RIGHT:
            self.right1 = True
        if key_down == keys.LEFT:
            self.left1 = True

        if key_down == keys.UP:
            self.up1 = True
        elif key_down == keys.DOWN:
            self.down1 = True

        # ATM, only player 1 controls implemented, so set the "enter" key for player 1
        if key_down == keys.ENTER:
           if self.bulletCooldowns[0] >= BulletCooldown:
                bulletSpawn = Vector2(self.players[0].hitBox.pos.x, self.players[0].hitBox.pos.y)
                bullet = Bullet(Circle(bulletSpawn, 8), BulletSpeed, self.players[0].angle)
                self.bullets.append(bullet)
                self.std_physics.objects.append(bullet.hitBox)
                self.pixel_physics.objects.append(bullet.hitBox)
                self.wall_physics.objects.append(bullet.hitBox)

                self.bulletCooldowns[0] = 0

    def key_up(self, key_up: int):
        if key_up == keys.RIGHT:
            self.right1 = False
        if key_up == keys.LEFT:
            self.left1 = False

        if key_up == keys.UP:
            self.up1 = False
        elif key_up == keys.DOWN:
            self.down1 = False
test(TankGame2, None)
