from display import BaseDisplay
import neopixel
import board
import time
import numpy as np
from itertools import cycle
import cv2


class PixelDisplay(BaseDisplay):
    def __init__(self, radius):
        super().__init__(radius)

        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = board.D18

        # The number of NeoPixels
        num_pixels = self.get_number_pixels()

        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.ORDER = neopixel.GRB

        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=0.4, auto_write=False, pixel_order=self.ORDER
        )
        self.pixels.fill(0)
        self.pixels.show()
        time.sleep(0.5)

    def _convert_to_pixel_array(self, mat):
        return mat[self._circle_mask.nonzero()]

    def add_images(self, filenames: list):
        for f in filenames:
            self.add_image(f, convert=cv2.COLOR_BGR2RGB)

    def display(self):
        for m in cycle(self._animation_frames):
            pixel_array = self._convert_to_pixel_array(m)
            for i in enumerate(self.pixels):
                print()
                self.pixels[i] = tuple(pixel_array[i])
            self.pixels.show()
            time.sleep(1)
