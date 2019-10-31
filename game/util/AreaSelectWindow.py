import cv2


class AreaSelectWindow:
    down=False

    def __init__(self, w, h, name, color, thickness=1, click=10):
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

        self.t = 0
        self.l = 0
        self.r = w
        self.b = h

        self.name = name
        self.color = color
        self.click = click
        self.range = range
        self.thickness = thickness

        cv2.setMouseCallback(name, self.on_click)

    def on_click(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.down=True

        if event==cv2.EVENT_LBUTTONUP:
            self.down=False

        if self.down:
            if abs(x - self.l) <= self.click:
                self.l = min(x, self.r)
            if abs(x - self.r) <= self.click:
                self.r = max(x, self.l)
            if abs(y - self.t) <= self.click:
                self.t = min(y, self.b)
            if abs(y - self.b) <= self.click:
                self.b = max(y, self.t)

    def get_sub_image(self, img):
        return img[self.t:self.b, self.l:self.r]

    def show(self, bg):
        cv2.rectangle(bg,   (self.l-self.thickness, self.t-self.thickness),
                      (self.r+self.thickness, self.b+self.thickness),self.color, self.thickness)
        cv2.imshow(self.name, bg)

    def __del__(self):
        cv2.destroyWindow(self.name)
