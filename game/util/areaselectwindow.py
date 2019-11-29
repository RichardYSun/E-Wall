import cv2


class AreaSelectWindow:

    def __init__(self, w, h, name, color, thickness=1, click=10):
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

        self.down = False

        self.t = 0
        self.l = 0
        self.r = w
        self.b = h-400
        self.w = w
        self.h = h

        self.name = name
        self.color = color
        self.click = click
        self.range = range
        self.thickness = thickness
        self.sel = [False] * 4

        cv2.setMouseCallback(name, self.on_click)

    def on_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if abs(x - self.l) <= self.click:
                self.sel[0] = True
            if abs(x - self.r) <= self.click:
                self.sel[1] = True
            if abs(y - self.t) <= self.click:
                self.sel[2] = True
            if abs(y - self.b) <= self.click:
                self.sel[3] = True

        if event == cv2.EVENT_LBUTTONUP:
            self.sel = [False] * 4

        if self.sel[0]:
            self.l = max(0, min(x, self.r-10))
        if self.sel[1]:
            self.r = min(self.w, max(x, self.l+10))
        if self.sel[2]:
            self.t = max(0, min(y, self.b-10))
        if self.sel[3]:
            self.b = min(self.h, max(y, self.t+10))

    def get_sub_image(self, img):
        return img[self.t:self.b, self.l:self.r]

    def show(self, bg):
        cv2.rectangle(bg, (self.l - self.thickness, self.t - self.thickness),
                      (self.r + self.thickness, self.b + self.thickness), self.color, self.thickness)
        cv2.imshow(self.name, bg)

    def __del__(self):
        cv2.destroyWindow(self.name)
