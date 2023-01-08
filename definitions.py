#!/usr/bin/env python3

# Configuration

VALVE_INDEX_DP = "alsa_output.pci-0000_08_00.1.hdmi-stereo-extra3"
VALVE_INDEX_MIC = "alsa_input.usb-Valve_Corporation_Valve_VR_Radio___HMD_Mic_46B7E4067C-LYM-01.multichannel-input"

BT_SPEAKER = "bluez_sink.FC_58_FA_73_8C_31.a2dp_sink"

# List of outputs, in order of preference
# Get output names with "pactl list sinks"
# pulseeffects, amplifier, HDMI monitor (or Valve Index), motherboard line out
outputs = [
	VALVE_INDEX_DP,
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
BT_INTERVAL = 1.000

# Bluetooth devices to try to connect to
bluetooth_devices = [
	"FC:58:FA:73:8C:31"
]
