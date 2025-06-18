import cv2
import numpy as np  


def opening(image, dim =3):
    window = np.ones((dim,dim), np.uint8)
    eroded_image = cv2.erode(image, window, iterations= 1)
    opened_image = cv2.dilate(eroded_image, window, iterations= 1)
    return opened_image


def closing(image, dim = 5):
    window = np.ones((dim,dim), np.uint8)
    dilated_image = cv2.dilate(image, window, iterations= 1)
    closed_image = cv2.erode(dilated_image, window, iterations= 1)
    return closed_image


