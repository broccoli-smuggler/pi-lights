import cv2
from itertools import cycle
import numpy as np
import time

class OpenCVDisplay(object):
    def __init__(self, radius):
        self.radius = radius
        self._animation_frames = []
        self._display_size = 200
        self._refresh_rate = 20
        self._circle_mask = self._calculate_circle_mask()

    def _calculate_circle_mask(self):
        im = np.zeros((self._display_size*2, self._display_size*2, 3), np.uint8)
        cv2.circle(im, (self._display_size, self._display_size), self._display_size, (255, 255, 255), thickness=-1)
        mat = cv2.resize(im, (self.radius*2, self.radius*2), cv2.INTER_AREA)
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        mat = cv2.threshold(mat, 10, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("pixels.png", mat)
        return mat

    def add_images(self, filenames: list):
        for f in filenames:
            self.add_image(f)

    def add_image(self, filename):
        mat = cv2.imread(filename)
        mat = cv2.resize(mat, (self.radius*2, self.radius*2), cv2.INTER_AREA)
        mat = cv2.bitwise_and(mat, mat, mask=self._circle_mask)
        # mat = cv2.resize(mat, (self._display_size, self._display_size), cv2.INTER_NEAREST)
        self._animation_frames.append(mat)

    def load_animation(self, filename):
        cap = cv2.VideoCapture(filename)
        while cap.isOpened():
            ret, frame = cap.read()

    def display(self):
        for m in cycle(self._animation_frames):
            cv2.imshow("pixels", m)
            cv2.waitKey(int((60/self._refresh_rate) * 100))

