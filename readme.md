# Parking camera system VW Golf 2017 - (BirdEye)

equimpent to prepare:
		* (4) ELP 8mp USB Camera Wide Angle Fisheye Lens 185 Degree 4K [amazon](https://www.amazon.com/-/he/dp/B01HD1V3UO?ref=ppx_yo2ov_dt_b_product_details&th=1)
		* (4) papers of checkboard white-black (5*5), size 100cm*100cm the size of each black/white square is 20cm*20cm.


# camera calibration:
	
1. connect the camera to the pc and capture multiple images of the checkerboard pattern from different angles and positions.
	examples exists in cameraCalbiration\imgs

|   |   |   |
|:-:|:-:|:-:|
|ex1|ex2|ex3|
|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (35).png"/>|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (23).png"/>|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (19).png"/>|
script : [CaptureAndSave.html](https://github.com/majedabu/Parking-Camera-System/blob/main/cameraCalbiration/CaptureAndSave.html)


2. calbirate the camera  using OpenCV calibration method for fisheye cameras.
	<img style="margin:0px auto;display:block" width=500 src=".\cameraCalbiration\cameraCalbiration.png"/>
	script : [extractFisheyeCameraIntrinsics.py](https://github.com/majedabu/Parking-Camera-System/blob/main/cameraCalbiration/extractFisheyeCameraIntrinsics%20.py)

# image undistortion