import cv2

from game.framework import CVMap
import numpy as np
from numpy import ndarray


class CVer:
    def __init__(self):
        self.canny_lower=100
        self.canny_higher=200
        self.sobel_thres=0.08
        self.prev=None

    def do_cv(self, frame: ndarray) -> CVMap:
        #frame=cv2.resize(frame,(int(frame.shape[1]/1), int(frame.shape[0]/1)))
        #frame, g, r = cv2.split(frame)

        #get optical flow
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
