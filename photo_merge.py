"""Merge photos from handscanner, using template."""
from tkinter import filedialog
from tkinter import Tk
import os
from PIL import Image
import pathlib
from datetime import datetime


def merge(UID, debug=False):
    """Merge photos together into one single image, using template.

    Args:
        UID (str): User ID to makephoto for.
        debug (boolean, optional): Whether to print debug info to console.
    """
    MEDIA_DIR = os.path.abspath(os.path.basename(__file__))
    if debug:
        print("MEDIA DIR: \t{}".format(MEDIA_DIR))
    CURRENT_DIR = os.path.join(MEDIA_DIR, datetime.now().strftime("%Y/%m/%d"))
    if debug:
        print("Writing to: \t{}".format(CURRENT_DIR))
    root = Tk()

    while True:
        root.filenames = filedialog.askopenfilenames(
            initialdir=MEDIA_DIR,
            title="Select photos",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"),
                       ("all files", "*.*")))
        if len(root.filenames) <= 6:
            break
        else:
            root = Tk()

    if debug:
        print(root.filenames)
    images = list(map(Image.open, root.filenames))
    widths, heights = zip(*(i.size for i in list(images)))

    total_width = max(widths) * 3
    max_height = 2 * max(heights)

    foreground = Image.new('RGB', (total_width, max_height))
    background = Image.open('handscannerTemplate.png')
    x_offset = 0
    y_offset = 0
    CURRENT_DIR = os.path.split(root.filenames[0])[0]
    pathlib.Path(CURRENT_DIR).mkdir(parents=True, exist_ok=True)

    for ix, im in enumerate(images):
        if debug:
            print("PHOTO {}: \n\tX_off:\t{}\n\tY_off:\t{}".format(
                ix, x_offset, y_offset))
        foreground.paste(im, (x_offset, y_offset))
        x_offset += im.size[0]
        if (ix + 1) % 3 == 0:
            x_offset = 0
            y_offset += im.size[1]

    background.paste(foreground, (40, 40))
    background.save(os.path.join(CURRENT_DIR, '{}_combined.png'.format(UID)))
    background.show()
