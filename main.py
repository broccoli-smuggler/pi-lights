# Simple test for NeoPixels on Raspberry Pi

from display import OpenCVDisplay
from pi.pixel_display import PixelDisplay

d = PixelDisplay(8)

# d.add_image("a.jpg")
# d.add_image("wave.jpg")
d.add_images(["1.png", "2.png", "3.png", "4.png", "3.png", "2.png"])
d.display()
