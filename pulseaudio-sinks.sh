#!/usr/bin/env bash

# Log the commands run
set -x


# ======== Section 1 ========

# Create our null sink, named "recording".

# 1. Applications that output to the "combined" sink in the next section will
# 	have their output forwarded into this null sink.
# 2. The "combined" sink will also output its received audio to the headphones,
# 	so that you can still hear what you are "recording".
# 3. In the third section, we use a loopback module to push microphone input
# 	into the recording sink. This allows for the recording sink to provide
# 	output from the microphone.
# 4. With these three things done, you can then set "recording.monitor" as an
# 	input device which provides your recorded applications as well as your
# 	recorded microphone, while still being able to hear your recorded
# 	applications through your headphones.

pactl load-module module-null-sink sink_name=recording \
	sink_properties=device.description=recording


# ======== Section 2 ========

# Now we're going to create our combining sink.

# 1. This combining sink will pass whatever it receives into the "recording"
# 	sink as well as into the headphones.
# 2. By doing this, you can still hear what is being captured by the recording
# 	sink.
# 3. In other words, this combining sink is where you will direct applications
# 	that you want to capture.

# Insert the name of your preferred output device here.
export HEADPHONES="alsa_output.usb-MONOPRICE_MONOLITH_HPA-00.iec958-stereo"
pactl load-module module-combine-sink sink_name=combined \
	sink_properties=device.description=combined \
	slaves=recording,$HEADPHONES


# ======== Section 3: Recording microphone output  ========

# Here, we use a loopback module to push microphone output into the recording sink.

# Insert the name of your preferred input device here.
#export MICROPHONE="alsa_input.usb-C-Media_Electronics_Inc._NEEWER_USB-200-00.iec958-stereo"
#pactl load-module module-loopback source=$MICROPHONE sink=recording latency_msec=1


# ======== Section 4: Usage ========

# Simply select the "recording.monitor" sink as the input device wherever you
# 	want to stream/record the application and microphone inputs.
