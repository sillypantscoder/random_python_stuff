#full

import subprocess
import os
import threading
import time

def start(filename):
	subprocess.run(["python3", "weirdimage.py", "images/" + filename])
	subprocess.run(["cp", "weird.png", "weirdimages/" + filename])
	#subprocess.Popen(["python3", "imageviewer.py", "weirdimages/" + filename])

imgs = os.listdir("images")
for filename in imgs:
	threading.Thread(target=start, args=(filename,), name=f"processing image {filename}").start()
	while threading.active_count() >= 4:
		time.sleep(1)
