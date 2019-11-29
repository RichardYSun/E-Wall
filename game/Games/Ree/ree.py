from typing import List, Tuple

import pygame
from cv2 import cv2
from numpy.core.multiarray import ndarray

from game.Games.Ree.book import Book
from game.Games.Ree.bullet import Bullet, Living
from game.Games.Ree.dude import Dude
from game.Games.Ree.enemy import Enemy
from game.Games.Ree.flag import Flag
from game.Games.Ree.player import Player
from game.cv.matcher import Matcher
from game.game import Game, GameContext
from game.img.images import imread, load_py_img
from game.physics2.pixelphysics import PixelPhysics, check_pixel_collision
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.util.vector2 import Vector2


class Ree(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer
        self.bullets: List[Bullet] = []
        self.living: List[Living] = []

        self.pixel_physics = PixelPhysics()
        self.wall_physics = WallPhysics()
        self.matcher = Matcher()
        self.frame = 0

        self.player = Player(Vector2(0, 0), self)
        self.pixel_physics.objects.append(self.player)
        self.living.append(self.player)
        self.wall_physics.objects.append(self.player)

        self.matcher = Matcher()

        self.add_template('ree/enemies/dude.jpg', Dude)
        self.add_template('ree/flag.jpg', Flag)
        self.add_template('ree/enemies/book.jpg', Book)

        self.templates = []

        self.won = 0
        self.win_img = None
        self.update_map(mp)

        lose_img = load_py_img('death.png')
        self.lose_img = pygame.transform.scale(lose_img, pygame.display.get_surface().get_size())

    def add_template(self, img: str, E):
        kek = []

        def on_appear(transform: ndarray, rect: List[Tuple[float, float]]):
            kek.append(E(transform, rect, self))
            self.templates.append(kek[0])

        def on_move(transform: ndarray, rect: List[Tuple[float, float]]):
            ree = kek[0]
            ree.update_hitbox(transform, rect)

        self.matcher.add_obj(imread(img), on_appear, on_move)

    def on_resize(self, size: Tuple[int, int]):
        super().on_resize(size)
        self.player.on_resize(size)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)
        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)
        self.player.update_map(new_map)
        self.frame += 1
        if self.frame == 10 :
            self.frame = 0
            self.matcher.update_map(new_map)

    def add_bullet(self, img: str, pos: Vector2, vel: Vector2, damage: float, src, size=None):
        b = Bullet(self.map, pos, img, damage, vel, src, size)
        self.pixel_physics.objects.append(b)
        self.wall_physics.objects.append(b)
        self.bullets.append(b)

    def remove_bullet(self, b: Bullet):
        self.pixel_physics.objects.remove(b)
        self.wall_physics.objects.remove(b)
        self.bullets.remove(b)

    def update_bullets(self, delta_t: float):
        for j in range(len(self.bullets) - 1, -1, -1):
            bul = self.bullets[j]
            bul.update(delta_t)
            flag = False

            for i in range(len(self.living) - 1, -1, -1):
                obj = self.living[i]
                col = check_pixel_collision(obj, bul)
                if bul.src is not obj and col > 0:
                    obj.damage(bul.damage)
                    if obj.health <= 0:
                        obj.die()
                    self.remove_bullet(bul)
                    flag = True
                    break

            # if bullet is not already dead and collided with wall, remove it
            if not flag:
                if bul.death_flag:
                    self.remove_bullet(bul)

    def update_game(self, keys_down: List[bool], delta_t: float):
        if self.player.health <= 0:
            surface = pygame.display.get_surface()
            surface.blit(self.lose_img, (0, 0))
            pygame.display.update()
        elif self.won:
            surface = pygame.display.get_surface()
            surface.blit(self.win_img, (0, 0))
            pygame.display.update()
        else:
            self.pixel_physics.update(delta_t)
            self.wall_physics.update(delta_t)

            self.player.update(delta_t, keys_down)

            self.update_bullets(delta_t)

            self.player.draw()
            for b in self.bullets:
                b.draw(self.map)

            for k in self.templates:
                k.update(delta_t)
                k.draw()

            pygame.surfarray.pixels_green(self.map.surface).fill(0)
            pygame.surfarray.pixels_blue(self.map.surface).fill(0)

            pygame.display.flip()

    def win(self):
        surface = pygame.display.get_surface()
        win_img = load_py_img('Win.png')
        self.win_img = pygame.transform.scale(win_img, surface.get_size())
        self.won = 1


if __name__ == "__main__":
    test(Ree, None)  # '../ree/enemies/squaredude.jpg')
    # test(Ree,'smalldude3.jpg')
