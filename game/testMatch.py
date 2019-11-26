import time
import numpy as np
import cv2
from matplotlib import pyplot as plt

from img.images import imread

MATCH_CNT = 10


def match(fnd: np.ndarray, img: np.ndarray):
    orb = cv2.ORB_create(nfeatures=500)

    kp1 = orb.detect(fnd, None)
    kp1, des1 = orb.compute(fnd, kp1)
    kp2 = orb.detect(img, None)
    kp2, des2 = orb.compute(img, kp2)

    # plt.imshow(cv2.drawKeypoints(img, kp2, None, color=(255, 0, 0), flags=0))
    # # plt.imshow(cv2.drawKeypoints(fnd, kp1, None, color=(255, 0, 0), flags=0))
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

    draw_mask = [0] * len(good)

    while len(good) - sum(draw_mask) > MATCH_CNT:
        print('loop')
        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in [good[i] for i in range(len(good)) if not draw_mask[i]]]).reshape(
            -1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in [good[i] for i in range(len(good)) if not draw_mask[i]]]).reshape(
            -1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        j = 0
        for i in range(len(good)):
            if not draw_mask[i]:
                draw_mask[i] |= matchesMask[j]
                j += 1

        h, w, d = fnd.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        img = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=draw_mask,  # draw only inliers
                       flags=2)

    img3 = cv2.drawMatches(fnd, kp1, img, kp2, good, None, **draw_params)
    plt.imshow(img3, 'gray'), plt.show()


img = imread('test/smallguy.jpg')
fnd = imread('test/guy.jpg')
match(fnd, img)
