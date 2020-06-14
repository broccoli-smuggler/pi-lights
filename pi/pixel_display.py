import platform


def PixelDisplay():
    pass


if platform.system() != 'Darwin':
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
            # Convert from BGR to GRB
            mat[:, :, [0, 1, 2]] = mat[:, :, [2, 0, 1]]
            return mat[self._circle_mask.nonzero()]

        def add_images(self, filenames: list):
            for f in filenames:
                self.add_image(f, convert=cv2.COLOR_BGR2RGB)

        def display(self):
            pixel_arrays = []
            for m in self._animation_frames:
                pixel_arrays.append(self._convert_to_pixel_array(m))

            for pixel_array in pixel_arrays:
                for (i, _) in enumerate(self.pixels):
                    self.pixels[i] = tuple(pixel_array[i])
                self.pixels.show()
                time.sleep(1)
