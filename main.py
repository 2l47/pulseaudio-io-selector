#!/usr/bin/env python3

# This script automatically adjusts the default input and output device for pulseaudio depending on what sinks (outputs) and sources (inputs) are available.

from colors import *
import os
import pprint
import time

from helpers import add_sinks, get_outputs, get_inputs, handle_valve_index_card_switching, pactl, remove_sinks, vr_running



# Configuration

VALVE_INDEX_DP = "alsa_output.pci-0000_08_00.1.hdmi-stereo-extra3"
VALVE_INDEX_MIC = "alsa_input.usb-Valve_Corporation_Valve_VR_Radio___HMD_Mic_46B7E4067C-LYM-01.multichannel-input"

# List of outputs, in order of preference
# Get output names with "pactl list sinks"
# pulseeffects, amplifier, HDMI monitor (or Valve Index), motherboard line out
outputs = [
	VALVE_INDEX_DP,
	"PulseEffects_apps",
	"alsa_output.usb-MONOPRICE_MONOLITH_HPA-00.iec958-stereo",
	"alsa_output.pci-0000_08_00.1.hdmi-stereo-extra4",
	"alsa_output.pci-0000_0a_00.4.analog-stereo"
]

# List of inputs, in order of preference
# Get input names with "pactl list sources"
# Valve Index, USB mic, recording, webcam, pulseeffects, amplifier, line in
inputs = [
	VALVE_INDEX_MIC,
	"alsa_input.usb-C-Media_Electronics_Inc._NEEWER_USB-200-00.iec958-stereo",
	"alsa_input.usb-046d_0990_D163B542-02.multichannel-input",
	"alsa_input.usb-046d_0990_D163B542-02.mono-fallback",
	"recording.monitor",
	"PulseEffects_apps.monitor",
	"alsa_output.usb-MONOPRICE_MONOLITH_HPA-00.iec958-stereo.monitor",
	"alsa_input.pci-0000_0a_00.4.analog-stereo"
]

# This variable tracks the current secondary slave of the combined sink.
# Yeah it's a global this is a script shut up
global CURRENT_COMBINED_SINK_OUTPUT
CURRENT_COMBINED_SINK_OUTPUT = None


def set_output_device():
	global CURRENT_COMBINED_SINK_OUTPUT
	print(BLUE + "Getting outputs...")
	available_outputs = get_outputs()
	print(f"Available output devices:\n{pprint.pformat(available_outputs)}")

	for priority in outputs:
		if priority in available_outputs:
			# Set this as the default sink (output)
			# But if VR isn't running, don't use the Valve Index speakers
			if priority == VALVE_INDEX_DP and not vr_running():
				print(ITALIC + ORANGE + "Not using the Valve Index speakers because SteamVR is not running.")
				continue
			print(RED + f"Current combined sink (output): {CURRENT_COMBINED_SINK_OUTPUT}")
			print(GREEN + f"Selecting {priority} as the default sink (output)")
			pactl(f"set-default-sink {priority}")
			# If this is the Valve Index, set the volume to 50%
			if priority == VALVE_INDEX_DP:
				pactl(f"set-sink-volume {priority} 32768")
			# Recreate the "combined" sink so that recordable applications output simultaneously on the correct default output device
			# On the first run, this will remove any sinks (outputs) we've previously created, avoiding potential duplicates
			if priority != CURRENT_COMBINED_SINK_OUTPUT:
				print(RED + f"Recreating the sink because new priority {priority} != old combined sink slave {CURRENT_COMBINED_SINK_OUTPUT}")
				remove_sinks()
				add_sinks(priority)
				CURRENT_COMBINED_SINK_OUTPUT = priority
			break


def set_input_device():
	print(BLUE + "Getting inputs...")
	available_inputs = get_inputs()
	print(f"Available input devices:\n{pprint.pformat(available_inputs)}")

	for priority in inputs:
		if priority in available_inputs:
			# Set this as the default source (input)
			# But if VR isn't running, don't use the Valve Index mic
			if priority == VALVE_INDEX_MIC and (not vr_running()):
				print(ITALIC + ORANGE + "Not using the Valve Index microphone because SteamVR is not running.")
				continue
			print(GREEN + f"Selecting {priority} as the default source (input)")
			pactl(f"set-default-source {priority}")
			# If this is our USB mic, set the gain to 11.00 dB
			if priority == "alsa_input.usb-C-Media_Electronics_Inc._NEEWER_USB-200-00.iec958-stereo":
				pactl(f"set-source-volume {priority} 99957")
			break


def handle_recording():
	print(BLUE + "Pushing applications to the combined sink...")
	# Make some applications use the "combined" sink to hear and record them
	# Spotify and VLC are always available through the "recording.monitor" source (input)
	# Adding Chromium for the Steam overlay means including Discord!
	applications_to_push = [r"spotify", r"VLC media player \(LibVLC \d\.\d+\.\d+\)", r"ZOOM VoiceEngine", r"Shairport Sync", r"Firefox"]
	app_regex = "|".join(applications_to_push)
	sink_inputs = pactl("list sink-inputs", rf" | grep -P 'Sink Input #\d+|application\.name' | grep -P '(?<=application\.name = \")({app_regex})(?=\")' -B1 | grep -Po '(?<=Sink Input #)\d+'")
	for sink_input in sink_inputs.split("\n")[:-1]:
		pactl(f"move-sink-input {sink_input} combined")


# Main program logic - just run until terminated
while True:
	# Handles switching the GPU to the correct profile, ensuring that the output is actually available for the combined sink
	handle_valve_index_card_switching()

	set_output_device()
	handle_recording()
	print()
	set_input_device()

	print(BLUE + "\nSleeping...")
	time.sleep(1)
	os.system("clear")
