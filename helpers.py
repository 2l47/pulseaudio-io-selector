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
