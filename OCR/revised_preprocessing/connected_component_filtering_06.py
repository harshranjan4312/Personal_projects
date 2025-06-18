import numpy as np
import cv2

def connected_component_filtering(image, min_size=10):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(image, connectivity=8)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] < min_size:
            labels[labels == i] = 0
    filtered_image = np.where(labels > 0, 255, 0).astype("uint8")
    return filtered_image