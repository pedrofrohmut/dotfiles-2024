from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

import subprocess
import os
from types import SimpleNamespace

mod = "mod4"
terminal = "alacritty"
calculator = "galculator"
HOMEDIR = os.path.expanduser("~/")

# My bash commands
cmd = SimpleNamespace(
    vol_up = "pactl set-sink-volume @DEFAULT_SINK@ +5%",
    vol_down = "pactl set-sink-volume @DEFAULT_SINK@ -5%",
    rofi_apps = "rofi -show drun -show-icons -theme ~/dotfiles/rofi/my_dracula.rasi",
    rofi_run = "rofi -show run -theme ~/dotfiles/rofi/my_dracula.rasi",
    rofi_power = "bash -c ~/dotfiles/scripts/rofi-power.sh",
    change_port = "bash -c ~/dotfiles/scripts/change_audio_port.sh",
    get_port_name = "bash -c ~/dotfiles/scripts/get_audio_port_name.sh",
    firefox = "bash -c 'command -v firefox >/dev/null 2>&1 && firefox || flatpak run org.mozilla.firefox'",
)

@lazy.function
def my_minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

@lazy.function
def my_move_window(qtile, direction):
    if qtile.current_window.floating:
        match direction:
            case "left":
                qtile.current_window.move_floating(-20, 0)
            case "down":
                qtile.current_window.move_floating(0, 20)
            case "up":
                qtile.current_window.move_floating(0, -20)
            case "right":
                qtile.current_window.move_floating(20, 0)
    else:
        match direction:
            case "left":
                qtile.current_layout.swap_left()
            case "down":
                qtile.current_layout.shuffle_down()
            case "up":
                qtile.current_layout.shuffle_up()
            case "right":
                qtile.current_layout.swap_right()

@lazy.function
def my_resize_window(qtile, direction):
    if qtile.current_window.floating:
        match direction:
            case "left":
                qtile.current_window.resize_floating(-20, 0)
            case "down":
                qtile.current_window.resize_floating(0, 20)
            case "up":
                qtile.current_window.resize_floating(0, -20)
            case "right":
                qtile.current_window.resize_floating(20, 0)
    else:
        match direction:
            case "left":
                qtile.current_layout.shrink_main()
            case "down":
                qtile.current_layout.grow()
            case "up":
                qtile.current_layout.shrink()
            case "right":
                qtile.current_layout.grow_main()

# Function to get the output of a shell command
def get_command_output(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

# Call my bash scripts to change port input and to get the name of the current input
def my_change_port():
    qtile.cmd_spawn(cmd.change_port)
    port_name = get_command_output(cmd.get_port_name)
    vol_txt.update(port_name)

# Call my bash scripts to change port input and to get the name of the current input
# Version made to be used on the Keys (keybinds) context
def my_change_port_keys(qtile):
    qtile.cmd_spawn(cmd.change_port)
    port_name = get_command_output(cmd.get_port_name)
    vol_txt.update(port_name)

# Get the port name to initialize the widget
initial_port_name = get_command_output(cmd.get_port_name)

# My custom Text widget to show current Audio Port and change it on click
vol_txt = widget.TextBox(text=initial_port_name, name="vol_txt")
vol_txt.mouse_callbacks = { "Button1": my_change_port }
vol_txt.update_interval = 0.5

@lazy.function
def my_next_layout(qtile):
    qtile.next_layout()

keys = [
    # Move focus between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.group.next_window()),
    Key([mod], "k", lazy.group.prev_window()),
    Key([mod, "shift"], "n", lazy.layout.next()),

    # Move window
    Key([mod, "shift"], "h", my_move_window("left")),
    Key([mod, "shift"], "j", my_move_window("down")),
    Key([mod, "shift"], "k", my_move_window("up")),
    Key([mod, "shift"], "l", my_move_window("right")),

    # Resize window
    Key([mod, "control"], "h", my_resize_window("left")),
    Key([mod, "control"], "j", my_resize_window("down")),
    Key([mod, "control"], "k", my_resize_window("up")),
    Key([mod, "control"], "l", my_resize_window("right")),
    Key([mod], "m", lazy.layout.reset()),

    # Switch between groups
    Key([mod], "p",      lazy.screen.prev_group()),
    Key([mod], "n",      lazy.screen.next_group()),
    Key([mod], "Tab",    lazy.screen.toggle_group()),
    Key(["mod1"], "Tab", lazy.screen.toggle_group()),

    # Layout control
    Key([mod], "u", lazy.window.toggle_minimize()),
    Key([mod], "i", lazy.window.toggle_floating()),
    Key([mod], "o", lazy.window.bring_to_front()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "b", lazy.hide_show_bar()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod,  "shift"], "u", my_minimize_all()),

    # Qtile
    Key([mod, "shift"], "q",   lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    # Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod, "control"], "x",  lazy.spawn(cmd.rofi_power)),

    # Programs
    Key([mod], "r",          lazy.spawn(cmd.rofi_run)),
    Key([mod, "shift"], "r", lazy.spawncmd()),
    Key([mod], "w",          lazy.spawn(cmd.firefox)),
    Key([mod], "e",          lazy.spawn("thunar")),
    Key([mod], "y",          lazy.spawn(cmd.rofi_apps)),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod, "shift"], "y", lazy.spawn("xfce4-appfinder")),

    # Sound
    Key([mod], "equal", lazy.spawn(cmd.vol_up)),
    Key([mod], "minus", lazy.spawn(cmd.vol_down)),

    # TODO: make a different function for this context
    # Key([mod], "0",     lazy.spawn(cmd.change_port)),
    Key([mod], "0",  lazy.function(my_change_port_keys)),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

