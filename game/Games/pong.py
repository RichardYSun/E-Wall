import cv2

from game.game import Game, GameContext
from game.physics2.collisiontypes import COLLISION_BOUNCE
from game.physics2.objects.circle import Circle
from game.physics2.pixelphysics import PixelPhysics
from game.physics2.standardphysics import StandardPhysics
from game.physics2.wallphysics import WallPhysics
from game.test import test
from game.util.vector2 import Vector2
import game.keys as keys


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
        self.ball.vel = Vector2(200, 200)  # make the ball begin moving

        # we must add the ball to each physics module we want it to follow
        self.std_physics.objects.append(self.ball)  # we want the ball to move
        self.pixel_physics.objects.append(self.ball)  # we want the ball to bounce off stuff in the frame
        self.wall_physics.objects.append(self.ball)  # we want the ball to bounce off walls

        self.score = (0, 0)

        self.start = 0

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

    def update_game(self, keys, delta_t: int):
        if self.start:

            # make sure to call update for all physics the game is using
            self.pixel_physics.update(delta_t)
            self.wall_physics.update(delta_t)
            self.std_physics.update(delta_t)

            # detect win conditions
            xmn, xmx, ymn, ymx = self.ball.get_bounds()
            if xmn < 0:  # player 1 wins
                self.ball.pos.x = self.map.width / 2  # reset ball to center
                self.ball.vel = Vector2(200, 200)  # reset ball velocity
                self.score = (self.score[0] + 1, self.score[1])  # increment score
                self.start = 0
            if xmx > self.map.width:  # player 2 wins
                self.ball.pos.x = self.map.width / 2  # reset ball to center
                self.ball.vel = Vector2(200, 200)  # reset ball velocity
                self.score = (self.score[0], self.score[1] + 1)  # increment score
                self.start = 0

        # as a precaution, always draw stuff at the END of the update function
        self.ball.draw_hitbox(self.map.game_img)

        self.draw_score()

    def draw_score(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        pos = (self.map.height // 2, 200)
        colour = (0, 255, 0)
        font_scale = 2
        thickness = 2

        cv2.putText(self.map.game_img, str(self.score[0]) + " " + str(self.score[1]), pos, font, font_scale, colour,
                    thickness, cv2.LINE_AA)

test(Pong, None)
