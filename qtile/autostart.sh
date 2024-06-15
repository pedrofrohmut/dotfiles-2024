#! /usr/bin/bash

################################################################################
# Autostart for Qtile ##########################################################
################################################################################

# --- ENV ----------------------------------------------------------------------
# Set env on the file '/etc/environment'. But keep them commented here for reference
# variable dont work on this file. like $PATH and $HOME

#export GTK_IM_MODULE=fcitx
#export QT_IM_MODULE=fcitx
#export XMODIFIERS=@im=fcitx

#export SHELL=/usr/bin/zsh
#export EDITOR=/usr/local/bin/nvim
#export GIT_EDITOR=/usr/local/bin/nvim
#export PATH=$PATH:$HOME/.local/bin

# --- System Tray --------------------------------------------------------------

# Japanese typing
fcitx5 &

# Network (Manage your network connections)
nm-applet &

# --- Background Apps ----------------------------------------------------------

# Change color temperature
wlsunset -T 5700 -t 3500 -g 1.0 -S 06:00 -s 19:00 &  ### My pref/recommend temp
#wlsunset -T 6500 -t 4500 -g 0.9 -S 06:00 -s 19:00 & ### My preference temp
#wlsunset -l 23.52 -L 46.35 -T 5700 -t 3500 &        ### Temp Recommend

# PolicyKit Authentication Agent (PolicyKit Authentication Agent)
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

swaybg -i ~/media/wallpaper/1316292.jpeg -m fill &
