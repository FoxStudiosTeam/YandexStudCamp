import os

files = os.listdir("./test")

txts = []

for file in files:
    if file.endswith(".txt"):
        txts.append(file)

for txt in txts:
    with open(f"./test/{txt}") as file:
        content = file.read()
        with open(f"./test/{txt}", "w") as writer:
            sto = content.replace("0", "1", 1)
            writer.write(sto)
            writer.close()
            file.close()