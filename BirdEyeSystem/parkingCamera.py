import cv2
import numpy as np
import os



#update the camera matrix wnad distortion coff you got from the calbiration part.
cameraMatrix = np.array([[1.16194631e+03, 0.00000000e+00, 1.91353747e+03],
                          [0.00000000e+00, 1.16326338e+03, 1.00390359e+03],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distCoeffs = np.array([-0.01669945, -0.08312363, 0.07524174, -0.02321733])


class ParkingCamera:

    def __init__(self, name, pathToImage, scale=[1.0, 1.0], shift=[0, 0]):

        self.name = name
        self.cameraMatrix = cameraMatrix
        self.distCoeffs = distCoeffs
        self.scale = scale
        self.shift = shift
        self.imagePath = pathToImage
        self.image = cv2.imread(pathToImage)
        self.resolution = self.image.shape[:2]
        self.initUndistortRectifyMap()


    def initUndistortRectifyMap(self):
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


    def undistort(self):
        """
        Undistorts a fisheye-distorted image using precomputed undistortion and rectification maps.

        Args:
            image (numpy.ndarray): The distorted input image to undistort.

        Returns:
            numpy.ndarray: The undistorted image.
        """
        return cv2.remap(self.image, *self.UndistortRectifyMap, interpolation=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_CONSTANT)

