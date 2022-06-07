import json
from PIL import Image
import cv2
import numpy as np
import requests

# THE FOLLOWING METHODS ARE PART OF THE ASSIGNMENT EXTENSION

# Save the plate image
def SaveLicensePlateImage(px_array, min_x, min_y, max_x, max_y):

    plate_array = np.zeros((min_y-max_y,max_x-min_x))

    for i in range(max_y, min_y):
        for j in range(min_x, max_x):
            plate_array[i-max_y][j-min_x] = px_array[i][j]

    cv2.imwrite("current_plate.png", plate_array)

# Compress the plate image to a smaller file size
def CompressImage(image_name="current_plate.png"):
    picture = Image.open(image_name)
    picture.save(image_name, 
                 optimize = True, 
                 quality = 10)


# Make the API request to the tesseract API
def TesseractAPIRequest(image_name="current_plate.png"):

    payload = {'isOverlayRequired': True,
               'apikey': 'K82744958488957',
               'OCREngine': 2,
               'language': 'eng',
               }
    with open(image_name, 'rb') as imagefile:
        saved_data = requests.post('https://api.ocr.space/parse/image',
                          files={image_name: imagefile},
                          data=payload,
                          )
    return saved_data.content.decode()


def PrintPlateFromAPI():
    request_data = TesseractAPIRequest()

    request_data = json.loads(request_data)

    plate_text = request_data.get("ParsedResults")[0].get("ParsedText")

    print(plate_text)
