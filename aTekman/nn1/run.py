from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load an official model
results = model("https://ultralytics.com/images/bus.jpg")

print("cls list:", results[0].names)

for box in results[0].boxes:
    print(box.cls[0])