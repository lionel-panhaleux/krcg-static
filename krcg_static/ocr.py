# Not used: kept here as a notepad if we need to do some OCR at some point

import cv2
import pytesseract


def read_library(path):
    # get the test zone only: need to resize images beforehand
    # or to use border/frame detection algorithms.
    # this measure was taken for a 353x500 pixels image
    img = cv2.imread(path, 0)[300:466, 40:308]
    # double exposure
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = min(255, img[i][j] * 2)
    # a bit of blur to make it smooth
    img = cv2.GaussianBlur(img, (3, 3), 0)
    # get a black-and-white picture for easier OCR
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # remove 5 pixels border to avoid detecting pipes everywhere
    # ask tesseract for OCR
    # remove end of feed char
    return pytesseract.image_to_string(img[5:161, 5:263])[:-1]
