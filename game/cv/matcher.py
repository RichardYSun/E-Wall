import time
from typing import Callable, Any, List, Tuple

import numpy as np
import cv2

from game.game import GameContext
from game.util import ParamWindow

PosUpdate = Callable[[np.ndarray, List[Tuple[float, float]]], None]


class MatchObj:
    def __init__(self):
        self.img: np.ndarray = None
        self.on_appear: PosUpdate = None
        self.on_move: PosUpdate = None
        self.kp: np.ndarray = None
        self.des: np.ndarray = None
        self.original_rect = None
        self.matched_rect = None
        self.appeared = False


class Matcher:
    MATCH_CNT = 10

    def __init__(self):
        self.orb: cv2.ORB = cv2.ORB_create(nfeatures=self.MATCH_CNT * 5000)

        # Source images that have already had their keypoints calculated
        self.objects: List[MatchObj] = []

        self.camera_img: np.ndarray = None
        self.cam_kp: np.ndarray = None
        self.cam_des: np.ndarray = None

    def add_obj(self, img: np.ndarray, on_appear: PosUpdate, on_move: PosUpdate):
        obj = MatchObj()
        obj.img = img
        obj.on_appear = on_appear
        obj.on_move = on_move
        obj.kp, obj.des = self.orb.detectAndCompute(img, None)
        h, w = img.shape[0:2]
        obj.original_rect = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        self.objects.append(obj)

    def update_map(self, mp: GameContext):
        img = mp.original_img
        self.camera_img = img
        kp2 = self.orb.detect(img, None)
        self.cam_kp, self.cam_des = self.orb.compute(img, kp2)

        for obj in self.objects:
            M = self.match_obj(obj)
            if M is None or len(M) == 0:
                pass
            else:
                nr = cv2.perspectiveTransform(obj.original_rect, M[0])
                r = []
                for a in nr:
                    x, y = a[0][0], a[0][1]
                    r.append((x * mp.downscale, y * mp.downscale))

                if obj.appeared:
                    obj.on_move(M, r)
                else:
                    obj.on_appear(M, r)

    # takes in an image and returns all instances of the image in the camera image
    def match_obj(self, obj: MatchObj):

        kp2, des2 = self.cam_kp, self.cam_des

        fnd = obj.img
        kp1, des1 = obj.kp, obj.des

        # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # matches = bf.match(des1, des2)
        # matches = sorted(matches, key=lambda x: x.distance)
        #
        # good = matches

        # bf
        # good = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(des1, des2)
        # bf_max=ParamWindow.get_int('bf max points', 10000, 100)
        # good = sorted(good, key=lambda x: x.distance)[:min(bf_max, len(good))]

        # flann
        index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
        search_params = dict(checks=500)
        matches = cv2.FlannBasedMatcher(index_params, search_params).knnMatch(des1, des2, k=2)

        good = []
        ratio_test = ParamWindow.get_int('ratio test', 100, 80) / 100.0
        for k in matches:
            if len(k) > 1 and k[0].distance <= ratio_test * k[1].distance:
                good.append(k[0])

        # debugging stuff
        show_debug = ParamWindow.get_int('debug matcher', 1, 1)
        if show_debug:
            draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                               singlePointColor=None,
                               matchesMask=[1] * len(good),  # draw only inliers
                               flags=2)
            cam_img = cv2.drawKeypoints(self.camera_img.copy(), kp2, None, color=(255, 0, 0), flags=0)
            obj_img = cv2.drawKeypoints(fnd.copy(), kp1, None, color=(255, 0, 0), flags=0)
            img3 = cv2.drawMatches(obj_img, kp1, cam_img, kp2, good, None, **draw_params)
            cv2.imshow('matches', img3)

        ret = []

        if len(good) > self.MATCH_CNT:
            src_pts = np.float32(
                [kp1[m.queryIdx].pt for m in good]).reshape(
                -1, 1, 2)
            dst_pts = np.float32(
                [kp2[m.trainIdx].pt for m in good]).reshape(
                -1, 1, 2)

            match = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)[0]
            ret.append(match)

        return ret
