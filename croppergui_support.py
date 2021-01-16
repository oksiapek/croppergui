#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 6.0
#  in conjunction with Tcl version 8.6
#    Dec 21, 2020 03:50:19 PM EET  platform: Linux
#    Jan 13, 2021 08:42:27 PM EET  platform: Linux
#    Jan 14, 2021 11:44:05 AM EET  platform: Linux
#    Jan 14, 2021 11:47:32 AM EET  platform: Linux

import sys
from PIL import Image, ImageTk
from cropperhandler import CropperHandler

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

_crop_handler = 0
_crop_lines = [10, 10, 600, 800]

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def a_btnClose(p1):
    print('croppergui_support.a_btnClose')
    sys.stdout.flush()

def a_btnCrop(p1):
    print('croppergui_support.a_btnCrop')
    sys.stdout.flush()

def a_btnNext(p1):
    print('croppergui_support.a_btnNext')
    sys.stdout.flush()

    _crop_handler = CropperHandler('Agadir_8302_011.jpg')
    # load the image file and fit it to canvas
    ima = _crop_handler.get_image().resize((w.canvPhoto.winfo_width(), w.canvPhoto.winfo_height()), Image.BILINEAR)
    photo = ImageTk.PhotoImage(ima)
    # put image on canvas
    w.canvPhoto.imageList = []
    id = w.canvPhoto.create_image(0, 0, image=photo, anchor=tk.NW)
    w.canvPhoto.imageList.append(photo)
    
    # calc crop lines: scale from org
    _org_size = _crop_handler.get_image().size
    _crops = _crop_handler.find_edges()
    _x_scale = w.canvPhoto.winfo_width() / _org_size[0]
    _y_scale = w.canvPhoto.winfo_height() / _org_size[1]
    _crop_lines[0] = _crops[0] * _x_scale
    _crop_lines[1] = _crops[2] * _y_scale
    _crop_lines[2] = _crops[1] * _x_scale
    _crop_lines[3] = _crops[3] * _y_scale
    # and add to canvas
    w.canvPhoto.create_rectangle(_crop_lines[0],_crop_lines[1],_crop_lines[2],_crop_lines[3],outline='white', dash='2 4')

def a_canv_mousewheel(p1):
    print('croppergui_support.a_canv_mousewheel')
    sys.stdout.flush()


def a_canv_scroll_down(p1):
    # add crop lines
    _crop_lines[3] -= 10
    w.canvPhoto.create_rectangle(_crop_lines[0],_crop_lines[1],_crop_lines[2],_crop_lines[3],outline='white', dash='2 4')
    print('croppergui_support.a_canv_scroll_down')
    sys.stdout.flush()

def a_canv_scroll_up(p1):
    # add crop lines
    _crop_lines[3] += 10
    w.canvPhoto.create_rectangle(_crop_lines[0],_crop_lines[1],_crop_lines[2],_crop_lines[3],outline='white', dash='2 4')
    print('croppergui_support.a_canv_scroll_up')
    sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import croppergui
    croppergui.vp_start_gui()





