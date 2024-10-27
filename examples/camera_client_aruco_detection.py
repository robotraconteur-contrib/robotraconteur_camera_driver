# This example demonstrates how to detect ArUco markers in a camera stream.

# Simple example Robot Raconteur standard camera client
# This program will capture a single compressed frame and
# display it.

# Press any key to exit

from RobotRaconteur.Client import *
from RobotRaconteurCompanion.Util.ImageUtil import ImageUtil

import cv2
import sys
import traceback
import argparse
import numpy as np
import traceback
from cv2 import aruco


def main():

    # Get the aruco dict and params
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    aruco_params = aruco.DetectorParameters()
    aruco_params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX

    # URL for connecting to the camera
    url = 'rr+tcp://localhost:59823?service=camera'
    if (len(sys.argv) >= 2):
        url = sys.argv[1]

    # Connect to the camera
    cam = RRN.ConnectService(url)

    # Create an ImageUtil object to help with image conversion
    image_util = ImageUtil(RRN, cam)

    cv2.namedWindow("Detected Markers")

    while True:
        # Capture the compressed frame from the camera, returns in PNG format
        raw_frame = cam.capture_frame_compressed()

        # Convert raw_frame to opencv format using companion library ImageUtil
        current_frame = image_util.compressed_image_to_array(raw_frame)

        # Detect the markers
        corners1, ids1, rejected = cv2.aruco.detectMarkers(current_frame, aruco_dict, parameters=aruco_params)

        # Draw the detected markers
        current_frame2 = cv2.aruco.drawDetectedMarkers(current_frame, corners1, ids1)

        # This example does not attempt to estimate the pose of the markers,
        # but the corners and ids can be used to estimate the pose using cv2.aruco.estimatePoseSingleMarkers
        
        cv2.imshow("Detected Markers", current_frame2)
        ret = cv2.waitKey(50)
        if ret != -1:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
