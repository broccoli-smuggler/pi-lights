# Simple test for NeoPixels on Raspberry Pi

from display import OpenCVDisplay
from pi.pixel_display import PixelDisplay

d = PixelDisplay(15)
# d = OpenCVDisplay(15)
# d.add_dir("Sky")
# d.add_dir("crown", ".")
d.add_image("t.png")

# d.add_image("wave.jpg")
# d.add_images(["1.png", "2.png", "3.png", "4.png", "3.png", "2.png"])
d.display()
