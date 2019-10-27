import cv2

from game.framework import CVMap
import numpy as np
from numpy import ndarray


class CVer:
    lower = 100
    higher = 200
    thres=0.9

    def do_cv(self, frame: ndarray) -> CVMap:
        frame=cv2.resize(frame,(int(frame.shape[1]/2), int(frame.shape[0]/2)))
        #frame, g, r = cv2.split(frame)
        cv2.imshow("original", frame)

        # convert to float image
        frame = np.float64(frame)
        frame *= 1.0 / 255

        # filter
        frame = cv2.GaussianBlur(frame, (3, 3), 0)

        # take sobel x and y
        sx = cv2.Sobel(frame, cv2.CV_64F, 1, 0)
        sy = cv2.Sobel(frame, cv2.CV_64F, 0, 1)

        # combine
        res = cv2.magnitude(sx, sy)

        # combine channels


        # convert back
        #res = cv2.Laplacian(frame, cv2.CV_64F)
        b,g,r=cv2.split(res)
        res=0.11*b+ 0.59*g+ 0.30*r
        #_,res = cv2.threshold(res, 0.01,255, cv2.THRESH_BINARY)

        # res=cv2.Canny(frame,100,250)

        return CVMap(res)
