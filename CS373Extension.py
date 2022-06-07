from PIL import Image
import cv2
import numpy as np
import requests
import matplotlib

# THE FOLLOWING METHODS ARE PART OF THE ASSIGNMENT EXTENSION

# Save the plate image
def SaveLicensePlateImage(px_array, min_x, min_y, max_x, max_y):

    plate_array = np.zeros((min_y-max_y,max_x-min_x))

    for i in range(max_y, min_y):
        for j in range(min_x, max_x):
            plate_array[i-max_y][j-min_x] = px_array[i][j]

    cv2.imwrite("current_plate.png", plate_array)