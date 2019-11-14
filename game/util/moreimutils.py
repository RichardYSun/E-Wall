import os
import cv2

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def imread(file, mode=cv2.IMREAD_COLOR, size=None):
    res = cv2.imread(ROOT_DIR + "\\..\\img\\" + file, mode)
    if res is None:
        raise Exception('Could not load image ' + ROOT_DIR + "\\..\\img\\" + file)
    if size is not None:
        res = cv2.resize(res, size)
    return res
