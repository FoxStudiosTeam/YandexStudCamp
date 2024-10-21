import os
import cv2

file = "0frame+0 (3).jpg"





idx = 0
for file in os.listdir("../upper_camera_polygon"):
    if not file.endswith(".jpg"):
        continue
    label = []
    image = cv2.imread('../upper_camera_polygon/' + file)
    image = cv2.resize(image, (512, 512))

    label = [float(x) for x in open('../upper_camera_polygon/' + file.replace(".jpg", ".txt")).readline().strip().split()][1:]
    print(label)
    height, width, _ = image.shape

    center_x, center_y = width // 2, height // 2

    top_left = image[0:center_y, 0:center_x]
    tl = (label[0] * 2, label[1] * 2)

    top_right = image[0:center_y, center_x:width]
    tr = ((1 - label[2]) * 2, label[3] * 2)
    top_right = cv2.flip(top_right, 1)

    bottom_right = image[center_y:height, center_x:width]
    br = ((1 - label[4]) * 2, (1 - label[5]) * 2)
    bottom_right = cv2.flip(bottom_right, -1)

    bottom_left = image[center_y:height, 0:center_x]
    bl = (label[6] * 2, (1 - label[7]) * 2)
    bottom_left = cv2.flip(bottom_left, 0)
    
    cv2.imwrite("dataset/" + str(idx) + ".jpg", top_left)
    with open("dataset/" + str(idx) + ".txt", "w") as f: f.write(str(tl[0]) + " " + str(tl[1]))
    cv2.imwrite("dataset/" + str(idx + 1) + ".jpg", top_right)
    with open("dataset/" + str(idx + 1) + ".txt", "w") as f: f.write(str(tr[0]) + " " + str(tr[1]))
    cv2.imwrite("dataset/" + str(idx + 2) + ".jpg", bottom_right)
    with open("dataset/" + str(idx + 2) + ".txt", "w") as f: f.write(str(br[0]) + " " + str(br[1]))
    cv2.imwrite("dataset/" + str(idx + 3) + ".jpg", bottom_left)
    with open("dataset/" + str(idx + 3) + ".txt", "w") as f: f.write(str(bl[0]) + " " + str(bl[1]))
    idx += 4







