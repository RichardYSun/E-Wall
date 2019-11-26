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
            kp1, des1 = self.objs[id(fnd)]
        else:
            kp1 = self.orb.detect(fnd, None)
            kp1, des1 = self.orb.compute(fnd, kp1)
            self.objs[id(fnd)] = (kp1, des1)

        kp2, des2 = self.kp2, self.des2

        # plt.imshow(cv2.drawKeypoints(img, kp2, None, color=(255, 0, 0), flags=0))
        # plt.imshow(cv2.drawKeypoints(fnd, kp1, None, color=(255, 0, 0), flags=0))
        # plt.show()
        # return

        index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
        search_params = dict(checks=100)

        matches = cv2.FlannBasedMatcher(index_params, search_params).knnMatch(des1, des2, k=5)

        good = []
        for k in matches:
            if len(k) > 1 and k[0].distance < 0.7 * k[1].distance:
                good.append(k[0])

        # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
        #                    singlePointColor=None,
        #                    matchesMask=[1] * len(good),  # draw only inliers
        #                    flags=2)
        # img3 = cv2.drawMatches(fnd, kp1, img, kp2, good, None, **draw_params)
        #
        # plt.imshow(img3), plt.show()
        # return

        found = [0] * len(good)

        matches = []

        while len(good) - sum(found) > self.MATCH_CNT:
            print(len(good) - sum(found))
            src_pts = np.float32(
                [kp1[m.queryIdx].pt for m in [good[i] for i in range(len(good)) if not found[i]]]).reshape(
                -1, 1, 2)
            dst_pts = np.float32(
                [kp2[m.trainIdx].pt for m in [good[i] for i in range(len(good)) if not found[i]]]).reshape(
                -1, 1, 2)

            match, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matches_mask = mask.ravel().tolist()
            j = 0
            for i in range(len(good)):
                if not found[i]:
                    found[i] |= matches_mask[j]
                    j += 1

            # h, w, d = fnd.shape
            # pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            # dst = cv2.perspectiveTransform(pts, match)
            # mg = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

            matches.append(match)

        # draw_params = dict(matchColor=(0, 255, 0),
        #                    singlePointColor=None,
        #                    matchesMask=found,
        #                    flags=2)
        #
        # img3 = cv2.drawMatches(fnd, kp1, img, kp2, good, None, **draw_params)
        # plt.imshow(img3, 'gray'), plt.show()

        return matches


# matcher = Matcher()
# matcher.update_img(imread('test/smallguy.jpg'))
# matcher.match_obj(imread('test/guy.jpg'))
