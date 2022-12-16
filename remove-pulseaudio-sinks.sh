#!/usr/bin/env bash

# Log the commands run
set -x

# I'm not cleaning up this line.
pactl list sinks | grep -P 'Name: (recording|combined)(\.\d+)?|Owner Module: \d+' | grep -E 'Name: (recording|combined)' -A 1 | grep -Po '(?<=Owner Module: )\d+' | xargs -n 1 pactl unload-module
