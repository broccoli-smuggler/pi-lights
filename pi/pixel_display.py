import platform
import numpy as np


def PixelDisplay():
    pass


if platform.system() != 'Darwin':
    from display import BaseDisplay
    import neopixel
    import board
    import time
    from itertools import cycle
    import cv2


    class PixelDisplay(BaseDisplay):
        def __init__(self, diameter):
            super().__init__(diameter)

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

            # For our array we actually start with a 7 row
            print("Adjusting circle mask for small light")
            self._circle_mask[0,4] = 255
            self._circle_mask[0,10] = 255

            # Convert to an array of rgb
            mat = mat[self._circle_mask.nonzero()]

            # The wiring of the light switch means each row is reversed
            lengths = self.get_row_lengths()
            print(lengths)
            start = 0
            odd = False
            for end_row in lengths:
                end_row += start
                if odd:
                    mat[start:end_row] = np.flip(mat[start:end_row], axis=0)
                odd = not odd
                start = end_row
            return mat  

        def add_images(self, filenames: list):
            for f in filenames:
                self.add_image(f, convert=cv2.COLOR_BGR2RGB)

        def display(self):
            pixel_arrays = []
            for m in self._animation_frames:
                pixel_arrays.append(self._convert_to_pixel_array(m))

            for pixel_array in cycle(pixel_arrays):
                for (i, _) in enumerate(self.pixels):
                    self.pixels[i] = tuple(pixel_array[i])
                self.pixels.show()
                time.sleep(1)
