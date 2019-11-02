import cv2

win_name = 'parameters'

created = set()

win_name = win_name
cv2.namedWindow(win_name, cv2.WINDOW_GUI_NORMAL)


def nothing(_):
    pass


def get_int(name, max_val=255, default_val=0):
    if name not in created:
        cv2.createTrackbar(name, win_name, default_val, max_val, nothing)
        created.add(name)
    return cv2.getTrackbarPos(name, win_name)
