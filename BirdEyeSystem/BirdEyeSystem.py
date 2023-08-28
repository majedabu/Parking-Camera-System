import cv2
import os
from parkingCamera import ParkingCamera
import argparse



class BirdEyeSystem:

    def __init__(self):

        self.ParkingCameraLeft = ParkingCamera("left", "imgs/left.png", [1.0, 1.0], [300, 0])
        self.ParkingCameraRight = ParkingCamera("right", "imgs/right.png",[0.65, 0.65], [0, 0])
        self.ParkingCameraFront = ParkingCamera("front", "imgs/front.png" ,[0.65, 0.65], [0, 0])
        self.ParkingCameraRear = ParkingCamera("rear", "imgs/rear.png",[0.65, 0.65], [0, 0])
        self.ParkingCameraList = [self.ParkingCameraLeft, self.ParkingCameraRight, self.ParkingCameraFront, self.ParkingCameraRear]
        self.undistorParkingCamerasDict = {}




    def undistoreParkingCameras(self, isNeedToSave=False):

        for parkingCamera in self.ParkingCameraList:
            res = parkingCamera.undistort()
            if isNeedToSave:
                outPath=parkingCamera.imagePath.replace(".png", "_undistorted.png")
                print("saving "+outPath+" ...")
                cv2.imwrite(outPath, res)

            self.undistorParkingCamerasDict[parkingCamera.name] = res


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-undistore", action="store_true", help="")
    args = parser.parse_args()

    BirdEyeSystemOBJ = BirdEyeSystem()
    if args.undistore:
        print("running undistorParkingCameras")
        BirdEyeSystemOBJ.undistoreParkingCameras(isNeedToSave=True)


if __name__ == "__main__":

    main()
