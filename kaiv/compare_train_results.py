from math import floor
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

PATH_ROOTS = "../runs"
PATHS = [
    "release",
    "release_v2",
    "release_v3",
]
FILE = "results.csv"
COLORS = [
    'red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 
    'magenta', 'yellow', 'black', 'lime'
]

def read_csv(file_path):
    labels = []
    data = []
    label = True
    for line in open(file_path, "r"):
        epoch, box_loss, cls_loss, dfl_loss, prec, recall, map50, map50_95, vbox, vcls, vdfl, _, _, _ = line.split(",")
        if label:
            labels = [
                epoch.replace(" ", ""),
                box_loss.replace(" ", ""), 
                cls_loss.replace(" ", ""), 
                dfl_loss.replace(" ", ""), 
                prec.replace(" ", ""), 
                recall.replace(" ", ""), 
                map50.replace(" ", ""), 
                map50_95.replace(" ", ""), 
                vbox.replace(" ", ""), 
                vcls.replace(" ", ""), 
                vdfl.replace(" ", "")
            ]
        else:
            data.append(
                [
                    float(epoch),
                    float(box_loss), 
                    float(cls_loss), 
                    float(dfl_loss), 
                    float(prec), 
                    float(recall), 
                    float(map50), 
                    float(map50_95), 
                    float(vbox), 
                    float(vcls), 
                    float(vdfl)
                ]
            )
        label = False
    return labels, np.array(data)

fig, axs = plt.subplots(2, 5, figsize=(18, 6))
for i in range(len(PATHS)):
    file_path = f"{PATH_ROOTS}/{PATHS[i]}/{FILE}"
    labels, data = read_csv(file_path)
    for plot_id in range(0, 10):
        axs[floor(plot_id/5)][plot_id%5].plot(data[:, 0], data[:, plot_id+1], label=PATHS[i], color=COLORS[i])
        axs[floor(plot_id/5)][plot_id%5].legend()
        axs[floor(plot_id/5)][plot_id%5].set_title(labels[plot_id+1])



plt.show()