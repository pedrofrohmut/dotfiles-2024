#!/bin/bash

# Sink
sink_name="alsa_output.pci-0000_0b_00.4.analog-stereo"

# Ports
lineout_port="analog-output-lineout"
headphones_port="analog-output-headphones"
active_port=$(pactl list sinks | grep "Active Port:" | awk -F ": " '{print $2}')

if [ "$active_port" = "$headphones_port" ]; then
    pactl set-sink-port $sink_name $lineout_port
else
    pactl set-sink-port $sink_name $headphones_port
fi
