import cv2

from game.game import GameContext
import numpy as np
from numpy import ndarray

from game.util import ParamWindow
from game.util.vector2 import Vector2
from game.util.line import Line

# algorithm
canny = 0
laplacian = 1
sobel = 2

# color space
bgr = 0
hsv = 1

# thresholding
thres_none = 0
thres = 1
thres_gaussian = 2


class CVer:

    def __init__(self):
        self.prev = None
        self.lsd = cv2.ximgproc.createFastLineDetector()

    def do_cv(self, mp: GameContext):
        frame = mp.cam_img
        algorithm = ParamWindow.get_int('algorithm', 2, 2)

        color_space = ParamWindow.get_int('color space', 1, 0)
        if color_space == hsv:
            cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, dst=frame)

        # filter
        blur_radius = ParamWindow.get_int('blur radius', 3, 3) * 2 + 1
        if blur_radius > 2:
            cv2.GaussianBlur(frame, (blur_radius, blur_radius), 0, dst=frame)

        if algorithm == sobel or algorithm == laplacian:

            # convert to float image
            frame = np.float64(frame)
            frame /= 255.0

            if algorithm == sobel:
                # take sobel x and y
                sy = cv2.Sobel(frame, cv2.CV_64F, 0, 1)
                sx = cv2.Sobel(frame, cv2.CV_64F, 1, 0)

                # combine x and y
                res = cv2.magnitude(sx, sy)

            else:
                res = cv2.Laplacian(frame, cv2.CV_64F, dst=frame)

            b, g, r = cv2.split(res)
            # combine channels
            bc = ParamWindow.get_int('b(h)', 255, 28)
            gc = ParamWindow.get_int('g(s)', 255, 151)
            rc = ParamWindow.get_int('r(v)', 255, 76)
            res = bc * b + gc * g + rc * r

            thresholding = ParamWindow.get_int('thresholding', 2, 1)
            if thresholding == thres_none:
                res = res.astype(np.uint8)
            elif thresholding == thres:
                thres_val = ParamWindow.get_int('threshold value', 255, 30)
                cv2.threshold(res, thres_val, 255, cv2.THRESH_BINARY, dst=res)
                res = res.astype(np.uint8)
            elif thresholding == thres_gaussian:
                block_size = ParamWindow.get_int('threshold block size', 5, 5) * 2 + 3
                C = ParamWindow.get_int('threshold C', 11, 2) - 11
                res = res.astype(np.uint8)
                cv2.adaptiveThreshold(res, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C,
                                      dst=res)

            if thresholding != thres_none:
                use_morph = ParamWindow.get_int('use morph', 1, 0)
                if use_morph == 1:
                    pass

        else:
            canny_lower = ParamWindow.get_int('canny lower', 255, 100)
            canny_higher = ParamWindow.get_int('canny higher', 255, 200)
            res = cv2.Canny(frame, canny_lower, canny_higher)

        # detect lines
        do_lsd = ParamWindow.get_int('do lsd', 1, 0)
        if do_lsd == 1:
            lines = self.lsd.detect(res)
            if lines is not None:
                lines_conv = []

                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    lines_conv.append(Line(Vector2(x1, y1), Vector2(x2, y2)))
            else:
                lines_conv = []
        else:
            lines = None
            lines_conv = []

        mp.edges = res
        mp.lines = lines
        mp.lines_conv = lines_conv
        mp.lsd = self.lsd

        # removes noise
        max_sz = ParamWindow.get_int('noise', 11, 3) | 1
        it = ParamWindow.get_int('it', 5, 0)
        if it>0:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (max_sz, max_sz))
            mp.edges = cv2.morphologyEx(mp.edges, cv2.MORPH_OPEN, kernel, iterations=it)
