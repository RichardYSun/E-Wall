import cv2


class ParamWindow():
    created = set()

    def __init__(self, win_name):
        self.win_name = win_name
        cv2.namedWindow(self.win_name)

    def nothing(self,_):
        pass

    def get_param(self, name, max_val=255, default_val=0):
        if name not in self.created:
            cv2.createTrackbar(name, self.win_name, default_val,max_val, self.nothing)
            self.created.add( name)
        return cv2.getTrackbarPos(name, self.win_name)
