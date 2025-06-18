import cv2


def invert_image(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image


