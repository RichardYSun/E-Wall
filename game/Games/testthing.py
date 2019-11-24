from typing import List, Dict, Tuple

import pygame
from numpy.core.multiarray import ndarray

from game import keys
from game.game import Game, GameContext
from game.physics2.objects.pixelobject import PixelObject
from game.test import test
from game.img.images import load_py_img, imread
from game.util.vector2 import Vector2

import cv2


class AnimationState:
    def __init__(self, img: str, game_size: Tuple[float, float] = None, offset: Vector2 = Vector2(0, 0),
                 timer: float = None,
                 next_state: str = None):
        self.o_py_img: pygame.Surface = load_py_img(img)
        self.cv_img: ndarray = imread(img, cv2.IMREAD_UNCHANGED)
        self.py_img: pygame.Surface = None

        self.next_state: str = next_state
        self.timer: float = timer
        self.offset: Vector2 = offset
        if game_size is None:
            game_size = self.o_py_img.get_size()
        self.game_size: Vector2 = game_size

    def load(self, mp: GameContext):
        self.py_img = mp.conv_img(self.o_py_img, self.game_size)


A = AnimationState


class c(PixelObject):
    def __init__(self, pos: Vector2, mp: GameContext):
        super().__init__(pos)
        self.facing = 'right'
        self.state: str = 'rest'
        self.states: Dict[str, AnimationState] = {
            'rest': A('ree/rest.bmp'),
            'walk1': A('ree/walk2.bmp'),
            'walk2': A('ree/rest.bmp'),
            'walk3': A('ree/walk1.bmp'),
            'walk4': A('ree/rest.bmp'),
            'jump_ready': A('ree/jump_ready.png'),
            'jump1': A('ree/jump1.png'),
            'jump2': A('ree/jump2.png'),
            'jump3': A('ree/jump3.png'),
            'jump4': A('ree/jump3.png'),
            'jump_land': A('ree/jump_land.png'),
            'jump_land2': A('ree/jump_ready.png'),
        }

        self.timer = 0
        # self.is_rect = True
        self.mp: GameContext = mp

    def on_resize(self, size: Tuple[int, int]):
        for s in self.states.values():
            s.load(self.mp)

    def update_map(self, new_map: GameContext):
        self.mp = new_map

    def set_state(self, state: str):
        self.state = state
        state = self.states[self.state]
        self.pos += state.offset
        if state.timer is not None:
            self.timer = 0

    # TODO actually use this
    def check_timer(self, delta_t: float):
        state = self.states[self.state]
        if state.timer is None:
            return
        self.timer += delta_t
        if self.timer > state.timer:
            self.timer = 0
            self.state = state.next_state

    def update(self, delta_t: float, down: List[bool]):
        w, h = self.states[self.state].py_img.get_size()
        self.vel.y += 9.8 * delta_t * self.mp.pixels_per_meter
        self.pos += self.vel * delta_t
        grounded = self.pos.y + h >= self.mp.height
        spd = w
        jmp = -4 * self.mp.pixels_per_meter
        friction = 10
        if grounded:
            self.pos.y = self.mp.height - h + 1
            self.vel.y = 0

            if self.state == 'jump_ready':
                if self.timer > 0.05:
                    self.vel.y = jmp

                    self.pos.y = self.mp.height - h - 1
                    self.state = 'jump1'
            else:
                if self.state == 'jump4':
                    self.timer = 0
                    self.state = 'jump_land'
                elif self.state == 'jump_land':
                    if self.timer > 0.2:
                        self.timer = 0
                        self.state = 'jump_land2'
                elif self.state == 'jump_land2':
                    if self.timer > 0.1:
                        self.state = 'rest'
                else:
                    moving = False
                    if down[keys.RIGHT1]:
                        self.facing = 'right'
                        self.vel.x = spd
                        moving = True
                    if down[keys.LEFT1]:
                        self.facing = 'left'
                        self.vel.x = -spd
                        moving = True
                    if moving:
                        friction = 0
                        if self.state == 'walk1':
                            if self.timer >= 0.2:
                                self.timer = 0
                                self.state = 'walk2'
                        elif self.state == 'walk2':
                            if self.timer >= 0.2:
                                self.timer = 0
                                self.state = 'walk3'
                        elif self.state == 'walk3':
                            if self.timer >= 0.2:
                                self.timer = 0
                                self.state = 'walk4'
                        elif self.state == 'walk4':
                            if self.timer >= 0.2:
                                self.timer = 0
                                self.state = 'walk1'
                        else:
                            self.state = 'walk1'
                            self.timer = 0
                    else:
                        self.state = 'rest'

                    if down[keys.UP1]:
                        self.state = 'jump_ready'
                        self.timer = 0
                self.vel.x -= self.vel.x * friction * delta_t
        else:
            if self.vel.y < 10:
                self.state = 'jump1'
            else:
                self.state = 'jump4'
        self.timer += delta_t

    def draw(self):
        img = self.states[self.state].py_img
        if self.facing == 'left':
            img = pygame.transform.flip(img, True, False)
        self.mp.image_py(img, self.pos)


class re(Game):

    def on_resize(self, size: Tuple[int, int]):
        self.r.on_resize(size)

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer
        self.r = c(Vector2(50, 50), mp)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)
        self.r.update_map(new_map)

    def update_game(self, keys_down: List[bool], delta_t: int):
        self.r.update(delta_t, keys_down)

        s = self.map.surface
        s.fill((255, 255, 255))
        self.r.draw()
        pygame.display.flip()


test(re, 'kust')
