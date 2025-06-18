import cv2

def image_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



def thresholding_image(image, threshold=127):
    grayscaled_image = image_to_grayscale(image)
    method, thresholded_image = cv2.threshold(grayscaled_image, threshold, 255, cv2.THRESH_BINARY)
    return thresholded_image




