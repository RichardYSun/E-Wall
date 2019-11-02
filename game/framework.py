from typing import List, Any

from numpy import ndarray


# represents information gathered from image processing
class CVMap:
    def __init__(self,width,height):
        self.width:int=width
        self.height:int=height
        self.edges: ndarray = None  # the image with edges detected
        self.lines: ndarray = None  # the list of lines detected in the form [[[x1,y1,x2,y2]],[[...]],...]
        self.game_img: ndarray = None  # the output image to draw on
        self.lsd: Any = None  # the line segment detector
        self.lines_conv: ndarray = None


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
