import cv2
from PIL import Image
import numpy as np

def resize(image_path):
    image = Image.open(image_path)
    dpi = image.info.get("dpi")
    image_width, image_height = image.size
    if dpi is not None:
        dpi_value = dpi[0]
    else:
        dpi_value = 72

    #we are aiming for 300 DPI
    scale_factor = 300 / dpi_value
    resized_width = int(image_width * scale_factor)
    resized_height = int(image_height * scale_factor)

    image_array = np.array(image)
    resized_image = cv2.resize(image_array, (resized_width, resized_height))

    return resized_image



