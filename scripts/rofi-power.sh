#! /usr/bin/env bash

# UI Texts
POWEROFF="Poweroff"
SUSPEND="Suspend"
REBOOT="Reboot"
CANCEL="Cancel"
YES="Yes"
NO="No"

maintheme="
    listview { lines: 3; }
    window { padding: 20; width: 280; }"

confirmtheme="
    listview { lines: 3; }
    window { padding: 20; width: 280; }"

rofi_cmd() {
    rofi -i -dmenu -lines 3 -theme-str "${maintheme}" -theme ~/dotfiles/rofi/my_dracula.rasi
}

run_rofi() {
    echo -e "$POWEROFF\n$SUSPEND\n$REBOOT" | rofi_cmd
}

rofi_confirm_cmd() {
    rofi -i -dmenu -lines 3 -theme-str "${confirmtheme}" -theme ~/dotfiles/rofi/my_dracula.rasi
}

run_rofi_confirm() {
    echo -e "$CANCEL\n$NO\n$YES" | rofi_confirm_cmd
}

option="$(run_rofi)"

case $option in
    $POWEROFF )
        confirm=$(run_rofi_confirm)
        if [ $confirm = $YES ]; then
            systemctl poweroff
        fi
        ;;
    $REBOOT )
        confirm=$(run_rofi_confirm)
        if [ $confirm = $YES ]; then
            systemctl reboot
        fi
        ;;
    $SUSPEND )
        # i3lock -i ~/media/wallpaper/lock.png && systemctl suspend
        slock & systemctl suspend
        ;;
    * )
        exit
        ;;
esac
