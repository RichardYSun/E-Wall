import numpy as np
import cv2


def k(x):
    pass

cap = cv2.VideoCapture(0)
controls, lower, higher = 'controls', 'lower', 'higher'
cv2.namedWindow(controls)
cv2.createTrackbar(lower, controls, 0, 255, k)
cv2.createTrackbar(higher, controls, 0, 255, k)

# Capture frame-by-frame
# ret, frame = cap.read()
frame = cv2.imread('test.png')

# Our operations on the frame come here
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

edge = cv2.Canny(frame, cv2.getTrackbarPos(lower, controls), cv2.getTrackbarPos(higher, controls))

# Display the resulting frame
cv2.imshow('frame', edge)

print(edge)
