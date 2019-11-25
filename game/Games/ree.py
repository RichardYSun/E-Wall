from typing import List, Dict, Tuple

import pygame
from numpy.core.multiarray import ndarray

from game import keys
from game.game import Game, GameContext
from game.physics2.collisiontypes import COLLISION_SLIDE, COLLISION_STICK
from game.physics2.objects.pixelobject import PixelObject
from game.physics2.pixelphysics import PixelPhysics
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.img.images import load_py_img, imread
from game.util.vector2 import Vector2

import cv2


class AnimationState:
    def __init__(self, img: str, game_size: Tuple[float, float], offset: Vector2 = Vector2(0, 0),
                 timer: float = None,
                 next_state: str = None):
        self.o_py_img: pygame.Surface = load_py_img(img).convert_alpha()

        self.cv_img: ndarray = cv2.extractChannel(imread(img, cv2.IMREAD_UNCHANGED), 3)
        self.py_img: pygame.Surface = None

        self.next_state: str = next_state
        self.timer: float = timer
        self.offset: Vector2 = offset
        if game_size is None:
            game_size = self.o_py_img.get_size()
        self.game_size: Vector2 = game_size
        self.cv_img = cv2.resize(self.cv_img, game_size)

    def load(self, mp: GameContext):
        self.py_img = mp.conv_img(self.o_py_img, self.game_size)


class Stuart(PixelObject):

    def __init__(self, pos: Vector2, mp: GameContext):
        super().__init__(pos)
        self.facing = 'right'
        self.state: str = 'rest'
        self.game_size = (230, 300)

        def A(nm: str, off:Tuple[int,int]=(0,0)):
            return AnimationState(nm, self.game_size, Vector2(off[0],off[1]))

        self.states: Dict[str, AnimationState] = {
            'rest': A('ree/walk_0.png',),
            'walk1': A('ree/walk_1.png',),
            'walk2': A('ree/walk_2.png',),
            'walk3': A('ree/walk_3.png',),
            'walk4': A('ree/walk_0.png',),
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
        self.use_direct_img = True
        self.mp: GameContext = mp
        self.collision_type = COLLISION_SLIDE
        self.grounded_timer = 0
        self.jmp_timer = 0

    def on_resize(self, size: Tuple[int, int]):
        for s in self.states.values():
            s.load(self.mp)

    def update_map(self, new_map: GameContext):
        self.mp = new_map

    def set_state(self, state: str):
        kstate = self.states[self.state]
        self.pos -= kstate.offset

        self.state = state

        kstate = self.states[self.state]
        self.pos += kstate.offset
        if kstate.timer is not None:
            self.timer = 0

    # TODO actually use this
    def check_timer(self, delta_t: float):
        state = self.states[self.state]
        if state.timer is None:
            return
        self.timer += delta_t
        if self.timer > state.timer:
            self.timer = 0
            self.set_state(state.next_state)

    def update(self, delta_t: float, down: List[bool]):
        w, h = self.game_size
        self.vel.y += 9.81 * delta_t * self.mp.pixels_per_meter
        self.pos += self.vel * delta_t
        self.grounded_timer -= delta_t
        # self.jmp_timer -= delta_t
        if self.collision_escape_vector.y < 0:
            self.grounded_timer = 0.1
        grounded = self.grounded_timer >= 0
        spd = w
        jmp = -h * 3
        friction = 10
        if grounded:

            if self.state == 'jump_ready':
                if self.timer > 0.05:
                    self.vel.y = jmp
                    self.pos.y -= 10
                    # self.jmp_timer = 0.1
                    self.set_state('jump1')
            else:
                if self.state == 'jump4':
                    self.timer = 0
                    self.set_state('jump_land')
                elif self.state == 'jump_land':
                    if self.timer > 0.2:
                        self.timer = 0
                        self.set_state('jump_land2')
                elif self.state == 'jump_land2':
                    if self.timer > 0.1:
                        self.set_state('rest')
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
                                self.set_state('walk2')
                        elif self.state == 'walk2':
                            if self.timer >= 0.2:
                                self.timer = 0
                                self.set_state('walk3')
                        elif self.state == 'walk3':
                            if self.timer >= 0.2:
                                self.timer = 0
                                self.set_state('walk4')
                        elif self.state == 'walk4':
                            if self.timer >= 0.2:
                                self.timer = 0
                                self.set_state('walk1')
                        else:
                            self.set_state('walk1')
                            self.timer = 0
                    else:
                        self.set_state('rest')

                    if down[keys.UP1]:
                        self.set_state('jump_ready')
                        self.timer = 0
                self.vel.x -= self.vel.x * friction * delta_t
        else:
            if self.vel.y < 10:
                self.set_state('jump1')
            else:
                self.set_state('jump4')
        self.timer += delta_t

    def draw(self):
        img = self.states[self.state].py_img
        if self.facing == 'left':
            img = pygame.transform.flip(img, True, False)
        self.mp.image_py(img, self.pos)

    def get_hitbox(self):
        return self.states[self.state].cv_img


class Ree(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer
        self.r = Stuart(Vector2(0, 0), mp)
        self.p = PixelPhysics()
        self.w = WallPhysics()
        self.p.objects.append(self.r)
        self.w.objects.append(self.r)

    def on_resize(self, size: Tuple[int, int]):
        self.r.on_resize(size)

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)
        self.p.update_map(new_map)
        # self.w.update_map(new_map)
        self.r.update_map(new_map)

    def update_game(self, keys_down: List[bool], delta_t: int):
        self.p.update(delta_t)
        # self.w.update(delta_t)
        self.r.update(delta_t, keys_down)

        s = self.map.surface
        self.r.draw()
        pygame.display.flip()


test(Ree,'kust')
