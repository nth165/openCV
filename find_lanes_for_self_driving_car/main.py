import cv2 as cv

img = cv.imread("./images/test_image.jpg")
cv.imshow("images", img)

cv.waitKey(0)
