from picamera import PiCamera
from time import sleep
from gpiozero import Button
from distutils import dir_util
from os import path
import os
from datetime import datetime
from photo_merge import merge

original_resolution = (1848, 2464)
RATIO = original_resolution[1]/original_resolution[0]
# Initial parameters and variables
SIZE = 480
RESOLUTION = (SIZE, int(SIZE*RATIO))
TODAY = datetime.today().strftime("%d-%m-%y")
CURRENT_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = path.join(CURRENT_DIR, "photos", TODAY)
dir_util.mkpath(BASE_DIR)
print("Base directory set to {}".format(BASE_DIR))
current_dirs = os.listdir(BASE_DIR)

if len(current_dirs)!=0:
    max_dir_num = max([int(d) for d in current_dirs])
    empty_dir_found=False
    for d in current_dirs:
        if len(os.listdir(path.join(BASE_DIR,d)))==0:
            empty_dir_found = True
            if int(d)>current_uid:
                current_uid = int(d)
        elif not empty_dir_found:
            current_uid = max_dir_num+1
else:
    current_uid = 1
        

# USER_ID = 1
USER_ID = current_uid


# Make the base directory
dir_util.mkpath(BASE_DIR)
# Define physical input variables
button1 = Button(14)
button2 = Button(15)
camera = PiCamera()
camera.preview_fullscreen=False
camera.preview_window=(5, 35, SIZE, int(SIZE*RATIO))
camera.resolution = RESOLUTION
camera.rotation = 90


# def start_process():
#     camera.start_preview()
#     uid = str(USER_ID).zfill(5)
#     button2.when_pressed = take_picture(uid, photo_number=1)
#     return True

# def stop_process():
#     camera.stop_preview()
#     USER_ID += 1
    
def take_picture(user_id, photo_number):
    
    camera.capture(path.join(BASE_DIR, user_id, "%.2d.jpg"%(photo_number)))
    return True

def run_process():
    global USER_ID
    while True:
        process_running = True
        photo_number = 1
        uid = str(USER_ID).zfill(5)
        dir_util.mkpath(path.join(BASE_DIR, uid))
        # Return button 1 to pre-pressed settings
        button1._active_event.clear()
        print("PUSH BUTTON")
        button1.wait_for_press()
        print("Current user ID set to: {}".format(USER_ID))
        camera.start_preview()
        sleep(1.1)
        while process_running:
            if button2.is_pressed:
                print("Taken photo number {}".format(photo_number))
                take_picture(uid, photo_number)
                photo_number += 1
            # Return button 2 to pre-pressed settings
            # button2._active_event.clear()
            elif button1.is_pressed:
                print("Stopping process")
                camera.stop_preview()
                merge(uid, debug=True)
                USER_ID += 1
                break
            else:
                continue


if __name__ == "__main__":
    run_process()
                   
                   
    
