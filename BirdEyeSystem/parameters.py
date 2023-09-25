import numpy as np
import cv2
import os

camerasPath = {
    "front": "resources/front.png",
    "rear":  "resources/rear.png",
    "left":  "resources/left.png",
    "right": "resources/right.png"
}

carImagePath = "resources/VWGolf17.png"


outputPath = "output/"

# --------------------------------------------------------------------


#update the camera matrix wnad distortion coff you got from the calbiration part.
cameraMatrix = np.array([[1.16194631e+03, 0.00000000e+00, 1.91353747e+03],
                         [0.00000000e+00, 1.16326338e+03, 1.00390359e+03],
                         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distCoeffs = np.array([-0.01669945, -0.08312363, 0.07524174, -0.02321733])


# --------------------------------------------------------------------



#how far outside the Checkboard you want to see in the stiched image.
shift_w = 150
shift_h = 150


# size of the gap between the calibration pattern and the car
gabBetweenCarAndCheckboardLeftOrRight = 22
gabBetweenCarAndCheckboardDown = 35
gabBetweenCarAndCheckboardUp = 25

# size of the gap between the Checkboards
gapBetweenTowCheckboardsInHoriznal = 487
gapBetweenTowCheckboardsInVertical = 219

# size of the checkboard
checkboradWidth = 100
checkboradHeight = 105

checkboardSize = 20

# total width/height of the output stitched image
total_h = gapBetweenTowCheckboardsInHoriznal + 2 * checkboradHeight + 2 * shift_h
total_w = gapBetweenTowCheckboardsInVertical + 2 * checkboradWidth + 2 * shift_w

# four corners of the  car [top-left (x_left, y_top), bottom-right (x_right, y_bottom)]
xl = shift_w + checkboradWidth + gabBetweenCarAndCheckboardLeftOrRight
xr = total_w - xl
yt = shift_h + checkboradHeight + gabBetweenCarAndCheckboardUp
yb = total_h - yt

# --------------------------------------------------------------------

frontL = 50
frontR = total_h - frontL

rearL = 50
rearR = total_h - rearL

rightL = 50
rightR = total_w - rightL

leftL = 50
leftR = total_w - leftL


# --------------------------------------------------------------------

projectShapes = {
    "front": (total_w, yt),
    "rear":  (total_w, yt),
    "left":  (total_h, xl),
    "right": (total_h, xl)
}


projectionPointsPerCategory = {
    "frontRear": [(shift_w + checkboardSize*3, shift_h + checkboardSize + 2.5),
                  (shift_w + checkboradWidth + gapBetweenTowCheckboardsInVertical + checkboardSize*2, shift_h + checkboardSize + 2.5),
                  (shift_w + checkboradWidth + gapBetweenTowCheckboardsInVertical + checkboardSize*2, shift_h + checkboardSize*4 + 2.5),
                  (shift_w + checkboardSize*3, shift_h + checkboardSize*4 + 2.5)],

    "leftRight": [(shift_h + checkboardSize*3 + 2.5, shift_w + checkboardSize),
                  (shift_h + checkboradHeight + gapBetweenTowCheckboardsInHoriznal + 2.5 + checkboardSize*2, shift_w + checkboardSize),
                  (shift_h + checkboradHeight + gapBetweenTowCheckboardsInHoriznal + 2.5 + checkboardSize*2, shift_w + checkboardSize*3),
                  (shift_h + checkboardSize*3 + 2.5, shift_w + checkboardSize*3)],
}


projectionPointsPerCam = {
    "front": projectionPointsPerCategory["frontRear"],
    "rear": projectionPointsPerCategory["frontRear"],
    "left": projectionPointsPerCategory["leftRight"],
    "right": projectionPointsPerCategory["leftRight"]
}


def readImage(pathToImage):
    try:
        with open(pathToImage):  # This will raise a FileNotFoundError if the file doesn't exist
            image = cv2.imread(pathToImage)
            if image is None:
                raise Exception("Error: Image not found or cannot be read.")
            return image
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{pathToImage}' not found.")
    except Exception as e:
        print(e)
        return None