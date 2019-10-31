from typing import List, Any

from numpy import ndarray


# represents information gathered from image processing
class CVMap:
    edges: ndarray  # the image with edges detected
    lines: ndarray  # the list of lines detected in the form [[[x1,y1,x2,y2]],[[...]],...]
    game_img: ndarray  # the output image to draw on
    lsd: Any  # the line segment detector
    lines_conv: ndarray


# base class for games
class Game:
    def __init__(self, initial_map: CVMap):
        self.map = initial_map

    # should be implemented by subclasses
    def update_game(self, keys: List[bool], delta_t: int):
        pass

    # called when there is a new info from image processing
    def update_map(self, new_map: CVMap):
        self.map = new_map
