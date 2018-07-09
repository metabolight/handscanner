# -*- coding: utf-8 -*-
""" Take a picture from the emtabolight hand scanner.

Take a picture using the metabolight handscanner and save the image
to the selected drive.

"""

from picamera import PiCamera
from time import sleep
from gpiozero import Button
from distutils import dir_util
from os import path
import os
from datetime import datetime
from photo_merge import merge


###  Define state variables ###
original_resolution = (1848, 2464)
"""tuple: original resolution of camera."""
RATIO = original_resolution[1] / original_resolution[0]
"""float: aspect ratio of the camera."""
# Initial parameters and variables
SIZE = 480
"""int: width of camera image."""
RESOLUTION = (SIZE, int(SIZE * RATIO))
"""tuple: scaled rsoluation of camera."""
TODAY = datetime.today().strftime("%d-%m-%y")
"""str: today's date for use in naming directories."""
CURRENT_DIR = path.abspath(path.dirname(__file__))
"""str: directory code is stored in."""
BASE_DIR = path.join(CURRENT_DIR, "photos", TODAY)
"""str: directory to store images in."""
dir_util.mkpath(BASE_DIR)
print("Base directory set to {}".format(BASE_DIR))
current_dirs = os.listdir(BASE_DIR)
"""list: List of current directories inside `BASE_DIR`."""


def get_uid(current_dirs):
    """ Get current user ID.
    Args:
        current_dirs (list of str): List of directories currently in BASE_DIR.
    Returns:
        current_uid (int): Current user ID
    """

    if len(current_dirs) == 0:
        current_uid = 1
    else:
        max_dir_num = max([int(d) for d in current_dirs])
        empty_dir_found = False
        for d in current_dirs:
            if len(os.listdir(path.join(BASE_DIR, d))) == 0:
                empty_dir_found = True
                if int(d) > current_uid:
                    current_uid = int(d)
            elif not empty_dir_found:
                current_uid = max_dir_num + 1
    return current_uid


# USER_ID = 1


def setup_camera():
    """ Set up the camera and controller.

    Returns:
        camera_config (dict): dict containing -
            camera (Object): configured pi camera object.
            preview_button (Object): configured preview controller button.
            photo_button (Object): configured photo controller button.
    """
    # Make the base directory
    dir_util.mkpath(BASE_DIR)
    # Define physical input variables
    preview_button = Button(14)
    photo_button = Button(15)

    camera = PiCamera()
    camera.preview_fullscreen = False
    camera.preview_window = (5, 35, SIZE, int(SIZE * RATIO))
    camera.resolution = RESOLUTION
    camera.rotation = 90

    camera_config = {
        "camera": camera,
        "preview_button": preview_button,
        "photo_button": photo_button
    }

    return camera_config


# def start_process():
#     camera.start_preview()
#     uid = str(USER_ID).zfill(5)
#     photo_button.when_pressed = take_picture(uid, photo_number=1)
#     return True

# def stop_process():
#     camera.stop_preview()
#     USER_ID += 1

def take_picture(camera, user_id, photo_number):
    """ Take a picture and store photo.
    Args:
        camera (Object): configured camera used for photo.
        user_id (str): user ID for photo being taken.
        photo_number (int): Number for current user's photo.
    """

    camera.capture(path.join(BASE_DIR, user_id, "%.2d.jpg" % (photo_number)))
    return True


def run_process(camera_config):
    """ Process to take multiple photos.

    Args:
        camera_config (dict): dict of information for configured camera set up

    """
    USER_ID = get_uid(current_dirs)

    camera = camera_config['camera']
    preview_button = camera_config['preview_button']
    photo_button = camera_config['photo_button']

    while True:
        process_running = True
        photo_number = 1
        uid = str(USER_ID).zfill(5)
        dir_util.mkpath(path.join(BASE_DIR, uid))
        # Return button 1 to pre-pressed settings
        preview_button._active_event.clear()
        print("PUSH BUTTON")
        preview_button.wait_for_press()
        print("Current user ID set to: {}".format(USER_ID))
        camera.start_preview()
        sleep(1.1)
        while process_running:
            if photo_button.is_pressed:
                print("Taken photo number {}".format(photo_number))
                take_picture(camera, uid, photo_number)
                photo_number += 1
            # Return button 2 to pre-pressed settings
            # photo_button._active_event.clear()
            elif preview_button.is_pressed:
                print("Stopping process")
                camera.stop_preview()
                merge(uid, debug=True)
                USER_ID += 1
                break
            else:
                continue


if __name__ == "__main__":

    camera_config = setup_camera()
    run_process(camera_config)
