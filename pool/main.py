import pyautogui
import time
from util import *
import cv2
import math
from scipy.spatial.distance import euclidean
from mss import mss

"""
https://8ballpool.com/en/game
Left half of screen, 80%
"""

# while True:
#     print(mouse())

def extend_line(box, length=500):
    pt1, pt2, pt3, pt4 = box
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = pt1, pt2, pt3, pt4
    d1 = euclidean(pt1, pt2)
    if x2 - x1 == 0:
        g1 = 9999
    else:
        g1 = (y2-y1) / (x2-x1)
    d2 = euclidean(pt1, pt4)
    if x4 - x1 == 0:
        g2 = 9999
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

# while True:
#     print(mouse())
class Game:
    def __init__(self):
        self.screen_coord = {
            'top': 450//2,
            'left': 100//2,
            'width': 1500//2,
            'height': 990//2,
        }
        self.table_coord = {
            'left': 315 - self.screen_coord['left'] * 2,
            'right': 1415 - self.screen_coord['left'] * 2,
            'top': 780 - self.screen_coord['top'] * 2,
            'bottom': 1350 - self.screen_coord['top'] * 2
        }
        self.sct = mss()
    def get_edges(self):
        return cv2.Canny(self.screen, threshold1=100, threshold2=180, apertureSize=3)
    def get_contours(self):
        contours, hierarchy = cv2.findContours(self.edges, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        return contours
    def get_boxes(self, shapes):
        boxes = []
        for shape in shapes:
            rectangle = cv2.minAreaRect(shape)
            points = np.rint(cv2.boxPoints(rectangle)).astype(int)
            boxes.append(points)
        return boxes
    def get_centers(self, boxes):
        centers = []
        for box in boxes:
            y = box[2][1] - (box[2][1] - box[0][1]) // 2
            x = box[2][0] - (box[2][0] - box[0][0]) // 2
            centers.append((int(y), int(x)))
        return centers

    def info(self):
        self.screen = np.array(self.sct.grab(self.screen_coord))
        self.rgb = cv2.cvtColor(self.screen, cv2.COLOR_BGR2RGB)
        self.gray = cv2.cvtColor(self.screen, cv2.COLOR_BGR2GRAY)
        self.edges = self.get_edges()
        self.contours = self.get_contours()
        self.guidelines = self.get_guidelines()
        self.balls = self.get_balls()
        self.walls = self.get_walls()
        self.predictions = self.get_predictions()
    def get_guidelines(self):
        contours = [c for c in self.contours if cv2.contourArea(c) > 30]
        boxes = self.get_boxes(contours)
        boxes = [b for b in boxes if euclidean(b[0], b[1]) < 5 or euclidean(b[0], b[3]) < 5]

        centers = self.get_centers(boxes)
        is_white = lambda color: sum(color) > 255 * 3 - 10
        guidelines = [box for center, box in zip(centers, boxes) if is_white(self.rgb[center])]
        return guidelines
    def draw_guidelines(self):
        boxes = [extend_line(guideline, length=1000) for guideline in self.guidelines]
        for box in boxes:
            cv2.drawContours(self.screen, [box], 0, (0,0,255), 1)
    def get_balls(self):
        balls = cv2.HoughCircles(self.gray,
                                   cv2.HOUGH_GRADIENT_ALT,
                                   dp=1,  # inverse ratio of accumulator res to image res
                                   minDist=5,
                                   param1=200,
                                   param2=0.8,
                                   minRadius=8,
                                   maxRadius=17)  # min dist btw centers of circles
        balls = balls[0] if balls is not None else []
        is_playable = lambda ball: self.table_coord['left'] < ball[0] < self.table_coord['right'] \
            and self.table_coord['top'] < ball[1] < self.table_coord['bottom']
        balls = [ball for ball in balls if is_playable(ball)]
        return balls
    def draw_balls(self):
        for x, y, r in self.balls:
            x, y, r = int(x), int(y), int(r)
            cv2.circle(self.screen, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(self.screen, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    def get_predictions(self):
        predictions = []
        for i1, ball1 in enumerate(self.balls):
            for i2, ball2 in enumerate(self.balls):
                if i1 != i2:
                    x1, y1, r1 = ball1
                    x2, y2, r2 = ball2
                    if euclidean((x1, y1), (x2, y2)) < r1 + r2 + 5:
                        center = ((x1 + x2) / 2, (y1 + y2) / 2)
                        gradient = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else 9999
                        predictions.append((center, gradient))
        return predictions
    def draw_predictions(self):
        for (x, y), gradient in self.predictions:
            point1 = (int(x - 1000), int(y - gradient * 1000))
            point2 = (int(x + 1000), int(y + gradient * 1000))
            cv2.line(self.screen, point1, point2, (0,255,0), 1)
    def get_walls(self):
        return
    def run(self):
        while True:
            self.info()
            self.draw_guidelines()
            self.draw_balls()
            self.draw_predictions()

            cv2.imshow("screen", self.screen)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break

game = Game()
game.run()

