import os
import numpy as np
import cv2

# Define the size of the checkerboard (number of inner corners)
checkerboard_size = (8, 6)  # Change this to match your checkerboard pattern
grid_points = np.zeros((1, np.prod(checkerboard_size), 3), np.float32)
grid_points[0, :, :2] = np.indices(checkerboard_size).T.reshape(-1, 2)

# Create arrays to store object points (3D points of checkerboard corners) and image points (2D points in the image)
object_points = []  # 3D points in real-world space
image_points = []  # 2D points in the image

# Generate object points for the corners of the checkerboard
objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)

# Path to the folder containing your PNG images
image_folder = 'imgs'

# List all PNG files in the folder
image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if
               filename.endswith(".png")]

objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane


for image_path in image_paths:

    # Load the PNG image
    image = cv2.imread(image_path)

    print("searching for chessboard corners in captured image " + image_path + "...")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    found, corners = cv2.findChessboardCorners(
        gray,
        checkerboard_size,
        cv2.CALIB_CB_ADAPTIVE_THRESH +
        cv2.CALIB_CB_NORMALIZE_IMAGE +
        cv2.CALIB_CB_FILTER_QUADS
    )

    if found:
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.01)
        cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), term)
        imgpoints.append(corners)
        objpoints.append(grid_points)


N_OK = len(objpoints)
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N_OK)]
calibration_flags = (cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC +
                     cv2.fisheye.CALIB_CHECK_COND +
                     cv2.fisheye.CALIB_FIX_SKEW)

ret, mtx, dist, rvecs, tvecs = cv2.fisheye.calibrate(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    K,
    D,
    rvecs,
    tvecs,
    calibration_flags,
    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
)

if ret:

    # Print the camera matrix and distortion coefficients
    print("Camera Matrix:")
    print(K)
    print("\nDistortion Coefficients:")
    print(D)

    # Optionally, you can save the camera matrix and distortion coefficients to a file
    np.savez("calibration.npz", camera_matrix=K, dist_coeffs=D)

    # Close any open OpenCV windows
    cv2.destroyAllWindows()
