# Robot Raconteur Camera Driver

The `robotraconteur-camera-driver` package provides a camera driver for Robot Raconteur based on OpenCV video
capture. See the [OpenCV documentation](https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html)
for more information on the video capture system and its capabilities. The driver allows for selecting the camera
by index, and changing some of the parameters made available by OpenCV. OpenCV does not provide a mechanism to
enumerate cameras and their capabilities so there is no option to list available cameras.

This driver uses the `com.robotraconteur.imaging.Camera` standard type.

Install using Python pip (Windows, Mac, Linux) or using Docker (Linux).

## Connection Info

The default connection information is as follows. These details may be changed using `--robotraconteur-*` command
line options when starting the service. Also see the
[Robot Raconteur Service Browser](https://github.com/robotraconteur/RobotRaconteur_ServiceBrowser) to detect
services on the network.

- URL: `rr+tcp://localhost:59823?service=camera`
- Device Name: `camera` or device name in the configuration file
- Node Name: `com.robotraconteur.imaging.camera`
- Service Name: `camera`
- Root Object Type:
  - `com.robotraconteur.imaging.Camera`

## Installation

Install using Python pip

```
python -m pip install robotraconteur-camera-driver
```

On Linux use `python3` instead of `python`. On Ubuntu the `python3-pip` apt package must be installed
to use python pip.

See the Docker section for installation instructions using docker.

## Usage

Example usage:

    python -m robotraconteur_camera_driver --camera-info-file=config/generic_webcam_1080p_default_camera_info.yml --width=1280 --height=720 --fps=20 --device-id=0

On Ubuntu, use `python3` instead of `python`

## Command Line Options

The following command line arguments are available:

- `--camera-info-file=` - The camera info file. Info files are available in the `config/` directory. See [camera info file documentation](https://github.com/robotraconteur/robotraconteur_standard_robdef/blob/master/docs/info_files/camerainfo.md). Also see `camera_client_calibrate_intrinsic.py` example.
- `--device-id=` - The Device ID used to identify the camera. Default is 0. Passed to the OpenCV Video Capture creation function.
- `--width=` - Captured image width (OpenCV `CAP_PROP_FRAME_WIDTH`)
- `--height=` - Captured image height (OpenCV `CAP_PROP_FRAME_HEIGHT`)
- `--fps=` - Frames per second (OpenCV `CAP_PROP_FPS`)
- `--focus=` - Camera focus (OpenCV `CAP_PROP_FOCUS`)
- `--exposure=` - Camera exposure (OpenCV `CAP_PROP_EXPOSURE`)
- `--gain=` - Camera gain (OpenCV `CAP_PROP_GAIN`)
- `--brightness=` - Camera brightness (OpenCV `CAP_PROP_BRIGHTNESS`)
- `--contrast=` - Camera contrast (OpenCV `CAP_PROP_CONTRAST`)
- `--saturation=` - Camera saturation (OpenCV `CAP_PROP_SATURATION`)

See the [OpenCV Video Capture](https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html) and [OpenCV Video Capture Properties](https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d) documentation for more information on these options.

The `focus`, `exposure`, `gain`, `brightness`, `contrast`, and `saturation` properties can be changed by the client using the `setf_param` function
during runtime. All parameters are scalar double types. For example:

```python
# camera_client connected using RRN.ConnectService
focus_value=10
camera_client.setf_param("focus", RR.VarValue(focus_value, "double"))
```

All Robot Raconteur node setup command line options are supported. See [Robot Raconteur Node Command Line Options](https://github.com/robotraconteur/robotraconteur/wiki/Command-Line-Options)

By default the node listens on TCP port 59823 and have the NodeName com.robotraconteur.imaging.Camera. If there are multiple cameras, it will be necessary to change these two values for each additional camera. These can be overridden using Robot Raconteur node setup command line options. An additional camera info file with a different device name is also needed. For example,

    python robotraconteur_camera_driver.py --camera-info-file=config/generic_webcam_1080p_default_camera_info2.yml --width=1280 --height=720 --fps=20 --device-id=1 --robotraconteur-tcp-port=54444 --robotraconteur-node-name=camera2

## Examples

The following examples can be found in the `examples/` directory:

- `camera_client_capture_frame.py` - Basic example to capture and display a single frame
- `camera_client_capture_frame_compressed.py` - Capture and display a frame from the camera using a compressed format. The compressed image is more efficient to transfer but requires additional computational power to compress the image. Lossless PNG is used to compress the image.
- `camera_client_image.py` - Stream full resolution uncompressed images
- `camera_client_image_preview.py` - Stream "preview" images, which are mjpeg compressed and reduced resolution for live preview use only
- `camera_client_aruco_detection.py` - Example of streaming detection of ArUco markers
- `camera_client_capture_calibration_images.py` and `camera_client_calibrate_intrinsic.py` - Examples capturing images and generating intrinsic calibration parameters. Outputs Yaml format compatible with info files.

## Docker Usage

```
sudo docker run --rm --net=host --privileged -v /var/run/robotraconteur:/var/run/robotraconteur -v /var/lib/robotraconteur:/var/lib/robotraconteur wasontech/robotraconteur-camera-driver --camera-info-file=config/generic_webcam_1080p_default_camera_info.yml --width=1280 --height=720 --fps=20 --device-id=0
```

It may be necessary to mount a docker "volume" to access configuration yml files that are not included in the docker image.
See the docker documentation for instructions on mounting a local directory as a volume so it can be accessed inside the docker.

## License

License: Apache 2.0

Author: John Wason, PhD

## Acknowledgment

This work was supported in part by the Advanced Robotics for Manufacturing ("ARM") Institute under Agreement Number W911NF-17-3-0004 sponsored by the Office of the Secretary of Defense. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of either ARM or the Office of the Secretary of Defense of the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for Government purposes, notwithstanding any copyright notation herein.

This work was supported in part by the New York State Empire State Development Division of Science, Technology and Innovation (NYSTAR) under contract C160142.

![](https://github.com/robotraconteur/robotraconteur/blob/master/docs/figures/arm_logo.jpg?raw=true)
![](https://github.com/robotraconteur/robotraconteur/blob/master/docs/figures/nys_logo.jpg?raw=true)
