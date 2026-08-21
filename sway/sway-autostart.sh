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
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# Color temperature (default: T 6500 t 4500)
wlsunset -T 5700 -t 3500 -g 1.0 -S 06:00 -s 19:00 &
