import cv2
from itertools import cycle
import numpy as np
import os


class BaseDisplay(object):
    def __init__(self, diameter):
        self.diameter = diameter
        self._animation_frames = []
        self._display_size = 200
        self._refresh_rate = 20
        self._circle_mask = self._calculate_circle_mask()
        print("Display initialised with {} pixels".format(self.get_number_pixels()))

    def _calculate_circle_mask(self):
        im = np.zeros((self._display_size*2, self._display_size*2, 3), np.uint8)
        cv2.circle(im, (self._display_size, self._display_size), self._display_size, (255, 255, 255), thickness=-1)
        mat = cv2.resize(im, (self.diameter, self.diameter), cv2.INTER_AREA)
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        mat = cv2.threshold(mat, 10, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("pixels.png", mat)
        return mat

    def get_row_lengths(self):
        return np.count_nonzero(self._circle_mask, axis=1)

    def get_number_pixels(self):
        return np.sum(self.get_row_lengths())

    def add_dir(self, dir_name, split="_"):
        names = []
        if os.path.isdir(dir_name):
            for (dirpath, _, filenames) in os.walk(dir_name):
                names = []
                for f in filenames:
                    if f.endswith("png") or f.endswith(".jpg") or f.endswith(".jpeg"):
                        order = float(f.split(split)[0])
                        names.append((order, dirpath + "/" + f))
                break
        names = sorted(names)
        names.extend(reversed(names[1:-1]))
        self.add_images(list(list(zip(*names))[1]))

    def add_images(self, filenames: list):
        for f in filenames:
            self.add_image(f)

    def add_image(self, filename, convert=None):
        if convert is not None:
            mat = cv2.imread(filename, convert)
        else:
            mat = cv2.imread(filename)
        mat = cv2.resize(mat, (self.diameter, self.diameter), cv2.INTER_AREA)
        mat = cv2.bitwise_and(mat, mat, mask=self._circle_mask)
        self._animation_frames.append(mat)

    def display(self):
        pass


class OpenCVDisplay(BaseDisplay):
    def __init__(self, radius):
        super().__init__(radius)

    def display(self):
        for m in cycle(self._animation_frames):
            cv2.imshow("pixels", m)
            cv2.waitKey(int((60/self._refresh_rate) * 100))
