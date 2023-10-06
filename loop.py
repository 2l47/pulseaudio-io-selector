#!/usr/bin/env python3

import os
import sys
import time

from helpers import notify



# Is there an instance running already?
try:
	f = open("loop.pid", "r")
	f.close()
	raise RuntimeError("ERROR: An instance of loop.py is already running!")
except FileNotFoundError as ex:
	pass


# Write our PID to the file so we can kill the loop externally if necessary
with open("loop.pid", "w") as f:
	f.write(str(os.getpid()))


print("Starting loop...")
try:
	while True:
		os.system(f"python3 ./main.py {' '.join(sys.argv[1:])}")
		notify("Relaunching pulseaudio-selector in 5 seconds...", title="pulseaudio-io-selector loop", duration=5000)
		time.sleep(5)
		notify("Relaunching pulseaudio-selector.", title="pulseaudio-io-selector loop", duration=2500)
except:
	raise
finally:
	print("Loop ending.")
	os.remove("loop.pid")
