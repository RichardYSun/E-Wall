import cv2
import numpy

from game.game import Game, GameContext
from game.physics2.collisiontypes import COLLISION_BOUNCE
from game.physics2.objects.circle import Circle
from game.physics2.pixelphysics import PixelPhysics
from game.physics2.standardphysics import StandardPhysics
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.util.moreimutils import conv_cv_to_py
from game.util.vector2 import Vector2
import game.keys as keys
import pygame

BALL_VEL = Vector2(200, 200)


class Pong(Game):

    def __init__(self, mp: GameContext):
        super().__init__(mp)  # make sure to call superclass initializer

        # we will use three physics modules in this game: StandardPhysics, PixelPhysics, WallPhysics
        # StandardPhysics makes objects move and applies gravity if needed
        self.std_physics = StandardPhysics(gravity=None)  # in this game we don't want gravity
        self.pixel_physics = PixelPhysics()  # PixelPhysics handles collisions of the camera image with the game objects
        self.wall_physics = WallPhysics()  # WallPhysics makes the objects bounce off walls
        # since this is pong, we want to disable the left and right walls
        self.wall_physics.left = False
        self.wall_physics.right = False

        # create the ball
        # Vector2(mp.width / 2, mp.height / 2) means the ball is in the center of the screen
        # 20 is the radius
        self.ball = Circle(Vector2(mp.width / 2, mp.height / 2), 20)
        self.ball.collision_type = COLLISION_BOUNCE  # this makes the ball bouncy
        self.ball.vel = BALL_VEL  # make the ball begin moving

        # we must add the ball to each physics module we want it to follow
        self.std_physics.objects.append(self.ball)  # we want the ball to move
        self.pixel_physics.objects.append(self.ball)  # we want the ball to bounce off stuff in the frame
        self.wall_physics.objects.append(self.ball)  # we want the ball to bounce off walls

        self.score = (0, 0)

        self.start = 0

        self.win = 0

        self.winTime = 0

    # this is called when there is a new frame available from camera
    def update_map(self, new_map: GameContext):
        super().update_map(new_map)  # make sure to call super

        # make sure to call update_map for all the physics you're using
        self.pixel_physics.update_map(new_map)
        self.wall_physics.update_map(new_map)
        self.std_physics.update_map(new_map)

    def key_down(self, key: int):
        if key == keys.ENTER:
            self.start = 1

    def update_game(self, keys, delta_t: float):
        if self.win != 0:
            self.winTime += delta_t
            if self.winTime > 2:
                self.score = (0, 0)
                self.win = 0
                return

            surface = self.map.surface
            surface.fill((0, 0, 0))

            pixels = pygame.transform.scale(conv_cv_to_py(self.map.edges), surface.get_size())
            surface.blit(pixels, (0, 0))

            pos = [(surface.get_width() // 4, surface.get_height() // 2),
                   (surface.get_width() * 3 // 4, surface.get_height() // 2)]

            self.draw_win(surface, pos[self.win - 1])
            self.draw_lose(surface, pos[2 - self.win])

            self.ball.draw(surface, self.map)

            self.draw_score(surface)

            pygame.display.update()
        else:
            if self.start:
                # make sure to call update for all physics the game is using
                self.pixel_physics.update(delta_t)
                self.wall_physics.update(delta_t)
                self.std_physics.update(delta_t)

                # detect win conditions
                xmn, xmx, ymn, ymx = self.ball.get_bounds()
                if xmn < 0:  # player 1 wins
                    self.ball.pos.x = self.map.width / 2  # reset ball to center
                    self.ball.pos.y = self.map.height / 2
                    self.ball.vel = BALL_VEL * self.map.downscale  # reset ball velocity
                    self.score = (self.score[0] + 1, self.score[1])  # increment score
                    if self.score[0] == 1:
                        self.win = 1
                        self.winTime = 0
                    self.start = 0
                if xmx > self.map.width:  # player 2 wins
                    self.ball.pos.x = self.map.width / 2  # reset ball to center
                    self.ball.pos.y = self.map.height / 2
                    self.ball.vel = BALL_VEL * self.map.downscale  # reset ball velocity
                    self.score = (self.score[0], self.score[1] + 1)  # increment score
                    if self.score[1] == 1:
                        self.win = 2
                        self.winTime = 0
                    self.start = 0

            # as a precaution, always draw stuff at the END of the update function
            surface = self.map.surface

            surface.fill((255, 255, 255))

            pixels = pygame.transform.scale(conv_cv_to_py(self.map.edges), surface.get_size())
            surface.blit(pixels, (0, 0))

            self.ball.draw(surface, self.map)

            self.draw_score(surface)

            pygame.display.update()

    def draw_score(self, surface):
        colour = (0, 255, 0)
        font = pygame.font.SysFont('arial', surface.get_width() // 6)
        text = font.render(str(self.score[0]) + "           " + str(self.score[1]), True, colour)
        textRect = text.get_rect()
        textRect.center = (surface.get_width() // 2, surface.get_height() // 10)

        surface.blit(text, textRect)

    def draw_win(self, surface, pos):
        colour = (0, 255, 0)
        font = pygame.font.SysFont('arial', surface.get_width() // 8)
        text = font.render('Winner', True, colour)
        textRect = text.get_rect()
        textRect.center = (surface.get_width() // 4, surface.get_height() // 2)

        surface.blit(text, textRect)

    def draw_lose(self, surface, pos):
        colour = (0, 255, 0)
        font = pygame.font.SysFont('arial', surface.get_width() // 8)
        text = font.render('Loser', True, colour)
        textRect = text.get_rect()
        textRect.center = (surface.get_width() * 3 // 4, surface.get_height() // 2)

        surface.blit(text, textRect)


test(Pong, None)
