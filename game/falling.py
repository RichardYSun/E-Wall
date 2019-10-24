import cv2

class Falling(Game):

    class Circle:
        def __init__(self, x, y, r):
            self.x=x
            self.y=y
            self.r=r

    def draw_circle(Circle c):
        cv2.circle(self.map.edges,CVPoint(c.x, c.y), c.r, 255)
    
    def update_game(self, keys, delta_t:int):
        if self.map is None:
            return
        pass
    
