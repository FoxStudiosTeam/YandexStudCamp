import cv2
import numpy as np


def fix_fish_eye(rawimg,cum):
    frame_width = int(cum.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cum.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    K = np.array([[1000, 0, frame_width / 2],
                  [0, 1000, frame_height / 2],
                  [0, 0, 1]])

    dist_coeffs = np.array([-0.3, 0.1, 0, 0, 0])


    new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist_coeffs, (frame_width, frame_height), 1,
                                               (frame_width, frame_height))

    map1, map2 = cv2.initUndistortRectifyMap(K, dist_coeffs, None, new_K, (frame_width, frame_height), cv2.CV_16SC2)
    undistorted_frame = cv2.remap(rawimg, map1, map2, cv2.INTER_LINEAR)
    return undistorted_frame
