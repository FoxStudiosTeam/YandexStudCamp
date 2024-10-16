from ultralytics import YOLO


model_labels = [
    "yolov8n.pt",
    "yolov8s.pt",
    "yolov9t.pt",
    "yolov9s.pt",
    "yolov10n.pt",
    "yolov10s.pt",
    "yolov10m.pt",
    "yolo11n.pt",
    "yolo11s.pt",
]

models = []

for model_label in model_labels:
    models.append((YOLO(model_label), model_label))


results = []
for (model, name) in models:
    result = model("https://ultralytics.com/images/bus.jpg")
    a, b, c = \
        result[0].speed["preprocess"], \
        result[0].speed["inference"], \
        result[0].speed["postprocess"]
    results.append((a + b + c, name))
    print(f"""Model: {name} takes 
\tpreprocess  : {a}
\tinference   : {b}
\tpostprocess : {c}
\tsumm        : {a + b + c}\n\n
""")
results.sort(key=lambda x: x[0])
for i, result in enumerate(results):
    print(f"#{i+1}: {result[1]} - {round(result[0]*100)/100}ms")

