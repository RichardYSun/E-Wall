from typing import Tuple

import pygame

from game import keys
from game.Games.TankGame.bullet import Bullet
from game.Games.TankGame.tank import Tank
from game.font.fonts import load_font
from game.game import Game, GameContext
from game.physics2.objects.circle import Circle
from game.physics2.objects.rectangle import Rectangle
from game.physics2.pixelphysics import PixelPhysics
from game.physics2.standardphysics import StandardPhysics
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.img.images import load_py_img
from game.util.vector2 import Vector2
import math

BulletSpeed = 100
BulletSize = 8
TankSize = 20
BulletCooldown = 1


class TankGame2(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)

        self.std_physics = StandardPhysics(gravity=None)
        self.pixel_physics = PixelPhysics()
        self.wall_physics = WallPhysics()

        self.spawn1 = Vector2(mp.width / 4, mp.height / 2)
        self.spawn2 = Vector2(mp.width * 3 / 4, mp.height / 2)

        self.blueTankImg: pygame.Surface = None
        self.greenTankImg: pygame.Surface = None
        self.bulletImg: pygame.Surface = None
        self.winnerImg: pygame.Surface = None

        self.up1 = False;
        self.left1 = False;
        self.down1 = False;
        self.right1 = False;
        self.up2 = False;
        self.left2 = False;
        self.down2 = False;
        self.right2 = False;

        self.restartButton = False;

        self.won = 0

        self.players = []*2
        self.bullets = []

        self.initialize_objects()
        self.initialize_buttons()

        self.font : pygame.font.Font = None
        self.textColor = (200,255,200)

    def initialize_objects(self):
        self.players = [] * 2
        self.bullets = []

        self.players.append(Tank(Rectangle(self.spawn1, TankSize, TankSize)))
        self.players.append(Tank(Rectangle(self.spawn2, TankSize, TankSize)))

        for tank in self.players:
            self.std_physics.objects.append(tank.hitBox)
            self.pixel_physics.objects.append(tank.hitBox)
            self.wall_physics.objects.append(tank.hitBox)

        self.bulletCooldowns = [0, 0]

    def initialize_buttons(self):
        self.up1 = False;
        self.left1 = False;
        self.down1 = False;
        self.right1 = False;
        self.up2 = False;
        self.left2 = False;
        self.down2 = False;
        self.right2 = False;

        self.restartButton = False;

        self.won = 0

    # called upon window resize
    def on_resize(self, size: Tuple[int, int]):
        # resize tank images to correct size
        self.blueTankImg = self.map.conv_img(load_py_img('tankAssets/BlueTank.png'), (TankSize, TankSize))
        self.greenTankImg = self.map.conv_img(load_py_img('tankAssets/GreenTank.png'), (TankSize, TankSize))
        self.bulletImg = self.map.conv_img(load_py_img('tankAssets/Bullet.png'), (BulletSize, BulletSize))
        self.winnerImg = self.map.conv_img(load_py_img('tankAssets/winner.png'), (BulletSize, BulletSize))
        w,h = size
        self.font = load_font('bit9x9.ttf', h // 8)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)

        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)
        self.std_physics.update_map(new_map)

    def update_game(self, keys_down, delta_t: int):
        if self.restartButton:
            self.initialize_objects()
            self.initialize_buttons()

        if not self.players[0].alive:
            text = self.font.render('Player 2 Wins', True, self.textColor)
            text_rect = text.get_rect()
            text_rect.center = (self.map.surface.get_width() //2, self.map.surface.get_height() //4)
            self.map.surface.blit(text, text_rect)

            #Put Winner Icon on top of P2
            self.map.image_py(self.winnerImg, self.players[1].hitBox.pos);
            self.stop_game()
            pygame.display.update()
            return
        if not self.players[1].alive:
            text = self.font.render('Player 1 Wins', True, self.textColor)
            text_rect = text.get_rect()
            text_rect.center = (self.map.surface.get_width() // 2, self.map.surface.get_height() // 4)
            self.map.surface.blit(text, text_rect)

            #Put Winner Icon on top of P1
            self.map.image_py(self.winnerImg, self.players[0].hitBox.pos);
            self.stop_game()
            pygame.display.update()
            return

        # make sure to call update for all physics the game is using
        self.pixel_physics.update(delta_t)
        self.wall_physics.update(delta_t)
        self.std_physics.update(delta_t)

        self.checkShot()
        self.checkKeys(delta_t)

        for i in range(len(self.players)):
            # ex
            #  self.map.image_py(self.tankimg, self.players[i].pos, size)
            if i == 0:
                self.map.image_py(self.blueTankImg, self.players[i].hitBox.pos)
            elif i == 1:
                self.map.image_py(self.greenTankImg, self.players[i].hitBox.pos)

            # self.players[i].hitBox.draw_hitbox(self.map.game_img)
            # cv2.line(self.map.game_img, (int(self.players[i].hitBox.pos.x), int(self.players[i].hitBox.pos.y)),
            #          (int(self.players[i].hitBox.pos.x + 12*math.cos(self.players[i].angle)),
            #             int(self.players[i].hitBox.pos.y + 12*math.sin(self.players[i].angle))), (69,42,210), 4)

        for bullet in self.bullets:
            bullet.timer -= 1

            if bullet.timer < 0:
                bullet.alive = False
                continue
            self.map.image_py(self.bulletImg, bullet.hitBox.pos)
            # bullet.hitBox.draw_hitbox(self.map.game_img)

        for i in range(len(self.bullets), 0):
            if not self.bullets[i].alive:
                self.remove(self.bullets[i])

        for i in range(len(self.bulletCooldowns)):
            self.bulletCooldowns[i] += delta_t

        pygame.display.update()

    def stop_game(self):
        for bullet in self.bullets:
            bullet.vel = 0;

        for tank in self.players:
            tank.playerSpeed = 0;

    def reset_game(self):
        self.players[0].alive = True
        self.players[0].hitbox = self.spawn1
        self.players[0].speed = 0;

        self.players[1].alive = True
        self.players[1].hitbox = self.spawn2
        self.players[1].speed = 0;

    def checkShot(self):
        for index in range(len(self.players)):
            for bullet in self.bullets:
                if self.players[index].hitBox.circle_collision(bullet.hitBox):
                    self.players[index].alive = False

                    bullet.alive = False
                    self.remove(bullet)
                    # self.remove(tank)

    def remove(self, obj: Bullet):
        self.std_physics.objects.remove(obj.hitBox)
        self.pixel_physics.objects.remove(obj.hitBox)
        self.wall_physics.objects.remove(obj.hitBox)
        self.bullets.remove(obj)

    def checkKeys(self, delta_t):
        if self.restartButton:
            self.initialize_buttons()
            self.initialize_objects()

        if self.right1:
            self.players[0].angle += self.players[0].turnSpeed * delta_t
            # self.players[0].rotateLeft(delta_t)

#           oldSurf = pygame.Surface((self.blueTankImg.hitbox.l*math.sqrt(2), self.blueTankImg.hitbox.h*math.sqrt(2)))

            #Rotates image
            oldSurf = self.players[0].hitBox

            self.blueTankImg = pygame.transform.rotate(self.blueTankImg, self.players[0].turnSpeed * delta_t)

            self.blueTankImg.get_rect().center = oldSurf.pos.x + oldSurf.l / 2, oldSurf.pos.x + oldSurf.h / 2
            #Rotates hitbox
            self.players[0].rotateRight(delta_t)
        if self.left1:
            self.players[0].angle -= self.players[0].turnSpeed * delta_t
            # self.players[0].rotateRight(delta_t)
            self.blueTankImg = pygame.transform.rotate(self.blueTankImg, -self.players[0].turnSpeed * delta_t)

        if self.up1:
            self.players[0].setSpeed(1)
        elif self.down1:
            self.players[0].setSpeed(-1)
        else:
            self.players[0].setSpeed(0)
        if self.right2:
            self.players[1].angle += self.players[1].turnSpeed * delta_t
            # self.players[1].rotateLeft(delta_t)
            self.greenTankImg = pygame.transform.rotate(self.greenTankImg, self.players[1].turnSpeed * delta_t)
        if self.left2:
            self.players[1].angle -= self.players[1].turnSpeed * delta_t
            # self.players[1].rotateRight(delta_t)
            self.greenTankImg = pygame.transform.rotate(self.greenTankImg, -self.players[1].turnSpeed * delta_t)
        if self.up2:
            self.players[1].setSpeed(1)
        elif self.down2:
            self.players[1].setSpeed(-1)
        else:
            self.players[1].setSpeed(0)

    def key_down(self, key_down: int):
        if key_down == keys.ACTIONB1 or key_down == keys.ACTIONB2:
            self.restartButton = True

        if key_down == keys.RIGHT1:
            self.right1 = True
        if key_down == keys.LEFT1:
            self.left1 = True

        if key_down == keys.UP1:
            self.up1 = True
        elif key_down == keys.DOWN1:
            self.down1 = True

        if key_down == keys.RIGHT2:
            self.right2 = True
        if key_down == keys.LEFT2:
            self.left2 = True

        if key_down == keys.UP2:
            self.up2 = True
        elif key_down == keys.DOWN2:
            self.down2 = True

        # ATM, only player 1 controls implemented, so set the "enter" key for player 1
        if key_down == keys.ACTIONA1:
            if self.bulletCooldowns[0] >= BulletCooldown:
                bulletSpawn = Vector2(self.players[0].hitBox.pos.x + 20 * math.cos(self.players[0].angle),
                                      self.players[0].hitBox.pos.y + 20 * math.sin(self.players[0].angle))
                bullet = Bullet(Circle(bulletSpawn, BulletSize), BulletSpeed, self.players[0].angle)
                self.bullets.append(bullet)
                self.std_physics.objects.append(bullet.hitBox)
                self.pixel_physics.objects.append(bullet.hitBox)
                self.wall_physics.objects.append(bullet.hitBox)

                self.bulletCooldowns[0] = 0

        if key_down == keys.ACTIONA2:
            if self.bulletCooldowns[1] >= BulletCooldown:
                bulletSpawn = Vector2(self.players[1].hitBox.pos.x + 20 * math.cos(self.players[1].angle),
                                      self.players[1].hitBox.pos.y + 20 * math.sin(self.players[1].angle))
                bullet = Bullet(Circle(bulletSpawn, BulletSize), BulletSpeed, self.players[1].angle)
                self.bullets.append(bullet)
                self.std_physics.objects.append(bullet.hitBox)
                self.pixel_physics.objects.append(bullet.hitBox)
                self.wall_physics.objects.append(bullet.hitBox)

                self.bulletCooldowns[1] = 0

    def key_up(self, key_up: int):
        if key_up == keys.RIGHT1:
            self.right1 = False
        if key_up == keys.LEFT1:
            self.left1 = False

        if key_up == keys.UP1:
            self.up1 = False
        elif key_up == keys.DOWN1:
            self.down1 = False

        if key_up == keys.RIGHT2:
            self.right2 = False
        if key_up == keys.LEFT2:
            self.left2 = False

        if key_up == keys.UP2:
            self.up2 = False
        elif key_up == keys.DOWN2:
            self.down2 = False

        if key_up == keys.ACTIONB1 or key_up == keys.ACTIONB2:
            self.restartButton = False


if __name__ == "__main__":
    test(TankGame2, None)
