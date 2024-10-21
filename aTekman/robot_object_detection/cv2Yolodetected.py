import cv2
from ultralytics import YOLO

model = YOLO('C:\\Users\\weednw\\PycharmProjects\\YandexStudCamp\\aTekman\\robot_object_detection\\src\\runs\\detect\\train16\\weights\\best.pt')

class_names = model.names
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    if not ret:
        print("кадр не получен")
        break

    results = model(frame)
    for result in results:
        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])

            if class_id < len(class_names):
                class_name = class_names[class_id]
            else:
                class_name = "Unknown"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name} (ID: {class_id}), Conf: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
