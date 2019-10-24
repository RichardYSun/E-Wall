import os

import cv2

from game.cv import CVer
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR + '/test.png')
tmp = cv2.imread(ROOT_DIR + '/test.png')

def test(G, still=True):
    def getImg():
        if not still:
            ret, frame = cap.read()
            return frame
        else:
            return tmp

    cap = cv2.VideoCapture(0)

    cver = CVer()
    mp = cver.do_cv(getImg())
    game = G(mp)

    while True:

        mp = cver.do_cv(getImg())
        game.update_map(mp)
        game.update_game([], 0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
