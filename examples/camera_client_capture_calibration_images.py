# Capture a series of calibration images from a camera. These images are saved
# in a subdirectory "calibration_images" in the current directory. These
# images are then used to calibrate the camera using the OpenCV calibration
# in the camera_client_calibrate_camera.py example.

# A live preview is displayed from the camera. Press "enter" or any
# letter key to capture an image. Press "q" to exit the program.
# The images are saved in the "calibration_images" directory.

# Move the landmark to various locations in the camera's field of view to
# capture a variety of images. The landmark should be placed at different
# distances from the camera and at different angles.

from RobotRaconteur.Client import *
from RobotRaconteurCompanion.Util.ImageUtil import ImageUtil

import cv2
import sys
import traceback
import argparse
import numpy as np
import traceback
from pathlib import Path

def main():

    # Create the directory for saving the calibration images
    img_dir = Path("calibration_images")
    img_dir.mkdir(exist_ok=True)

    # URL for connecting to the camera
    url = 'rr+tcp://localhost:59823?service=camera'
    if (len(sys.argv) >= 2):
        url = sys.argv[1]

    # Connect to the camera
    cam = RRN.ConnectService(url)

    # Create an ImageUtil object to help with image conversion
    image_util = ImageUtil(RRN, cam)

    i = 0

    while True:

        # Capture the compressed frame from the camera, returns in PNG format
        raw_frame = cam.capture_frame_compressed()

        # Convert raw_frame to opencv format using companion library ImageUtil
        current_frame = image_util.compressed_image_to_array(raw_frame)

        
        cv2.namedWindow("Image")

        cv2.imshow("Image", current_frame)
        rv = cv2.waitKey(10)
        if rv == ord('q'):
            break
        if rv != -1:
            with open(img_dir / f"calibration_image_{i}.png", "wb") as f:
                f.write(raw_frame.data.tobytes())
            i+=1

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()