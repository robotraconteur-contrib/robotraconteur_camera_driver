# This script generates intrinsic camera calibration parameters for a camera. The script
# uses images that were previously saved using the camera_client_capture_calibration_images.py
# script. The calibration images are loaded from the "calibration_images" directory in the
# current directory. The calibration images are used to generate the intrinsic camera
# calibration parameters using the OpenCV calibration algorithm. See
# https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html for more information on the

# This script expects a chessboard calibration landmark to be used in the calibration images. The
# chessboard should be held at various locations in the camera's field of view at different
# angles and distances.

# This script prints the intrinsic camera calibration parameters in YAML format that can be used in
# the camera info files. See the example configurations to see how to insert the calibration
# parameters into the camera info files.

import cv2
from pathlib import Path
import numpy as np
import yaml

# Chessboard parameters. This is the standard letter paper size chessboard. An example
# of a chessboard can be found at 
# https://github.com/artoolkit/artoolkit5/blob/master/doc/patterns/Calibration%20chessboard%20(US%20Letter).pdf
# Turn off printer scaling when printing the chessboard. The squares should be 3 cm on a side.
# Adjust the "square_size" parameter if the squares are a different size on the printed chessboard.

width = 7 # Number of squares in the width of the chessboard
height = 5 # Number of squares in the height of the chessboard
square_size=0.03 # Size of the squares in meters

def main():

    # Create the directory for saving the calibration images
    img_dir = Path("calibration_images")
    
    # Load the calibration images
    imgs = []
    for img_path in img_dir.glob("*.png"):
        img = cv2.imread(str(img_path))
        imgs.append(img)

    print (f"Loaded {len(imgs)} images")

    ret, mtx, dist, rvecs, tvecs, mean_error, imgs_out = _calibrate_camera_intrinsic2(imgs)

    if not ret:
        print("Calibration failed")
        return
    
    dist = dist.round(4)

    k = mtx.round(4).flatten(order='F').tolist()
    distortion_info = {
        "k1": float(dist[0]),
        "k2": float(dist[1]),
        "p1": float(dist[2]),
        "p2": float(dist[3]),
        "k3": float(dist[4])
    }

    image_size = { "width": imgs[0].shape[1], "height": imgs[0].shape[0]}

    yaml_data = {
        "calibration": {
            "image_size": image_size,
            "distortion_info": distortion_info,
            "K": k
        }
    }

    print("Calibration successful")
    print("Intrinsic camera calibration parameters:")
    print(yaml.dump(yaml_data))

    return


    # Loop over the images and display the images with the chessboard corners drawn

    for img in imgs_out:
        cv2.imshow("Image", img)
        cv2.waitKey(1000)
    
    cv2.destroyAllWindows()

# Function taken from the PyRI Open Source Teach Pendant vision module
# https://github.com/pyri-project/pyri-vision/blob/master/src/pyri/vision/camera_calibration_service/__main__.py

def _calibrate_camera_intrinsic2(images):
    # opencv_camera_calibration.py:6

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((height*width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    imgs = []

    for image in images:
                
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(image, (width, height), corners2, ret)
            imgs.append(img)
            # cv2.imshow("img", img)
            # cv2.waitKey(1000)

        else:
            print("Chessboard not found in image")
        

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    print( "total error: {}".format(mean_error/len(objpoints)) )

    return ret, mtx, dist.flatten(), rvecs, tvecs, mean_error, imgs

if __name__ == '__main__':
    main()