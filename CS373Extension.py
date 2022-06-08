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
def TesseractAPIRequest(image_name="current_plate.png", engine_num=2):

    # This is my API key, and I am leaving it in here for convenience of the marker so please remove the API key before posting anywhere else :)
    payload = {'isOverlayRequired': True,
               'apikey': 'K82744958488957',
               'OCREngine': engine_num,
               'language': 'eng',
               }
    with open(image_name, 'rb') as imagefile:
        saved_data = requests.post('https://api.ocr.space/parse/image',
                          files={image_name: imagefile},
                          data=payload,
                          )
    return saved_data.content.decode()


def ParseData(request_data):

    try:
        plate_text = request_data.get("ParsedResults")[0].get("ParsedText")
    except:
        print("Unable to find a number plate, trying different tesseract engine.")
        return "error_no_plate"

    return plate_text


def PrintPlateFromAPI():
    request_data = TesseractAPIRequest("current_plate.png", 2)

    request_data = json.loads(request_data)

    plate_text = ParseData(request_data) 

    # If engine 2 failed, try engine 1
    if plate_text == "error_no_plate":
        request_data = TesseractAPIRequest("current_plate.png", 1)
        request_data = json.loads(request_data)

        plate_text = ParseData(request_data)

    # If engine 1 failed, try engine 3
    if plate_text == "error_no_plate":
        request_data = TesseractAPIRequest("current_plate.png", 3)
        request_data = json.loads(request_data)

        plate_text = ParseData(request_data)

    # No engines worked, unable to find text
    if plate_text == "error_no_plate":
        print("Was unable to find number plate details, please try a different number plate")
        return

    print("{ TEXT ON NUMBER PLATE }")

    print(plate_text)

    print("==== END OF PROGRAM ====")