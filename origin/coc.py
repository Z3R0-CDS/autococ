
import json

import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import os
import time
import argparse
from threading import Thread


class CV_DATA():
    __ceck_pos__ = {
        "left_x":580,
        "right_x": 1500,
        "top_y": 280,
        "bottom_y": 870
    }
    __screen_size = [1920, 1080]

def look_click(screen_cap, target, click=True):
    sift = cv2.SIFT_create()
    kp_item1, des_item1 = sift.detectAndCompute(target, None)
    kp_item2, des_item2 = sift.detectAndCompute(screen_cap, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des_item1, des_item2, k=2)
    match_pts_item = []
    for m1, m2 in matches:
        if m1.distance < 0.65 * m2.distance:
            idx = m1.trainIdx
            match_pts_item.append(kp_item2[idx].pt)
            break
    if len(match_pts_item) != 0:
        if click:
            match_pts_item = np.array(match_pts_item)
            curr_pos = pyautogui.position()
            pyautogui.click(match_pts_item[0, 0]+580, match_pts_item[0, 1]+280, button='left')
            pyautogui.moveTo(curr_pos)
        return True
    else:
        return False

def raw_click(target, screen_cap, click=True):
    sift = cv2.xfeatures2d.SIFT_create()
    kp_item1, des_item1 = sift.detectAndCompute(target, None)
    kp_item2, des_item2 = sift.detectAndCompute(screen_cap, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des_item1, des_item2, k=2)
    match_pts_item = []
    for m1, m2 in matches:
        if True: #m1.distance < 0.65 * m2.distance
            idx = m1.trainIdx
            match_pts_item.append(kp_item2[idx].pt)
            break

    if len(match_pts_item) != 0:
        if click:
            match_pts_item = np.array(match_pts_item)
            curr_pos = pyautogui.position()
            new_img = cv2.rectangle(screen_cap, (400,0), (1200,50), (0, 255, 255), thickness=2)
            cv2.imshow('Current view', new_img)
            cv2.waitKey(0)
            os._exit(1)
            pyautogui.click(match_pts_item[0, 0], match_pts_item[0, 1], button='left')
            pyautogui.moveTo(curr_pos)

def collect(item_img, test, item_type):
    if look_click(test, item_img):
        print(f"[{time.asctime()}] Collected {item_type}")
    print(f"[{time.asctime()}] Done for {item_type}")

def ack_reload(image, screencap):
    if look_click(screencap, image):
        print(f"[{time.asctime()}] Found reload")
    print(f"[{time.asctime()}] Looked for reload")

def check_errors(image, screencap, error_type):
    if look_click(screencap, image, click=False):
        print(f"[{time.asctime()}] Found error {error_type}")
        ack_reload(cv2.imread('collect/reload.jpg', 0), screencap)
        if error_type == "Forced timeout check":
            # timeout_reset()
            print("ok")
    print(f"[{time.asctime()}] Looked for error {error_type}")

def timeout_reset():
    test = np.array(ImageGrab.grab())
    capture = cv2.cvtColor(test, cv2.COLOR_RGB2GRAY)  # COLOR_RGB2GRAY
    raw_click(cv2.imread('collect/gold.jpg', 0), capture)

def auto_click():
    while True:
        load_config()
        if True:
            box = (CV_DATA.__ceck_pos__["left_x"], CV_DATA.__ceck_pos__["top_y"], CV_DATA.__ceck_pos__["right_x"], CV_DATA.__ceck_pos__["bottom_y"])
            # test = np.array(ImageGrab.grab(bbox=(580,280,1500,870)))#ImageGrab.grab(bbox=(16,62,1100,700)))
            test = np.array(ImageGrab.grab(bbox=box))
            test = cv2.cvtColor(test, cv2.COLOR_RGB2GRAY)#COLOR_RGB2GRAY
            print("============================================")
            # check_errors(cv2.imread('collect/afk.jpg', 0), test, error_type="Forced timeout check")
            # check_errors(cv2.imread('collect/auszeit.jpg', 0), test, error_type="Forced timeout check")
            ack_reload(cv2.imread('collect/reload.jpg', 0),test)
            collect(cv2.imread('collect/elix.jpg', 0), test, item_type="Elix")
            collect(cv2.imread('collect/gold.jpg', 0), test, item_type="Gold")
            collect(cv2.imread('collect/dark.jpg', 0), test, item_type="Dark Elix")
            collect(cv2.imread('collect/dia.jpg', 0), test, item_type="Gem")
            collect(cv2.imread('collect/gold2.jpg', 0), test, item_type="Gold2")
            collect(cv2.imread('collect/elix2.jpg', 0), test, item_type="Elix2")
            print("============================================")
            time.sleep(60)
            if cv2.waitKey(1) == 27:
                break

def show_area():
    load_config()
    test = np.array(ImageGrab.grab(bbox=(580, 280, 1500, 870)))
    test = cv2.cvtColor(test, cv2.COLOR_BGR2RGB)
    cv2.imshow('Current view', test)
    cv2.waitKey(0)
    os._exit(1)

def load_config():
    try:
        with open("config.json", "r") as x:
            config = json.load(x)
        CV_DATA.__ceck_pos__ = config["check_area"]
        CV_DATA.__screen_size = config["screen"]
    except:
        print("Config could not be loaded. Bye!")
        time.sleep(20)
        os._exit(1)


if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='COC auto farmer using cv2. By Zero Industries.')
    parser.add_argument('-l', type=str,
                        help='Specify option to run ("s" for show check_area  and "r" to run)', default="r")
    # parser.add_argument('-l', type=str)
    args = parser.parse_args()
    if args.l.lower()=="r":
        # timeout_reset()
        watcher_thread = Thread(target=auto_click)
        print("Starting threads")
        watcher_thread.run()
        print("Started thread [1/1]")
        print("Done")
        watcher_thread.join()
    elif args.l.lower()=="s":
        show_area()
    else:
        parser.print_help()
        os._exit(1)