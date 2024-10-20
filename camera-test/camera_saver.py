import cv2 as cv

camera = cv.VideoCapture("http://192.168.2.81:8080?action=stream")
success, image = camera.read()

count = 0
while success:
    cv.imwrite("./saved/frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = camera.read()
    print('Read a new frame: ', success)
    count += 1

