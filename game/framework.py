class CVMap:
    def __init__(self, edges):
        self.edges = edges


class Game:
    def __init__(self, initial_map: CVMap):
        self.map = initial_map

    def update_game(self, keys, delta_t: int):
        pass

    def update_map(self, new_map: CVMap):
        self.map = new_map
