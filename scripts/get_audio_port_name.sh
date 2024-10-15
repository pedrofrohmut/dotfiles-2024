#!/bin/bash

sleep 0.3

# Sink
sink_name="alsa_output.pci-0000_0b_00.4.analog-stereo"

# Ports
lineout_port="analog-output-lineout"
headphones_port="analog-output-headphones"
active_port=$(pactl list sinks | grep "Active Port:" | awk -F ": " '{print $2}')

if [ "$active_port" = "$headphones_port" ]; then
    echo "Headphones"
else
    echo "Speakers"
fi
