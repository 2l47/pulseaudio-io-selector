#!/usr/bin/env bash

cd ~/Desktop/src/pulseaudio-io-selector
tmux new -ds "pulseaudio-io-selector" "./loop.py"
