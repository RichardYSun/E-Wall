import cv2

from game.cv import CVer


def test(G):
    cap = cv2.VideoCapture(0)

    cver = CVer()

    ret, frame = cap.read()
    mp = cver.do_cv(frame)

    game = G(mp)

    while True:
        ret, frame = cap.read()

        mp = cver.do_cv(frame)
        game.update_map(mp)
        game.update_game([], 0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
