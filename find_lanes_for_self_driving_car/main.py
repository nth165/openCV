import cv2 as cv
import numpy as np

def Canny(_img):
    gray = cv.cvtColor(_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    canny = cv.Canny(blur, 50, 150)
    return canny

def region_of_interest(_img):
    height = _img.shape[0]
    triangle = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(_img)
    cv.fillPoly(mask, triangle, 255)
    return mask

img = cv.imread("./images/test_image.jpg")
lane_img = np.copy(img)
canny = Canny(lane_img)

cv.imshow("images", region_of_interest(canny))
cv.waitKey(0)
