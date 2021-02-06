import cv2 as cv
import numpy as np

def make_coordinates(_img, _line_parameters):
    slope, intercept = _line_parameters
    y1 = _img.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1, x2, y2])

def average_slope_intercept(_img, _lines):
    left_fit = []
    right_fit = []
    for line in _lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    
    left_line = make_coordinates(_img, left_fit_average)
    right_line = make_coordinates(_img, right_fit_average)

    return np.array([left_line,right_line ])


def Canny(_img):
    gray = cv.cvtColor(_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    canny = cv.Canny(blur, 50, 150)
    return canny

def display_lines(_img, _lines):
    line_image = np.zeros_like(_img)
    if _lines is not None:
        for  x1,y1,x2,y2 in _lines:
            cv.line(line_image, (x1, y1), (x2,y2), (0,255,0), 10)
    return line_image

def region_of_interest(_img):
    height = _img.shape[0]
    triangle = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(_img)
    cv.fillPoly(mask, triangle, 255)
    masked_image = cv.bitwise_and(_img, mask)
    return masked_image

# img = cv.imread("./videos/test2.mp4")
# lane_img = np.copy(img)
# canny_image = Canny(lane_img)
# cropped_image = region_of_interest(canny_image)
# lines = cv.HoughLinesP(cropped_image,2,np.pi/180,100, np.array([]), minLineLength=40, maxLineGap=5)
# averaged_line = average_slope_intercept(lane_img, lines)
# line_image = display_lines(lane_img, averaged_line)
# combo_image = cv.addWeighted(lane_img, 0.8, line_image, 1, 1)
# cv.imshow("images",combo_image)
# cv.waitKey(0)

cap = cv.VideoCapture("./videos/test.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = Canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv.HoughLinesP(cropped_image,2,np.pi/180,100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_line = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_line)
    combo_image = cv.addWeighted(frame, 0.8, line_image, 1, 1)
    cv.imshow("images", combo_image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break;

cap.release();
cv.destroyAllWindows();