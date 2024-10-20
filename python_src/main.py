import threading
import fs_stream_edited as camera
import time
import asyncio
threads = []
#threads.append(threading.Thread(target=camera.main, args=()))

def spam():
    while True:
        print("spam")
        time.sleep(1)

flask = threading.Thread(target= camera.main, args=(), daemon=True)




#s = threading.Thread(target= spam, args=())
#s.run()
flask.run()
spam()