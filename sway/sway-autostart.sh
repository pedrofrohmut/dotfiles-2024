#!/usr/bin/env bash

################################################################################
# Autostart for Sway ###########################################################
################################################################################

# --- System Tray --------------------------------------------------------------

# Japanese typing
fcitx5 &

# Network Manager
nm-applet &

# Blueman (Bluetooth)
blueman-applet &

# --- Background Apps ----------------------------------------------------------

# PolicyKit Authentication Agent (PolicyKit Authentication Agent)
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# Notification Daemon
mako &

# Color temperature (default: T 6500 t 4500)
# wlsunset -T 5700 -t 3500 -g 1.0 -S 06:00 -s 18:00 &

# Color temperature (5700 day 3500 night) (location lat:log 23.52:46.35) (brightness 100% day and 80% night)
gammastep-indicator -t 5700:3500 -l 23.52:46.35 -b 1.0:0.8 &

# Setup the background
swaybg -i $HOME/media/wallpaper/1332407.png -m stretch &
