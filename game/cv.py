import cv2

from game.framework import CVMap
import numpy as np
from numpy import ndarray

from game.util.ParamWindow import ParamWindow

canny = 0
laplacian = 1
sobel = 2

bgr = 0
hsv = 1


class CVer:

    def __init__(self):
        self.prev = None
        self.lsd = cv2.ximgproc.createFastLineDetector()
        self.params = ParamWindow('cv params')

    def do_cv(self, frame: ndarray) -> CVMap:
        algorithm = self.params.get_param('algorithm', 2, 1)

        color_space = self.params.get_param('color space', 1, 0)
        if color_space == hsv:
            cv2.cvtColor(frame, cv2.COLOR_BGR2HSV, dst=frame)

        # filter
        blur_radius = self.params.get_param('blur radius', 3, 3)
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
            bc = self.params.get_param('b(h)', 255, 28)
            gc = self.params.get_param('g(s)', 255, 151)
            rc = self.params.get_param('r(v)', 255, 76)
            res = bc * b + gc * g + rc * r
            # sobel_thres = self.params.get_param('sobel thres', 100, 80) / 1000.0
            # _, res = cv2.threshold(res, sobel_thres, 255, cv2.THRESH_BINARY)

            res = res.astype(np.uint8)
        else:
            canny_lower = self.params.get_param('canny lower', 255, 100)
            canny_higher = self.params.get_param('canny higher', 255, 200)
            res = cv2.Canny(frame, canny_lower, canny_higher)

        # detect lines
        lines = self.lsd.detect(res)
        if lines is not None:
            lines_conv = []
            for line in lines:
                line = line[0]
                lines_conv.append(line)
        else:
            lines_conv = None

        mp = CVMap()
        mp.edges = res
        mp.lines = lines
        mp.lines_conv = lines_conv
        mp.lsd = self.lsd
        return mp

# stupid optical flow stuff thats too slow

# frame=cv2.resize(frame,(int(frame.shape[1]/1), int(frame.shape[0]/1)))
# frame, g, r = cv2.split(frame)

# get optical flow
# kst=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# kst=kst.astype(np.uint8)
# if self.prev is None:
#     self.prev=kst
# flow=cv2.calcOpticalFlowFarneback(self.prev,kst,None,pyr_scale=0.5,
#                                   levels=1, winsize=5,iterations=1,
#                                   poly_n=5,poly_sigma=1.1,flags=0)
# mag = cv2.magnitude(flow[..., 0], flow[..., 1])
# _,mag=cv2.threshold(mag,5,255,cv2.THRESH_BINARY)

# cv2.imshow('movement', mag)
# self.prev=kst
