import cv2
import numpy as np
from parameters import cameraMatrix, distCoeffs, projectShapes, readImage



class ParkingCamera:

    def __init__(self, name, pathToImage, scale=[1.0, 1.0], shift=[0, 0]):

        self.cameraName = name
        self.cameraMatrix = cameraMatrix
        self.distCoeffs = distCoeffs
        self.scale = scale
        self.shift = shift
        self.imagePath = pathToImage
        self.image = readImage(pathToImage)
        self.resolution = self.image.shape[:2]
        self.projectMatrix = None
        self.projectShape = projectShapes[name]
        self.InitUndistortRectifyMap()


    def FlipImage(self, image):

        if self.cameraName == "rear":
            return image.copy()[::-1, ::-1, :]
        elif self.cameraName == "left":
            return cv2.transpose(image)[::-1]
        elif self.cameraName == "front":
            return image.copy()
        else:#right
            return np.flip(cv2.transpose(image), 1)

    def InitUndistortRectifyMap(self):
        """
        Initializes the undistortion and rectification map for fisheye camera calibration.

        This function performs the following steps:
        1. Creates a new camera matrix by applying scaling and shifting transformations.
        2. Initializes an undistortion and rectification map using the modified camera matrix.
        3. Stores the resulting map in 'self.UndistortRectifyMap' for later use.
        """
        newMatrix = self.cameraMatrix.copy()
        newMatrix[0, 0] *= self.scale[0]
        newMatrix[1, 1] *= self.scale[1]
        newMatrix[0, 2] += self.shift[0]
        newMatrix[1, 2] += self.shift[1]
        height, width = self.resolution
        self.UndistortRectifyMap = cv2.fisheye.initUndistortRectifyMap(
            self.cameraMatrix, self.distCoeffs, np.eye(3), newMatrix, (width, height), cv2.CV_16SC2)


    def Undistort(self):
        """
        Undistorts a fisheye-distorted image using precomputed undistortion and rectification maps.

        Args:
            image (numpy.ndarray): The distorted input image to undistort.

        Returns:
            numpy.ndarray: The undistorted image.
        """
        return cv2.remap(self.image, *self.UndistortRectifyMap, interpolation=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_CONSTANT)

    def Project(self, image):
        result = cv2.warpPerspective(image, self.projectMatrix, self.projectShape)
        return result