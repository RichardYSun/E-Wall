import cv2

from game.framework import CVMap
import numpy as np
from numpy import ndarray


class CVer:
    def __init__(self):
        self.lower=100
        self.higher=200
        self.sobel_thres=0.8

    def do_cv(self, frame: ndarray) -> CVMap:
        frame=cv2.resize(frame,(int(frame.shape[1]/1), int(frame.shape[0]/1)))
        #frame, g, r = cv2.split(frame)

        # convert to float image
        frame = np.float64(frame)
        frame *= 1.0 / 255

        # filter
        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # take sobel x and y
        sx = cv2.Sobel(frame, cv2.CV_64F, 1, 0)
        sy = cv2.Sobel(frame, cv2.CV_64F, 0, 1)

        # combine
        res = cv2.magnitude(sx, sy)

        # combine channels


        # convert back
        # res = cv2.Laplacian(frame, cv2.CV_64F)
        b,g,r=cv2.split(res)
        res=0.11*b+ 0.59*g+ 0.30*r
        _,res = cv2.threshold(res, self.sobel_thres,255, cv2.THRESH_BINARY)

        # res=cv2.Canny(frame,70,200)

        return CVMap(res)