#############################################################################################
# Groups ####################################################################################
#############################################################################################

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False)),
    ])

#############################################################################################
# Layouts ###################################################################################
#############################################################################################

layouts = [
    layout.MonadTall(
        border_focus="#3a3b4c",
        border_normal="#1a1b2c",
        border_width=2,
        single_border_width=0,
        change_ratio=0.02,
        margin=0,
    ),
    layout.Max(),
]

#############################################################################################
# ScratchPads ###############################################################################
#############################################################################################

groups.append(ScratchPad("scratchpad", [
    DropDown("term", terminal, width=0.8, height=0.8, y=0.08, opacity=1),
    DropDown("calc", calculator, width=0.2, height=0.4, y=0.3, x=0.3, opacity=1),
]))

keys.extend([
    Key([mod], "t", lazy.group["scratchpad"].dropdown_toggle("term")),
    Key([mod], "c", lazy.group["scratchpad"].dropdown_toggle("calc")),
])

#############################################################################################
# Bar and Widgets ###########################################################################
#############################################################################################

widget_defaults = dict(font="FiraMono Nerd Font", fontsize=11, padding=3, background="1a1b2ccc")
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active="00ffff", inactive="bababa", fontsize=11,
                    highlight_method="line", highlight_color="005757",
                    disable_drag=True
                ),
                widget.Prompt(),
                widget.TaskList(
                    fontsize=13, font="FiraMono Nerd Font", foreground="aaaabb",
                    highlight_method="border", border="666666", border_width=1,
                    margin_x=20, padding_x=10, padding_y=2, spacing=20, icon_size=0,
                    # Takes a slice of the first 25 characters to make it short to fit
                    parse_text=lambda x : x[:25]
                ),
                widget.CurrentLayout(
                    font="FiraMono Nerd Font", fontsize=12, padding=8, mouse_callbacks = { "Button1": my_next_layout }
                ),
                widget.Sep(padding=20),
                vol_txt, # My custom widget to change default sink
                widget.Sep(padding=20),
                widget.Volume(fmt='Vol: {}', step=5, update_interval=0.4),
                widget.Sep(padding=20),
                widget.CPU(format="CPU: {load_percent}%", update_interval=3.0),
                widget.Sep(padding=20),
                widget.Memory(format="RAM: {MemPercent}%", update_interval=3.0),
                widget.Sep(padding=20),
                widget.Clock(format="%d/%m/%Y [%a]", update_interval=60.0),
                widget.Clock(format="%R", update_interval=1.0, foreground="00ffff"),
                widget.Sep(padding=20),
                widget.Systray(icon_size=14, padding=8), ### Doesnt work on wayland
            ],
            24,
        ),
    ),
]

#############################################################################################
# Options ###################################################################################
#############################################################################################

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="galculator"),
        Match(wm_class="xfce4-appfinder"),
        Match(wm_class="Blueman-manager"),
    ],
    border_focus="#3a3b4c",
    border_normal="#1a1b2c",
    border_width=2,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 28

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

#############################################################################################
# Hooks #####################################################################################
#############################################################################################

@hook.subscribe.startup_once
def start_once():
    subprocess.call([HOMEDIR + '/dotfiles/qtile/autostart.sh'])
