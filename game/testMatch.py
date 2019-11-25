import numpy as np
import cv2
from matplotlib import pyplot as plt

from game.img.images import imread

MATCH_CNT = 10


def match(img: np.ndarray, fnd: np.ndarray):
    sift = cv2.SIFT()

    kp1, des1 = sift.detectAndCompute(img, None)
    kp2, des2 = sift.detectAndCompute(fnd, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict(checks=50)

    matches = cv2.FlannBasedMatcher(index_params, search_params).knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > MATCH_CNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h, w = fnd.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        img2 = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    else:
        print
        "Not enough matches are found - %d/%d" % (len(good), MATCH_CNT)
        matchesMask = None

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)

    img3 = cv2.drawMatches(fnd, kp1, img, kp2, good, None, **draw_params)

    plt.imshow(img3, 'gray'), plt.show()


img = imread('testmatch.png')
fnd = imread('ree/jump1.png')
match(img, fnd)
