from typing import List, Any, Tuple

import pygame
from numpy import ndarray

from game.util.vector2 import Vector2


class GameContext:
    def __init__(self, cam_img: ndarray, use_pygame=True):
        self.cam_img = cam_img
        self.height, self.width, _ = cam_img.shape  # width,height of game

        self.edges: ndarray = None  # the image with edges detected
        self.lines: ndarray = None  # the list of lines detected in the form [[[x1,y1,x2,y2]],[[...]],...]
        self.game_img: ndarray = None  # the output image to draw on
        self.lsd: Any = None  # the line segment detector
        self.lines_conv: ndarray = None
        self.pixels_per_meter = 50  # conversion for pixels to real physics
        if use_pygame:
            pywidth = pygame.display.get_surface().get_size()[0]
            aspect = self.height / float(self.width)
            pyheight = int(pywidth * aspect)  # size of pygame window
            self.pysize = (pywidth, pyheight)
            self.surface = pygame.display.set_mode(self.pysize)  # pygame surface
            self.s = pywidth / self.width  # scaling factor between game and pygame

    # convert game vector coords to pygame coords
    def cc(self, coord: Vector2) -> Tuple[int, int]:
        return coord.x * self.s, coord.y * self.s

    def draw_circle(self, pos: Vector2, radius: int):
        pass

    # convert game vector coords to pygame coordss
    def cc(self, coord: Vector2) -> Tuple[int, int]:
        return int(coord.x * self.sx()), int(coord.y * self.sy())

# base class for games
class Game:
    def __init__(self, initial_map: GameContext):
        self.map = initial_map

    # should be implemented by subclasses
    def update_game(self, keys_down: List[bool], delta_t: int):
        pass

    # called when key is pushed down
    def key_down(self, key: int):
        pass

    # called when key comes back up
    def key_up(self, key: int):
        pass

    # called when there is a new info from image processing
    def update_map(self, new_map: GameContext):
        self.map = new_map
        pass
