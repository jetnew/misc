import pyautogui
import time
from util import *
import cv2
import math
from scipy.spatial.distance import euclidean

"""
https://8ballpool.com/en/game
Left half of screen, 80%
"""


# while True:
#     print(mouse())

GAME_X1, GAME_Y1, GAME_X2, GAME_Y2 = 100//2, 450//2, 1600//2, 1440//2

def rect_height_correct(box, low, high):
    return low < euclidean(box[0], box[1]) < high or \
           low < euclidean(box[0], box[3]) < high

def rect_in_area(box, x1=275-GAME_X1, y1=745-GAME_Y1, x2=1450-GAME_X1, y2=1380-GAME_Y1):
    for point in box:
        x, y = point
        if x1 > x or x > x2:
            return False
        if y1 > y or y > y2:
            return False
    return True

def extend_line(box, length=500):
    pt1, pt2, pt3, pt4 = box
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = pt1, pt2, pt3, pt4
    d1 = euclidean(pt1, pt2)
    if x2 - x1 == 0:
        g1 = 0
    else:
        g1 = (y2-y1) / (x2-x1)
    d2 = euclidean(pt1, pt4)
    if x4 - x1 == 0:
        g2 = 0
    else:
        g2 = (y4-y1) / (x4-x1)
    if d1 > d2:
        grad = g1
        x1 -= length
        y1 -= length * grad
        x2 += length
        y2 += length * grad
        x3 += length
        y3 += length * grad
        x4 -= length
        y4 -= length * grad
    else:
        grad = g2
        x1 += length
        y1 += length * grad
        x2 += length
        y2 += length * grad
        x3 -= length
        y3 -= length * grad
        x4 -= length
        y4 -= length * grad

    return np.array([[x1, y1],
                     [x2, y2],
                     [x3, y3],
                     [x4, y4]]).astype(int)

def guideline(cont):
    boxes = []
    n = 0
    for c in cont:
        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))
        if rect_height_correct(box, 1, 5) and rect_in_area(box):
            boxes.append(box)
            n += 1
    boxes = [extend_line(box, length=1000) for box in boxes]
    return boxes

def draw_guideline(screen, boxes):
    for box in boxes:
        cv2.drawContours(screen, [box], 0, (0,0,255), 2)


import time
from PIL import ImageGrab
from mss import mss
sct = mss()
while True:
    now = time.time()
    # screen = screenshot(GAME_X1, GAME_Y1, GAME_X2, GAME_Y2)
    # screen = ImageGrab.grab(bbox=(GAME_X1, GAME_Y1, GAME_X2, GAME_Y2))
    screen = sct.grab((GAME_X1, GAME_Y1, GAME_X2, GAME_Y2))
    screen = np.array(screen)
    # screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)


    edge = edges(screen)
    cont = contours(edge)
    cont = [c for c in cont if cv2.contourArea(c) > 30]
    guidelines = guideline(cont)
    draw_guideline(screen, guidelines)

    cv2.imshow("screen", screen)
    # print("Imshow:", time.time() - now)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
