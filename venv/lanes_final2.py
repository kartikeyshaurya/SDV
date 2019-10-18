import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)

grayscale = cv2.cvtColor(lane_image, cv2.COLOR_RGB2BGR)
smoothing = cv2.GaussianBlur(grayscale, (5, 5), 0)
canny = cv2.Canny(smoothing, 50, 150)


def region_of_interest(image):
    height = image.shape[0]
    polygon = np.array([[(100, height), (850, height), (550, 100)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


cropped_image = region_of_interest(canny)

# finding lane lines in image
lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array(0), minLineLength=40, maxLineGap=5)


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            return line_image
def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1,x2), (y1,y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0: # y is reversed in image
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    # add more weight to longer lines
    left_fit_average  = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line  = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)
    averaged_lines = [left_line, right_line]
    return averaged_lines

line_image = display_lines(lane_image, lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
plt.imshow(canny)
plt.show()
cv2.imshow('result', combo_image)
cv2.waitKey(0)
