#!/usr/bin/env python3

# Configuration

VALVE_INDEX_BASE = "alsa_output.pci-0000_08_00.1."
VALVE_INDEX_DP = "alsa_output.pci-0000_08_00.1.hdmi-stereo-extra3"
VALVE_INDEX_MIC = "alsa_input.usb-Valve_Corporation_Valve_VR_Radio___HMD_Mic_46B7E4067C-LYM-01.mono-fallback"

# A card profile you want to use for audio
DEFAULT_CARD_PROFILE = "output:hdmi-stereo-extra4" # Digital Stereo (HDMI 5) Output
# Valve Index output card profile
VALVE_INDEX_CARD_PROFILE = "output:hdmi-stereo-extra3" # Digital Stereo (HDMI 4) Output
VALVE_INDEX_SURROUND_CARD_PROFILE = "output:hdmi-surround71-extra3" # Digital Surround 7.1 (HDMI 4) Output
# An unused card profile for silent fixing
UNUSED_CARD_PROFILE = "output:hdmi-stereo-extra4" # Digital Stereo (HDMI 5) Output

AIRPODS = "bluez_sink.58_0A_D4_E7_09_C5.a2dp_sink"
BT_SPEAKER = "bluez_sink.FC_58_FA_73_8C_31.a2dp_sink"

# List of outputs, in order of preference
# Get output names with "pactl list sinks"
# pulseeffects, amplifier, HDMI monitor (or Valve Index), motherboard line out
outputs = [
	VALVE_INDEX_DP,
	AIRPODS,
	BT_SPEAKER,
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

# Time between attempting to connect to Bluetooth devices.
BT_CONNECT_INTERVAL = 15.000

# Bluetooth devices to try to connect to
bluetooth_devices = [
	"FC:58:FA:73:8C:31"
]
