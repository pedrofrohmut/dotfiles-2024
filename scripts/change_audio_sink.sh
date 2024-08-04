#!/bin/bash

# Sink names
hdmi_sink="alsa_output.pci-0000_09_00.1.hdmi-ac3-surround"
bluetooth_sink="bluez_output.08_F0_B6_68_78_50.1"
audio_card_sink="alsa_output.pci-0000_0b_00.4.analog-stereo"

# Sink list to array
mapfile -t sink_list < <(pactl list sinks short)

for x in "${sink_list[@]}"; do
    # Get the id for the bluetooth sink
    if [[ "$x" = *"$bluetooth_sink"* ]]; then
        bluetooth_id=$(echo $x | awk '{print $1}')
    fi
    # Get the id for the audio card sink
    if [[ "$x" = *"$audio_card_sink"* ]]; then
        audio_card_id=$(echo $x | awk '{print $1}')
    fi
done

default_sink=$(pactl get-default-sink)

if [[ $default_sink = $bluetooth_sink ]]; then
    new_id=$audio_card_id
else
    new_id=$bluetooth_id
fi

pactl set-default-sink $new_id

inputs_ids=$(pactl list sink-inputs short | awk '{print $1}')

for input_id in $inputs_ids; do
    pactl move-sink-input $input_id $new_id
done
