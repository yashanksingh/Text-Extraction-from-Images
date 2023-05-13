# python main.py --image 18628.png

import argparse
import os
from datetime import datetime

import clipboard
import cv2
import keyboard
from PIL import ImageGrab
from pytesseract import *

from util import *

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False)
args = vars(ap.parse_args())


def extractText(image = None):
    if image is None:
        image = ImageGrab.grabclipboard()
        gray_image = get_grayscale(clip=image)
    else:
        gray_image = get_grayscale(image=image)

    if gray_image is None:
        warn("Cannot open image. Check file path/integrity.")
        return

    text = pytesseract.image_to_string(gray_image)
    print(text)
    clipboard.copy(text)


# noinspection PyBroadException
def get_grayscale(image = None, clip = None):
    try:
        curr = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = os.path.dirname(os.path.abspath(__file__)) + fr"\tests\{curr}"
        os.makedirs(path)

        if image is None:
            clip.save(path + r"\ORIG.png", "PNG")
        else:
            cv2.imwrite(path + r"\ORIG.png", image)

        orig_image = cv2.imread(path + r"\ORIG.png")
        gray = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path + r"\GRAY.png", gray)

        return cv2.imread(path+  r"\GRAY.png")
    except Exception:
        return None


def main():
    start()
    argImagePath = args["image"]
    if argImagePath is not None:
        path = os.path.dirname(os.path.abspath(__file__)) + "\\" + argImagePath
        argImage = cv2.imread(path)
        extractText(argImage)
        stop()

    keyboard.add_hotkey("ctrl+shift+|", extractText)
    keyboard.wait("ctrl+`")

if __name__ == "__main__":
    main()
