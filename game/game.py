from typing import List, Any, Tuple, Union

import pygame
from numpy import ndarray

from game.util.vector2 import Vector2

Coordinate = Union[Vector2, Tuple[float, float]]


class GameContext:
    def __init__(self, cam_img: ndarray, use_pygame=True):
        self.width: int = cam_img.shape[1]  # width of game
        self.height: int = cam_img.shape[0]  # height of game
        self.cam_img = cam_img

        self.edges: ndarray = None  # the image with edges detected
        self.lines: ndarray = None  # the list of lines detected in the form [[[x1,y1,x2,y2]],[[...]],...]
        self.game_img: ndarray = None  # the output image to draw on
        self.lsd: Any = None  # the line segment detector
        self.lines_conv: ndarray = None
        self.pixels_per_meter = 50  # conversion for pixels to real physics
        if use_pygame:
            self.surface = pygame.display.get_surface()
            self.pysize = self.surface.get_size()
            self.sx = self.surface.get_width() / float(self.width)
            self.sy = self.surface.get_height() / float(self.height)

    # convert game coords to pygame coords
    def cc(self, coord: Coordinate) -> Tuple[int, int]:
        if coord is Vector2:
            return coord.x * self.sx, coord.y * self.sy
        if coord is Tuple[float,float]:
            return coord[0] * self.sx, coord[1] * self.sy
        raise Exception('unsupported coordinate type')

    # convert tuple rect to tuple rect
    def cr(self, r: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        x, y = self.sx, self.sy
        return r[0] * x, r[1] * y, r[2] * x, r[3] * y

    # draw pygame image to screen (image should be from py_img_)
    def image_py(self, img: pygame.Surface, dest: Coordinate, flags=0, surface: pygame.Surface = None):
        if surface is None:
            surface = self.surface
        surface.blit(img, self.cc(dest), special_flags=flags)


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
