# 2021 Pekka Oksiala
#
# crop picture: find and remove black/while frames;typically due to scan
#
# CropperHandler

import glob
import math
import os
import sys

from PIL import Image


class CropperHandler:
    def __init__(self, picname: str):
        # consts
        self._dir_target = "crops"  # relative to current

        self.cRgbBlackSum = 50  # below (black = 3 * 0)
        self.cRgbWhiteSum = 700  # above (white = 3 * 255)
        self.cRgbLevel = 30

        self.cExtCrop = 10  # add extra crop to automatic crop value
        self.cStartFromEdge = 200  # start point from pic edge
        self.cFileMode = "*." + "jpg"  # files to process

        self.ifile = picname
        self._limits = []
        # open file
        print(self.ifile)  # files to process
        self.im = Image.open(self.ifile)
        # and create output dir if not exist
        self.ensure_dir()

    # create target dir if not exist
    def ensure_dir(self):
        if not os.path.exists(self._dir_target):
            os.mkdir(self._dir_target)

    # is edge: define it by rgb values
    #  by: rgb-sum (or separate rgb values)
    def is_edge(self, x: int, y: int):
        if True:
            _r, _g, _b = self.im.getpixel((x, y))
            if (_r + _g + _b) < self.cRgbBlackSum or (_r + _g + _b) > self.cRgbWhiteSum:
                return True
            else:
                return False
        else:
            if _r < self.cRgbLevel and _g < self.cRgbLevel and _b < self.cRgbLevel:
                return True
            else:
                return False

    # what: 0=left, 1=up, 2=right, 3=down
    def search_pic_edge(self, im, what):
        _dx = _dy = 0
        if what == 0:
            _dx = 1
        if what == 1:
            _dy = 1
        if what == 2:
            _dx = -1
        if what == 0:
            _dy = -1
        _n = 0
        return _n

    # photo orintation: find edge at 1/6 and 5/6, calculate angel and rotate
    # dev dev dev
    def line_up(self, im):
        xres, yres = im.size
        rad = 57.3  # degrees
        n1 = cStartFromEdge
        xp = xres / 6.0
        while is_edge(xp, n1):
            n1 += 1
        n2 = cStartFromEdge
        xp = 5.0 * xres / 6.0
        while is_edge(xp, n2):
            n2 += 1
        degree = rad * math.atan(1.0 * (n2 - n1) / (4.0 * xres / 6.0))
        # if calculated angle 'too' big do not line up: can't calculate from pic
        if degree > 3.0 or degree < -3.0:
            print("   -no line up due to angle calc impossible/not reasonable")
        elif degree > -0.5 and degree < 0.5:
            print("   -no need for line up")
        else:
            im = im.rotate(degree)
            print(
                "   -rotate=" + str(degree)
            )  # + ", dx=" + str(4.0*xres/6.0) + ", dy=" + str(n1-n2)
        return im

    def find_edges(self):
        _xres, _yres = self.im.size
        _xps = (int(_xres / 4), int(_xres / 2), int(_xres * 0.75))  # sample locations
        _yps = (int(_yres / 4), int(_yres / 2), int(_yres * 0.75))

        # left edge
        _x = self.cStartFromEdge
        while _x > 0 and (
            self.is_edge(_x, _yps[0]) == False
            or self.is_edge(_x, _yps[1]) == False
            or self.is_edge(_x, _yps[2]) == False
        ):
            _x -= 1
        self._limits.append(_x + self.cExtCrop)

        # right edge.
        _x = _xres - self.cStartFromEdge
        while _x < _xres and (
            self.is_edge(_x, _yps[0]) == False
            or self.is_edge(_x, _yps[1]) == False
            or self.is_edge(_x, _yps[2]) == False
        ):
            _x += 1
        self._limits.append(_x - self.cExtCrop)

        # upper edge
        _y = self.cStartFromEdge
        while _y > 0 and (
            self.is_edge(_xps[0], _y) == False
            or self.is_edge(_xps[1], _y) == False
            or self.is_edge(_xps[2], _y) == False
        ):
            _y -= 1
        self._limits.append(_y + self.cExtCrop)

        # lower edge
        _y = _yres - self.cStartFromEdge
        while _y < _yres and (
            self.is_edge(_xps[0], _y) == False
            or self.is_edge(_xps[1], _y) == False
            or self.is_edge(_xps[2], _y) == False
        ):
            _y += 1
        self._limits.append(_y - self.cExtCrop)

        return self._limits

    def save_crop(self, limits):
        _tofile = self._dir_target + "/" + self.ifile
        # remove existing
        if os.path.exists(_tofile):
            os.unlink(_tofile)
        # crop picture by found edges
        _region = self.im.crop((limits[0], limits[2], limits[1], limits[3]))
        _region.save(_tofile, quality=95)

    def get_image(self):
        return self.im

    def change_edge(self, direction, c_val):
        if direction == "up":
            self._limits[2] += c_val
        elif direction == "down":
            self._limits[3] += c_val
        elif direction == "left":
            self._limits[0] += c_val
        elif direction == "right":
            self._limits[1] += c_val

        return self._limits


# -------------- 'main' code ----------------------
def main():
    if len(sys.argv) <= 1:
        print("Usage: cropperhandler filemask")
        return

    # loop pic files
    picfiles = sys.argv[1:]
    for infile in picfiles:
        hdr = CropperHandler(infile)
        lims = hdr.find_edges()
        hdr.save_crop(lims)


if __name__ == "__main__":
    main()
