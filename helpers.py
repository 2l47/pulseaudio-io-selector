#!/usr/bin/env python3

# Helper functions

from colors import *
import subprocess



# Shortcut for running pactl with the provided arguments
def pactl(args, extra=""):
	command = f"pactl {args}{extra}"
	print(GRAY + f"Running command: {command}")
	try:
		return subprocess.check_output(command, shell=True).decode("ASCII")
	except subprocess.CalledProcessError:
		return ""


def remove_sinks():
	print(BLUE + "Removing sinks we previously created...")
	# Still not cleaning up this line
	pactl("list sinks", " | grep -P 'Name: (recording|combined)(\.\d+)?|Owner Module: \d+' | grep -E 'Name: (recording|combined)' -A 1 | grep -Po '(?<=Owner Module: )\d+' | xargs -n 1 pactl unload-module")


# For more details, see pulseaudio-sinks.sh in the initial commit
def add_sinks(combined_output):
	# Create the "recording" null sink
	print(BLUE + "Creating the \"recording\" null sink...")
	pactl("load-module module-null-sink sink_name=recording sink_properties=device.description=recording")
	# Create the "combined" sink with "recording" as the primary slave and the given output as a secondary slave
	print(BLUE + "Creating the \"combined\" sink with \"recording\" as the primary slave and \"{combined_output}\" as a secondary slave...")
	pactl(f"load-module module-combine-sink sink_name=combined sink_properties=device.description=combined slaves=recording,{combined_output}")
	# If you wanted your microphone to be always-on on top of "recording", you would enable this
	#MICROPHONE = "YOUR_MICROPHONE_NAME"
	#pactl(f"load-module module-loopback source={MICROPHONE} sink=recording latency_msec=1")


# Get available sinks (outputs)
def get_outputs():
	result = pactl("list sinks", " | grep Name:")
	available = result.split()
	while "Name:" in available:
		available.remove("Name:")
	return available


# Get available sources (inputs)
def get_inputs():
	result = pactl("list sources", " | grep Name:")
	available = result.split()
	while "Name:" in available:
		available.remove("Name:")
	return available


# Returns whether SteamVR is running (should we switch to the headset?)
def vr_running():
	try:
		return subprocess.check_output("pgrep vrmonitor", shell=True)
	except subprocess.CalledProcessError:
		pass
