from typing import List, Dict, Tuple

import pygame

from game import keys
from game.game import Game, GameContext
from game.physics2.objects.physicsobject import PhysicsObject
from game.test import test
from game.util.moreimutils import get_py_img
from game.util.vector2 import Vector2


class c(PhysicsObject):
    def __init__(self, pos: Vector2):
        super().__init__(pos)
        self.facing = 'right'
        self.state = 'rest'
        self.states: Dict[str, pygame.Surface] = {
            'rest': get_py_img('test2/ree0.bmp',0.5),
            'walk1': get_py_img('test2/ree1.bmp',0.5),
            'walk2': get_py_img('test2/ree0.bmp',0.5),
            'walk3': get_py_img('test2/ree3.bmp',0.5),
            'walk4': get_py_img('test2/ree0.bmp',0.5),
            'jump_ready': get_py_img('test2/jump_ready.png',0.5),
            'jump1': get_py_img('test2/jump1.png',0.5),
            'jump2': get_py_img('test2/jump2.png',0.5),
            'jump3': get_py_img('test2/jump3.png',0.5),
            'jump4': get_py_img('test2/jump3.png',0.5),
            'jump_land': get_py_img('test2/jump_land.png',0.5),
            'jump_land2': get_py_img('test2/jump_ready.png',0.5),
        }

        self.timer = 0
        self.mp: GameContext = None

    def update_map(self, new_map: GameContext):
        self.mp = new_map

    def update(self, delta_t: float, down: List[bool]):
        w, h = self.states[self.state].get_size()
        self.vel.y += 9.8 * delta_t * self.mp.pixels_per_meter
        self.pos += self.vel * delta_t
        grounded = self.pos.y + h >= self.mp.height
        spd = w*2
        jmp = -4 * self.mp.pixels_per_meter
        jump2_vel = -2 * self.mp.pixels_per_meter
        jump3_vel = 2 * self.mp.pixels_per_meter
        friction = 10
        jump_min_x = w/2
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
                    if down[keys.RIGHT]:
                        self.facing = 'right'
                        self.vel.x = spd
                        moving = True
                    if down[keys.LEFT]:
                        self.facing = 'left'
                        self.vel.x = -spd
                        moving = True
                    if moving:
                        friction=0
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

                    if down[keys.UP]:
                        self.state = 'jump_ready'
                        self.timer = 0
                self.vel.x -=self.vel.x*friction*delta_t
        else:
            friction=0
            if self.vel.y < 10:
                self.state = 'jump1'
            else:
                self.state = 'jump4'
        self.timer += delta_t

    def draw(self, surface: pygame.Surface):
        img = self.states[self.state]
        if self.facing == 'left':
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, self.pos.as_int_tuple())


class re(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer
        self.r = c(Vector2(50, 50))

    def update_map(self, new_map: GameContext):
        super().update_map(new_map)
        self.r.update_map(new_map)

    def update_game(self, keys_down: List[bool], delta_t: int):
        self.r.update(delta_t, keys_down)

        s = self.map.surface
        s.fill((255, 255, 255))
        self.r.draw(s)
        pygame.display.flip()


test(re, 'kust')
