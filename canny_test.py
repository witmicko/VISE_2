import cv2
import numpy as np
from matplotlib import pyplot as plt




def nothing(x):
    pass

# Create a black image, a window
img = cv2.imread('templates/abs_1.png')
old_L=100
old_H=200
canny = cv2.Canny(img, old_L, old_H)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('L','image',100,500,nothing)
cv2.createTrackbar('H','image',200,500,nothing)
# switch = '0 : OFF \n1 : ON'
# cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',canny)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    # old_L
    # old_H
    # get current positions of four trackbars
    L = cv2.getTrackbarPos('L','image')
    H = cv2.getTrackbarPos('H','image')
    if L != old_L or H != old_H:
        canny = cv2.Canny(img, L, H)
        old_L = L
        old_H = H

cv2.destroyAllWindows()