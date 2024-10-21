import cv2 as cv2
import numpy as np

camera = cv2.VideoCapture("rtsp://Admin:rtf123@192.168.2.250/251:554/1/1")
success, image = camera.read()

frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = camera.get(cv2.CAP_PROP_FPS)
total_frames = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))

K = np.array([[1000, 0, frame_width / 2],
              [0, 1000, frame_height / 2],
              [0, 0, 1]])

dist_coeffs = np.array([-0.3, 0.1, 0, 0, 0])


new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist_coeffs, (frame_width, frame_height), 1,
                                           (frame_width, frame_height))

map1, map2 = cv2.initUndistortRectifyMap(K, dist_coeffs, None, new_K, (frame_width, frame_height), cv2.CV_16SC2)


count = 0
while success:
    undistorted_frame = cv2.remap(image, map1, map2, cv2.INTER_LINEAR)

    cv2.imwrite("./saved_board/frame%d.jpg" % count, undistorted_frame)     # save frame as JPEG file
    success,image = camera.read()
    print('Read a new frame: ', count)
    count += 1

