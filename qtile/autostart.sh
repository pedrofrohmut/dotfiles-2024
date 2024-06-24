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

# PolicyKit Authentication Agent (PolicyKit Authentication Agent)
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
lxsession &

# Power Manager
xfce4-power-manager &

# Load my custom theme
xrdb -merge ~/.Xresources &

if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    # Change color temperature (default: T 6500 t 4500)
    wlsunset -T 5700 -t 3500 -g 1.0 -S 06:00 -s 19:00 &

    # Wallpaper setter
    swaybg -i ~/media/wallpaper/1316292.jpeg -m fill &
else
    # Keyboard repeat dalay/rate
    xset r rate 250 25 &

    # Compositor for X11
    picom --config ~/.config/picom/picom.conf &

    # Change color temperature
    redshift-gtk &

    # Wallpaper setter
    nitrogen --restore &

    # Hide Mouse Cursor when idle for 2 seconds
    unclutter --timeout 2 --ignore-scrolling &
fi
