from typing import List

from numpy import ndarray


# represents information gathered from image processing
class CVMap:
    edges: ndarray
    lines: ndarray


# base class for games
class Game:
    def __init__(self, initial_map: CVMap):
        self.map = initial_map

    # should be implemented by subclasses
    # should return image of game to display
    def update_game(self, keys: List[bool], delta_t: int):
        pass

    # called when there is a new info from image processing
    def update_map(self, new_map: CVMap):
        self.map = new_map
