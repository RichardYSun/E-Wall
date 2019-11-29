from typing import Tuple, Dict, List

import pygame

from game import keys
from game.Games.Ree.animationstate import AnimationState
from game.Games.Ree.bullet import Living

from game.game import GameContext
from game.physics2.collisiontypes import COLLISION_SLIDE
from game.sound.sounds import load_sound
from game.util.vector2 import Vector2


class Player(Living):

    def __init__(self, pos: Vector2, gm):
        super().__init__(2000, pos)
        self.facing = 'right'
        self.state: str = 'rest'
        self.game_size = (115, 150)
        self.gm = gm

        def A(nm: int):
            return AnimationState(img='ree/player/sprite_' + str(nm) + '.png',
                                  game_size=None,
                                  scale=0.4)

        self.states: Dict[str, AnimationState] = {
            'rest': A(0),
            'walk1': A(1),
            'walk2': A(2),
            'walk3': A(3),
            'walk4': A(0),
            'jump_ready': A(4),
            'jump1': A(5),
            'jump2': A(6),
            'jump3': A(7),
            'jump4': A(7),
            'jump_land': A(8),
            'jump_land2': A(4),
        }

        self.timer = 0
        # self.is_rect = True

        self.use_direct_img = True
        self.mp: GameContext = gm.map
        self.collision_type = COLLISION_SLIDE
        self.grounded_timer = 0
        self.jmp_timer = 0
        self.shoot_timer = 0
        self.shoot_sound = load_sound('ree/fire.wav')

    def on_resize(self, size: Tuple[int, int]):
        for s in self.states.values():
            s.load(self.mp)

    def update_map(self, new_map: GameContext):
        self.mp = new_map

    def set_state(self, state: str):

        self.state = state

        kstate = self.states[self.state]
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

    def update_movement(self, delta_t: float, down: List[bool]):
        w, h = self.game_size
        self.grounded_timer -= delta_t
        # self.jmp_timer -= delta_t
        if self.touching_bottom or self.collision_escape_vector.y < 0:
            self.grounded_timer = 0.1
        grounded = self.grounded_timer >= 0
        spd = w * 1.5
        jmp = -h * 3
        friction = 10

        if grounded:

            if self.state == 'jump_ready':
                if self.timer > 0.05:
                    self.vel.y = jmp
                    self.pos.y -= 20
                    # self.jmp_timer = 0.1
                    self.set_state('jump1')
            else:
                if self.state == 'jump4':
                    self.timer = 0
                    self.set_state('jump_land')
                elif self.state == 'jump_land':
                    if self.timer > 0.2:
                        self.timer = 0
                        self.pos.y -= 10
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

    def update_gun(self, down: List[bool], delta_t: float):
        self.shoot_timer -= delta_t
        bullet_vel = Vector2(self.gm.map.pixels_per_meter, 0)
        bullet_dmg = 100

        if self.shoot_timer <= 0 and down[keys.ACTIONA1]:
            self.shoot_timer = 0.5
            self.shoot_sound.play()
            if self.facing == 'left':
                self.gm.add_bullet('1.png', self.pos + Vector2(0, 10), bullet_vel * -1, bullet_dmg, self)
            else:
                self.gm.add_bullet('1.png', self.pos + Vector2(0, 10), bullet_vel, bullet_dmg, self)

    def update(self, delta_t: float, down: List[bool]):
        self.update_movement(delta_t, down)
        self.update_gun(down, delta_t)

        self.vel.y += 9.81 * delta_t * self.mp.pixels_per_meter
        self.pos += self.vel * delta_t

    def draw_healthbar(self):
        bnds = self.get_bounds()
        ctr_x = (bnds[0] + bnds[1]) / 2
        bar_len, bar_w = 70, 6
        rect = self.mp.cr((ctr_x - bar_len / 2, bnds[2] - 6 - bar_w, bar_len, bar_w))
        rect2 = self.mp.cr((ctr_x - bar_len / 2, bnds[2] - 6 - bar_w, bar_len * self.health / self.max_health, bar_w))
        pygame.draw.rect(self.mp.surface, (255, 255, 255), rect2)
        pygame.draw.rect(self.mp.surface, (255, 255, 255), rect,2)

    def draw(self):
        img = self.states[self.state].py_img
        if self.facing == 'left':
            img = pygame.transform.flip(img, True, False)
        self.mp.image_py(img, self.pos)
        self.draw_healthbar()

    def get_hitbox(self):
        return self.states[self.state].cv_img

    def damage(self, damage: float):
        super().damage(damage)
