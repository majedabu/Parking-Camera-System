import cv2
from parkingCamera import ParkingCamera
import numpy as np
import argparse
from point_selector import select_points_and_draw_lines
from parameters import camerasPath, total_w, total_h, xl, xr, yt, yb, projectionPointsPerCam, carImagePath, outputPath, readImage
import random

class BirdEyeSystem:

    def __init__(self):

        self.ParkingCameraLeft = ParkingCamera("left", camerasPath["left"], [0.5, 0.5], [150, -100])
        self.ParkingCameraRight = ParkingCamera("right", camerasPath["right"], [0.5, 0.5], [-150, 0])
        self.ParkingCameraFront = ParkingCamera("front", camerasPath["front"], [0.5, 0.5], [100, 0])
        self.ParkingCameraRear = ParkingCamera("rear", camerasPath["rear"], [0.5, 0.5], [50, 0])

        self.ParkingCameraList = {
            "left": self.ParkingCameraLeft,
            "right": self.ParkingCameraRight,
            "front": self.ParkingCameraFront,
            "rear": self.ParkingCameraRear
        }

        self.undistortedParkingCamerasDict = {}
        self.projectedParkingCamerasDict = {}
        self.projectedWithFlip = {}
        self.carImage = readImage(carImagePath)
        self.image = np.zeros((total_h, total_w, 3), np.uint8)
        self.averageLuminance = None
        self.averageLuminancePerImage = {}


    def UndistoreParkingCameras(self, isNeedToSave=False):
        """
        Undistorts images from parking cameras.

        Args:
            isNeedToSave (bool): Indicates whether to save the undistorted images.

        Returns:
            None
        """

        #iterate through parking cameras
        for camName, parkingCamera in self.ParkingCameraList.items():
            #Undistort the image
            res = parkingCamera.Undistort()

            if isNeedToSave:
                outPath = outputPath + camName + "_undistorted.png"
                self.SaveImage(outPath, res)

            # store undistorted image in the dictionary
            self.undistortedParkingCamerasDict[parkingCamera.cameraName] = res


    def ProjectParkingCameras(self, isNeedToSave=False):
        """
        Projects parking cameras to a bird's eye view using perspective transformation.

        Args:
            isNeedToSave (bool): Indicates whether to save the images.

        Returns:
            None
        """

        #step 1: Undistort parking cameras
        self.UndistoreParkingCameras(isNeedToSave)

        #step 2: Iterate through undistorted cameras
        for name, undistorted in self.undistortedParkingCamerasDict.items():
            imgPath = self.ParkingCameraList[name].imagePath

            #step 3: Select points for perspective transformation
            selectedPoints = np.float32(select_points_and_draw_lines(undistorted, outputPath + name + "_selectedPoints.png", isNeedToSave))

            #step 4: define destination points for perspective transformation
            destinationPoints = np.float32(projectionPointsPerCam[name])

            #step 5: calculate perspective transformation matrix
            self.ParkingCameraList[name].projectMatrix = cv2.getPerspectiveTransform(selectedPoints, destinationPoints)

            #step 6: project the image to bird's eye view
            birdEyeImage = self.ParkingCameraList[name].Project(undistorted)

            self.projectedParkingCamerasDict[name] = birdEyeImage
            #save the bird's eye view image if required
            if isNeedToSave:
                outPath = outputPath + name + "_birdEye.png"
                self.SaveImage(outPath, birdEyeImage)

            #show the bird's eye view image
            self.ShowImage("Bird's View", birdEyeImage)


    def ApplyLuminance(self):

        total_luminance = 0

        for imgName, img in self.projectedWithFlip.items():
            lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l_channel = lab_img[:, :, 0]
            self.averageLuminancePerImage[imgName] = l_channel.mean() / 100.0
            total_luminance += self.averageLuminancePerImage[imgName]  # Normalize to [0, 1]

        self.averageLuminance = total_luminance / 4


        for imgName, image in self.projectedWithFlip.items():

            factor = self.averageLuminance / self.averageLuminancePerImage[imgName]

            print(imgName, factor)
            # Convert BGR to LAB
            lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

            # Split LAB channels
            l_channel, a_channel, b_channel = cv2.split(lab_image)

            # Convert L channel to float and adjust luminance
            l_channel = np.clip(l_channel.astype(np.float32) * factor, 0, 255).astype(np.uint8)

            # Merge LAB channels back
            adjusted_lab_image = cv2.merge((l_channel, a_channel, b_channel))

            # Convert LAB back to BGR
            adjusted_image = cv2.cvtColor(adjusted_lab_image, cv2.COLOR_LAB2BGR)

            self.projectedWithFlip[imgName] = adjusted_image



    def TopView(self, isNeedToSave=False, applyLuminance=False):

        self.ProjectParkingCameras(isNeedToSave=isNeedToSave)
        for cameraName, projected_ in self.projectedParkingCamerasDict.items():
            self.projectedWithFlip[cameraName] = self.ParkingCameraList[cameraName].FlipImage(projected_)

        if applyLuminance:
            self.ApplyLuminance()

        self.Stich()
        self.AddCar()

        if isNeedToSave:
            outPath = outputPath + "birdEye.png"
            self.SaveImage(outPath, self.image)

        self.ShowImage("BirdView Result", self.image)



    def ShowImage(self, window_title, image):
        cv2.imshow(window_title, image)
        while True:
            key = cv2.waitKey(1) & 0xFF
            # 'Enter' key is detected!
            if key == 13 or key == ord("q"):
                return 1


    def SaveImage(self, output_path, data):
        print("saving " + output_path + " ...")
        cv2.imwrite(output_path, data)

    def crop_by_direction(self, direction):
        if direction == "FL":
            return self.image[:yt, :xl]
        elif direction == "F":
            return self.image[:yt, xl:xr]
        elif direction == "FR":
            return self.image[:yt, xr:]
        elif direction == "BL":
            return self.image[yb:, :xl]
        elif direction == "B":
            return self.image[yb:, xl:xr]
        elif direction == "BR":
            return self.image[yb:, xr:]
        elif direction == "L":
            return self.image[yt:yb, :xl]
        elif direction == "R":
            return self.image[yt:yb, xr:]
        elif direction == "C":
            return self.image[yt:yb, xl:xr]
        else:
            raise ValueError("Invalid direction: {}".format(direction))


    def Stich(self):

        front = self.projectedWithFlip["front"]
        rear = self.projectedWithFlip["rear"]
        left = self.projectedWithFlip["left"]
        right = self.projectedWithFlip["right"]

        np.copyto(self.crop_by_direction("F"), self.crop_image(front, "FM"))
        np.copyto(self.crop_by_direction("B"), self.crop_image(rear, "BM"))
        np.copyto(self.crop_by_direction("L"), self.crop_image(left, "LM"))
        np.copyto(self.crop_by_direction("R"), self.crop_image(right, "RM"))

        np.copyto(self.crop_by_direction("FL"), self.AverageMergeTwoImage(self.crop_image(front, "FI"), self.crop_image(left, "LI"), 0.4, 180, 0.4, 160))
        np.copyto(self.crop_by_direction("FR"), self.AverageMergeTwoImage(self.crop_image(front, "FII"), self.crop_image(right, "RII"), -0.4, yt-10, -0.4, yt-11))
        np.copyto(self.crop_by_direction("BL"), self.AverageMergeTwoImage(self.crop_image(left, "LIII"), self.crop_image(rear, "BIII"),  -0.4, 115, -0.4, 95))
        np.copyto(self.crop_by_direction("BR"), self.AverageMergeTwoImage(self.crop_image(right, "RIV"), self.crop_image(rear, "BIV"), 0.4, 15, 0.4, 0))


    def AverageMergeTwoImage(self, imA, imB, m1, b1, m2, b2):
        # Initialize an array with the same dimensions as imA
        merged_image = np.zeros_like(imA)

        for i in range(imA.shape[0]):


            for j in range(imA.shape[1]):
                #calculate the y positions on the two lines
                y_linear2 = int(m1 * j + b1)
                y_linear1 = int(m2 * j + b2)

                if i < y_linear1:
                    # If above line 1, choose pixel from imA
                    if not np.all(imA[i, j] == [0, 0, 0]):
                        merged_image[i, j] = imA[i, j]

                elif i > y_linear2:
                    # If below line 2, choose pixel from imB
                    if not np.all(imB[i, j] == [0, 0, 0]):
                        merged_image[i, j] = imB[i, j]

                else:
                    # For overlapping region, perform weighted average
                    if not np.all(imA[i, j] == [0, 0, 0]):
                        if not np.all(imB[i, j] == [0, 0, 0]):
                            merged_image[i, j] = (imA[i, j] * 0.5 + imB[i, j] * 0.5).astype(np.uint8)
                        else:
                            merged_image[i, j] = imA[i, j]
                    elif not np.all(imB[i, j] == [0, 0, 0]):
                        merged_image[i, j] = imB[i, j]

                if np.all(merged_image[i, j] == [0, 0, 0]):
                    if not np.all(imA[i, j] == [0, 0, 0]):
                        merged_image[i, j] = imA[i, j]
                    else:
                        merged_image[i, j] = imB[i, j]


        return merged_image


    def AverageMergeTwoImagexx(self, imA, imB, m1, b1, m2, b2):
        # Initialize an array with the same dimensions as imA
        merged_image = np.zeros_like(imA)

        for i in range(imA.shape[0]):
            for j in range(imA.shape[1]):
                #calculate the y positions on the two lines
                y_linear1 = int(m1 * j + b1)
                y_linear2 = int(m2 * j + b2)

                if i == y_linear2:
                    merged_image[i, j] = [255, 0, 0]

                elif i == y_linear1:
                    merged_image[i, j] = [0, 255, 0]

        return merged_image


    def AddCar(self):

        self.carImage = cv2.resize(self.carImage, (xr - xl, yb - yt))
        np.copyto(self.crop_by_direction("C"), self.carImage)

    def crop_image(self, image, crop_type):
        if crop_type == "FI":
            return image[:, :xl]
        elif crop_type == "FII":
            return image[:, xr:]
        elif crop_type == "FM":
            return image[:, xl:xr]
        elif crop_type == "BIII":
            return image[:, :xl]
        elif crop_type == "BIV":
            return image[:, xr:]
        elif crop_type == "BM":
            return image[:, xl:xr]
        elif crop_type == "LI":
            return image[:yt, :]
        elif crop_type == "LIII":
            return image[yb:, :]
        elif crop_type == "LM":
            return image[yt:yb, :]
        elif crop_type == "RII":
            return image[:yt, :]
        elif crop_type == "RIV":
            return image[yb:, :]
        elif crop_type == "RM":
            return image[yt:yb, :]
        else:
            raise ValueError("Invalid crop type: {}".format(crop_type))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-undistore", action="store_true", help="")
    parser.add_argument("-projection", action="store_true", help="")
    parser.add_argument("-topView", action="store_true", help="")

    args = parser.parse_args()
    BirdEyeSystemOBJ = BirdEyeSystem()


    if args.projection:
        print("running projection")
        BirdEyeSystemOBJ.ProjectParkingCameras(isNeedToSave=True)

    elif args.undistore:
        print("running undistortionParkingCameras")
        BirdEyeSystemOBJ.UndistoreParkingCameras(isNeedToSave=True)

    elif args.topView:
        print("running topView")
        BirdEyeSystemOBJ.TopView(isNeedToSave=True, applyLuminance=True)

if __name__ == "__main__":

    main()
