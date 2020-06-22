# Simple test for NeoPixels on Raspberry Pi

from display import OpenCVDisplay
from pi.pixel_display import PixelDisplay

base_dir = "/home/pi/dev/pi-lights/"

d = PixelDisplay(15, refresh=230)
#d = OpenCVDisplay(15)
# d.add_dir("Sky")
d.add_dir(base_dir + "uni")
#d.add_dir(base_dir + "crown", ".")
# d.add_image("t.png")

# d.add_image("wave.jpg")
d.display()
