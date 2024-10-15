import cv2 as cv

camera = cv.VideoCapture("rtsp://Admin:rtf123@192.168.2.250/251:554/1/1")
success, image = camera.read()

count = 0
while success:
    cv.imwrite("./saved_board/frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = camera.read()
    print('Read a new frame: ', success)
    count += 1

