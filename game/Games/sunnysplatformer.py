from typing import List

from game.game import Game, GameContext
from game.physics2.objects.platformcharacter import PlatformCharacter
from game.physics2.pixelphysics import PixelPhysics
from game.physics2.standardphysics import StandardPhysics
from game.physics2.wallphysics import WallPhysics
from game.test import test
import cv2

from game.util.moreimutils import imread
from game.util.vector2 import Vector2


class Character(PlatformCharacter):
    rest_right = imread('sunnysplatformer/walk1.png', cv2.IMREAD_UNCHANGED,  (30,120))
    walk1_right = imread('sunnysplatformer/walk0.png', cv2.IMREAD_UNCHANGED, (30,120))
    walk2_right = imread('sunnysplatformer/walk2.png', cv2.IMREAD_UNCHANGED, (30,120))


class SunnysPlatformer(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer

        self.std_physics = StandardPhysics()
        self.pixel_physics = PixelPhysics()
        self.wall_physics = WallPhysics()

        self.c = Character(Vector2(mp.width / 2, 50))
        self.std_physics.objects.append(self.c)
        self.pixel_physics.objects.append(self.c)
        self.wall_physics.objects.append(self.c)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)

        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)
        self.std_physics.update_map(new_map)

    def key_down(self, key: int):
        pass

    def update_game(self, keys_down: List[bool], delta_t: int):

        self.std_physics.update(delta_t)
        self.wall_physics.update(delta_t)
        self.pixel_physics.update(delta_t)
        self.wall_physics.update(delta_t)

        self.c.update(delta_t, keys_down)

        self.c.draw(self.map.game_img)


test(SunnysPlatformer, 'kust')
