from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

import subprocess
import os

mod = "mod4"
terminal = "alacritty"
HOMEDIR = os.path.expanduser("~/")

@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

keys = [
    # Move focus between windows
    Key([mod], "h",     lazy.layout.left()),
    Key([mod], "l",     lazy.layout.right()),
    Key([mod], "j",     lazy.layout.down()),
    Key([mod], "k",     lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    # Change window position on the current group
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Resize window size
    Key([mod, "control"], "h", lazy.layout.grow()),
    Key([mod, "control"], "l", lazy.layout.shrink()),
    Key([mod, "control"], "n", lazy.layout.normalize()),
    Key([mod, "shift"], "n",   lazy.layout.reset()),
    Key([mod], "o",            lazy.layout.maximize()),

    # Move floating windows
    Key([mod, "shift"], "Left",  lazy.window.move_floating(-10, 0)),
    Key([mod, "shift"], "Right", lazy.window.move_floating(10, 0)),
    Key([mod, "shift"], "Up",    lazy.window.move_floating(0, -10)),
    Key([mod, "shift"], "Down",  lazy.window.move_floating(0, 10)),

    # Resize floating windows
    Key([mod, "control"], "Left",  lazy.window.resize_floating(-10, 0)),
    Key([mod, "control"], "Right", lazy.window.resize_floating(10, 0)),
    Key([mod, "control"], "Up",    lazy.window.resize_floating(0, -10)),
    Key([mod, "control"], "Down",  lazy.window.resize_floating(0, 10)),

    # Switch between groups
    Key([mod], "p",      lazy.screen.prev_group()),
    Key([mod], "n",      lazy.screen.next_group()),
    Key([mod], "Tab",    lazy.screen.toggle_group()),
    Key(["mod1"], "Tab", lazy.screen.toggle_group()),

    # Layout control
    Key([mod], "i",              lazy.window.toggle_floating()),
    Key([mod], "o",              lazy.window.bring_to_front()),
    Key([mod], "u",              lazy.window.toggle_minimize()),
    Key([mod,  "shift"], "u",    minimize_all()),
    Key([mod], "b",              lazy.hide_show_bar()),
    Key([mod], "m",              lazy.next_layout()),
    Key([mod, "shift"], "space", lazy.layout.toggle_split()),
    ### Key([mod, "shift"], "space", lazy.layout.flip()),
    ### Key([mod], "f", lazy.window.toggle_fullscreen()),

    # Qtile
    Key([mod], "Return",       lazy.spawn(terminal)),
    Key([mod, "shift"], "q",   lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r",            lazy.spawncmd()),
    Key([mod, "shift"], "F3",  lazy.spawn("systemctl suspend")),

    # Programs
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "w",      lazy.spawn("firefox")),
    Key([mod], "e",      lazy.spawn("thunar")),
    Key([mod], "c",      lazy.spawn("galculator")),
    Key([mod], "y",      lazy.spawn("xfce4-appfinder")),

    # Sound
    Key([mod], "equal", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([mod], "minus", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([mod], "0",     lazy.spawn("bash {0}/dotfiles/scripts/new_change_sink.sh".format(HOMEDIR))),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend( [
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

layouts = [
    ### layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    ### layout.Bsp(),
    # layout.MonadTall(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2, single_border_width=0),
    layout.MonadTall(
        border_focus="#3a3b4c", 
        border_normal="#1a1b2c",
        border_focus_stack=["#d75f5f", "#8f3d3d"], 
        border_width=2,
        single_border_width=0
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Stack(num_stacks=2),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(active="00ffff", inactive="bababa", fontsize=14,
                        highlight_method="line", highlight_color="005757"),
                widget.Prompt(),
                widget.TaskList(fontsize=13, font="Fira Code",
                        foreground="aaaabb", highlight_method="block", border="343434",
                        margin_x=10, padding_x=2, spacing=4, parse_text=lambda x : x[:25]),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Volume(fmt='Vol: {}', step=5, update_interval=0.4, mouse_callbacks={
                    'Button1': lazy.spawn("bash {0}/dotfiles/scripts/new_change_sink.sh".format(HOMEDIR)) 
                }),
                widget.Sep(padding=20),
                widget.Clock(format="%d/%m/%Y [%a]", update_interval=60.0),
                widget.Sep(padding=20),
                widget.Clock(format="%R", update_interval=1.0, foreground="00ffff"),
                widget.Sep(padding=20),
                widget.Systray(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

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
    ]
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

# @hook.subscribe.startup_once
# def start_once():
#     subprocess.call("bash {0}/dotfiles/qtile/autostart.sh".format(HOMEDIR))

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/dotfiles/qtile/autostart.sh'])

