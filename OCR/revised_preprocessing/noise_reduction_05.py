import cv2


#we will use 3 different denoising methods to get a properly denoised image
def gaussian_blur(image_input): 
    return cv2.GaussianBlur(image_input, (5,5), 0)
def median_blur(image_input):
   return cv2.medianBlur(image_input, 5)
def bilateral_filter(image_input):
    return cv2.bilateralFilter(image_input, 9, 75,75)

def combined_denoise(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    medianed= cv2.medianBlur(blurred, 5)
    denoised = cv2.bilateralFilter(medianed, 9, 75, 75)
    return denoised


