import time
import numpy as np
import cv2
from matplotlib import pyplot as plt
from game.img.images import imread
from game.util import ParamWindow


class Matcher:
    MATCH_CNT = 10

    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=self.MATCH_CNT * 50)

        # Source images that have already had their keypoints calculated
        self.objs = {}

        self.camera_img = None

    def update_img(self, img):
        self.camera_img = img
        kp2 = self.orb.detect(img, None)
        self.kp2, self.des2 = self.orb.compute(img, kp2)

    # takes in an image and returns all instances of the image in the camera image
    def match_obj(self, fnd: np.ndarray):
        img = self.camera_img

        if id(fnd) in self.objs:
            kp1, des1 = self.objs[fnd]
        else:
            kp1 = self.orb.detect(fnd, None)
            kp1, des1 = self.orb.compute(fnd, kp1)
            self.objs[id(fnd)] = (kp1, des1)

        kp2, des2 = self.kp2, self.des2

        index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
        search_params = dict(checks=100)

        matches = cv2.FlannBasedMatcher(index_params, search_params).knnMatch(des1, des2, k=5)

        good = []
        for k in matches:
            if len(k) > 1 and k[0].distance < 0.7 * k[1].distance:
                good.append(k[0])

        matched = [0] * len(good)

        matches = []

        while len(good) - sum(matched) > self.MATCH_CNT:
            print(len(good) - sum(matched))
            src_pts = np.float32(
                [kp1[m.queryIdx].pt for m in [good[i] for i in range(len(good)) if not draw_mask[i]]]).reshape(
                -1, 1, 2)
            dst_pts = np.float32(
                [kp2[m.trainIdx].pt for m in [good[i] for i in range(len(good)) if not draw_mask[i]]]).reshape(
                -1, 1, 2)
            match, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matches_mask = mask.ravel().tolist()

            matches.append([np.int32(match)])

        return matches


# matcher = Matcher()
# matcher.update_img(imread('test/smallguy.jpg'))
# matcher.match_obj(imread('test/guy.jpg'))
