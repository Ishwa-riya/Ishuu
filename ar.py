# import necessary packages
import argparse
import imutils
import time
import cv2
import sys
import numpy as np
from imutils.video import VideoStream
# construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str, default="DICT_4X4_50",
                help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

# dictionary of supported ArUco tags
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# verify that the supplied ArUCo tag exists and is supported by OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
    print(f"[INFO] ArUCo tag of '{args['type']}' is not supported")
    sys.exit(0)

# load ArUCo dictionary and parameters
print(f"[INFO] detecting '{args['type']}' tags...")
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# camera calibration parameters (replace with your actual calibration)
cameraMatrix = np.array([[800, 0, 320],
                         [0, 800, 240],
                         [0, 0, 1]], dtype=np.float32)
distCoeffs = np.zeros((5, 1))  # assuming no distortion

# size of the marker in meters (adjust this value)
markerLength = 0.05  # 5 cm

# start video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=1000)

    # detect markers
    corners, ids, rejected = arucoDetector.detectMarkers(frame)

    if ids is not None:
        ids = ids.flatten()
        # estimate pose of each marker
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)

        for i in range(len(ids)):
            # draw detected markers and axis
            cv2.aruco.drawDetectedMarkers(frame, corners)
            cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], 0.03)

            # draw marker ID text
            c = corners[i][0]
            topLeft = tuple(c[0].astype(int))
            cv2.putText(frame, str(ids[i]), (topLeft[0], topLeft[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # show output frame
    cv2.imshow("AR Marker Detection", frame)
    key = cv2.waitKey(1) & 0xFF

    # exit on 'q'
    if key == ord("q"):
        break

# cleanup
cv2.destroyAllWindows()
vs.stop()