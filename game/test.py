import os

import cv2
import time

from game.cv import CVer

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR + '/test.png')
tmp = cv2.imread(ROOT_DIR + '/test2.bmp')


def test(G, still=True):
    def get_img():
        if not still:
            ret, frame = cap.read()
            return frame
        else:
            return tmp

    cap = cv2.VideoCapture(0)

    cver = CVer()
    mp = cver.do_cv(get_img())
    game = G(mp)
    last_time = time.time()

    while True:
        mp = cver.do_cv(get_img())
        game.update_map(mp)
        t = time.time()
        img = game.update_game([], t - last_time)
        last_time = t
        cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
