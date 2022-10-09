import pyautogui
import cv2
import numpy as np
import platform

if platform.system() == "Darwin":
    OS = "MAC"
else:
    OS = "ANY"

def mouse():
    x, y = pyautogui.position()
    if OS == "MAC":
        x *= 2
        y *= 2
    return x, y

def screenshot(x1=None, y1=None, x2=None, y2=None):
    screen = pyautogui.screenshot() if x1 is None else pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
    return cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)

def edges(screen: np.array):
    threshold1 = 100
    threshold2 = 180
    apertureSize = 3
    return cv2.Canny(screen, threshold1, threshold2, apertureSize)

def display(screen):
    cv2.imshow("", screen)
    cv2.waitKey(0)

def match_element(screen, element):
    screen = edges(screen)
    element = cv2.cvtColor(element, cv2.COLOR_BGR2GRAY)
    element = cv2.Canny(element, 50, 200)
    tH, tW = element.shape[:2]
    result = cv2.matchTemplate(screen, element, cv2.TM_CCOEFF_NORMED)
    (_, score, _, xy) = cv2.minMaxLoc(result)
    return xy[0], xy[1], xy[0] + tW, xy[1] + tH, score

def display_bounding_box(screen, x1, y1, x2, y2):
    cv2.rectangle(screen, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imshow("", screen)
    cv2.waitKey(0)

def contours(edge: np.array):
    """
    :param edge: array of edges from canny edge
    :return: (contours, hierarchy)

    Notes:
        hierarchy[i][0] - next contour at same hierarchy
        hierarchy[i][1] - previous contour at same hierarchy
        hierarchy[i][2] - first child contour
        hierarchy[i][3] - first parent contour

        Value is negative if no such contour
    """
    mode = cv2.RETR_LIST
    method = cv2.CHAIN_APPROX_SIMPLE
    contours, hierarchy = cv2.findContours(edge, mode, method)
    return contours

def display_contours(screen, contours):
    for cont in contours:
        x1, y1, x2, y2 = contour_bounding_box(cont)
        cv2.rectangle(screen, (x1, y1), (x2, y2), (0, 0, 255), 2)
    print("No. of contours:", len(contours))
    cv2.imshow("Contours", screen)
    cv2.waitKey(0)

def contour_bounding_box(contour):
    rect = cv2.minAreaRect(contour)
    box = np.int0(cv2.boxPoints(rect))
    x1, y1 = min(box[:, 0]), min(box[:, 1])
    x2, y2 = max(box[:, 0]), max(box[:, 1])
    return x1, y1, x2, y2

def contour_big_enough(contour, min_area=300):
    return cv2.contourArea(contour) > min_area


def circles(screen):
    gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT_ALT,
                               dp=1,  # inverse ratio of accumulator res to image res
                               minDist=5,
                               param1=200,
                               param2=0.8,
                               minRadius=0)  # min dist btw centers of circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)

        for x, y, r in circles:
            cv2.circle(screen, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(screen, (x-5, y-5), (x+5, y+5), (0, 128, 255), -1)

    cv2.imshow("screen", screen)
    cv2.waitKey(0)
    return circles