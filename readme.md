# Parking camera system VW Golf 2017 - (BirdEye)

## _equimpent to prepare:_

 - (4) ELP 8mp USB Camera Wide Angle Fisheye Lens 180 Degree 4K [amazon](https://www.amazon.com/-/he/dp/B01HD1V3UO?ref=ppx_yo2ov_dt_b_product_details&th=1)
 - (4) papers of checkboard white-black (5X5), size 100cmX100cm the size of each black/white square is 20cmX20cm.


# camera calibration:
	
1. connect the camera to the pc and capture multiple images of the checkerboard pattern from different angles and positions.
     - examples exists in [cameraCalbiration\imgs](https://github.com/majedabu/Parking-Camera-System/tree/main/cameraCalbiration/imgs)
     - script : [CaptureAndSave.html](https://github.com/majedabu/Parking-Camera-System/blob/main/cameraCalbiration/CaptureAndSave.html)

|   |   |   |
|:-:|:-:|:-:|
|ex1|ex2|ex3|
|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (35).png"/>|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (23).png"/>|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (19).png"/>|

2. calbirate the camera  using OpenCV calibration method for fisheye cameras.
     - script : [extractFisheyeCameraIntrinsics.py](https://github.com/majedabu/Parking-Camera-System/blob/main/cameraCalbiration/extractFisheyeCameraIntrinsics%20.py)
    
|   |
|:-:|
|camera matrix 3x3 output (focal length and center) + Distortion Coefficients 1x4 vector.|
|<img style="margin:0px auto;display:block" src=".\cameraCalbiration\cameraCalbiration.png"/>|


# Image Undistortion and Corner Capture
In our case, we require precise control over the image transformation to ensure we capture the corners of each camera frame without losing any pixels. The default OpenCV fisheye undistortion process can be problematic as it tends to crop the image and display a region that OpenCV deems suitable.
To address this issue, we leverage the "cv2.fisheye.initUndistortRectifyMap" function, which offers the capability to perform both scaling and shifting (translation). <br/> By employing this function, we obtain a new intrinsic matrix tailored to our specific needs. Subsequently, we apply this transformation using the "remap" function.
This approach allows us to maintain control over the scaling and translation of the image, ensuring that we capture all the critical corners while preserving all the pixels in the process.

- script : [BirdEyeSystem.py](https://github.com/majedabu/Parking-Camera-System/blob/main/BirdEyeSystem/BirdEyeSystem.py)
- ```sh
    	command: BirdEyeSystem.py -undistore
|   |   |
|:-:|:-:|
|front fisheye image |front undistorted defualt|
|<img style="margin:0px auto;display:block" width=500 src=".\BirdEyeSystem\imgs\front.png"/>|<img style="margin:0px auto;display:block" width=500 src=".\BirdEyeSystem\imgs\tests\front_undistorted_default.png"/>|

 - scaling and translation to catch the coreners(missing pixels):

|   |   |
|:-:|:-:|
|front - scale (0.5,0.5)|front - scale(0.5,0.5) & shift (200,0)|
|<img style="margin:0px auto;display:block" width=500 src=".\BirdEyeSystem\imgs\tests\front_scaleXY_0.5.png"/>|<img style="margin:0px auto;display:block" width=500 src=".\BirdEyeSystem\imgs\tests\front_scaleXY_0.5_shiftX_200.png"/>|


