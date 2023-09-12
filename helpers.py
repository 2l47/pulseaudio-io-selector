#!/usr/bin/env python3

# Helper functions

from colors import *
from definitions import *
import os
import subprocess
import time



def notify(message):
	os.system(f"notify-send pulseaudio-io-selector \"{message}\"")


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
	print(BLUE + f"Creating the \"combined\" sink with \"recording\" as the primary slave and \"{combined_output}\" as a secondary slave...")
	assert combined_output in get_outputs()
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


def handle_valve_index_card_switching():
	# Switch the graphics card audio output from the monitor speaker to the Valve Index when VR is running
	print(BLUE + "Configuring GPU DisplayPort audio output...")
	if VALVE_INDEX_MIC in get_inputs() and vr_running():
		print("Valve Index mic detected, checking card profile")
		data = pactl("list sinks", " | grep -Po '(?<=Name: |Sample Specification: |device\.profile\.name = ).*'").split("\n")
		found_dp_output = False
		for index, item in enumerate(data):
			if item.startswith("alsa_output.pci-0000_08_00.1."):
				found_dp_output = True
				sample_spec, profile = data[index + 1:index + 2 + 1] # Slice funniness
				print(f"\tName: {item}")
				print(f"\tSample spec: {sample_spec}")
				print(f"\tProfile: {profile}")
				if "float32le" in sample_spec or "192000Hz" in sample_spec:
					# We have to switch card profiles in order to get the sample rate set correctly
					print("Incompatible sample spec detected, switching card profiles")
					pactl("set-card-profile 0 output:hdmi-surround71-extra3") # Digital Surround 7.1 (HDMI 4) Output"
					time.sleep(1) # Wait a moment
		if not found_dp_output:
			print("Couldn't find the DP output; swapping card to HDMI monitor to fix")
			pactl("set-card-profile 0 output:hdmi-stereo-extra4") # Digital Stereo (HDMI 5) Output"
		# If the Valve Index is plugged in, switch GPU audio output to it
		pactl("set-card-profile 0 output:hdmi-stereo-extra3") # Digital Stereo (HDMI 4) Output"
		# Wait a moment before set_output_device() tries to recreate the "combined" sink
		time.sleep(1)
	else:
		# Otherwise, switch GPU audio output to the HDMI monitor
		pactl("set-card-profile 0 output:hdmi-stereo-extra4") # "Digital Stereo (HDMI 5) Output"
