from typing import List, Any, Tuple, Union

import cv2
import pygame
from numpy import ndarray

from game.img.images import py_resize
from game.util.vector2 import Vector2

Coordinate = Union[Vector2, Tuple[float, float]]


class GameContext:
    def __init__(self, cam_img: ndarray, use_pygame=True):
        self.downscale = 0.7  # downscale level
        self.original_img:ndarray = cam_img

        h, w = cam_img.shape[0:2]
        cam_img = cv2.resize(cam_img, (int(w * self.downscale), int(h * self.downscale)))
        self.cam_img = cam_img
        self.width: int = cam_img.shape[1]  # width of game
        self.height: int = cam_img.shape[0]  # height of game

        self.edges: ndarray = None  # the image with edges detected
        self.lines: ndarray = None  # the list of lines detected in the form [[[x1,y1,x2,y2]],[[...]],...]
        self.game_img: ndarray = None  # the output image to draw on
        self.lsd: Any = None  # the line segment detector
        self.lines_conv: ndarray = None
        self.pixels_per_meter = 200  # conversion for pixels to real physics
        self.size = Vector2(self.width, self.height)
        if use_pygame:
            self.surface: pygame.Surface = pygame.display.get_surface()
            self.pysize = self.surface.get_size()
            self.sx = self.surface.get_width() / float(self.width)
            self.sy = self.surface.get_height() / float(self.height)

    def recalc_size(self):
        self.surface: pygame.Surface = pygame.display.get_surface()
        self.pysize = self.surface.get_size()
        self.sx = self.surface.get_width() / float(self.width)
        self.sy = self.surface.get_height() / float(self.height)

    # convert game coords/size to pygame coords/size
    def cc(self, coord: Coordinate) -> Tuple[int, int]:
        if isinstance(coord, Vector2):
            return int(coord.x * self.sx), int(coord.y * self.sy)
        if isinstance(coord, Tuple) or isinstance(coord, ndarray):
            return int(coord[0] * self.sx), int(coord[1] * self.sy)
        raise Exception('unsupported coordinate type')

    # convert tuple rect to tuple rect
    def cr(self, r: Tuple[float, float, float, float]) -> Tuple[int, int, int, int]:
        a = self.cc(r[0:2])
        b = self.cc(r[2:4])
        return a[0], a[1], b[0], b[1]

    def crr(self, r: Tuple[float, float, float, float]) -> Tuple[int, int, int, int]:
        a = self.cc((r[0],r[2]))
        b = self.cc((r[1],r[3]))
        return a[0], a[1], b[0]-a[0], b[1]-a[1]

    # convert pygame image to game size
    def conv_img(self, img: pygame.Surface, size: Coordinate):
        return py_resize(img, self.cc(size))

    # draw pygame image to screen (image should be from py_img_)
    def image_py(self, img: pygame.Surface, dest: Coordinate, flags: int = 0,
                 surface: pygame.Surface = None):
        if surface is None:
            surface = self.surface
        surface.blit(img, self.cc(dest), special_flags=flags)


# base class for games
class Game:
    def __init__(self, initial_map: GameContext):
        self.map: GameContext = initial_map

    # should be implemented by subclasses
    def update_game(self, keys_down: List[bool], delta_t: float):
        pass

    # called when key is pushed down
    def key_down(self, key: int):
        pass

    # called when key comes back up
    def key_up(self, key: int):
        pass

    # called on window resize
    def on_resize(self, size: Tuple[int, int]):
        self.map.recalc_size()

    # called when there is a new info from image processing
    def update_map(self, new_map: GameContext):
        self.map = new_map
        pass
