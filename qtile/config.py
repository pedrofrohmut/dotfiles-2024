from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

from os import path

mod = "mod4"
terminal = "alacritty"
HOMEDIR = path.expanduser("~/")

keys = [
    ### # BSP Layout
    ### key([mod], "j", lazy.layout.down()),
    ### key([mod], "k", lazy.layout.up()),
    ### key([mod], "h", lazy.layout.left()),
    ### key([mod], "l", lazy.layout.right()),

    ### key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ### key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    ### key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    ### key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    ### key([mod, "mod1"], "j", lazy.layout.flip_down()),
    ### key([mod, "mod1"], "k", lazy.layout.flip_up()),
    ### key([mod, "mod1"], "h", lazy.layout.flip_left()),
    ### key([mod, "mod1"], "l", lazy.layout.flip_right()),

    ### key([mod, "control"], "j", lazy.layout.grow_down()),
    ### key([mod, "control"], "k", lazy.layout.grow_up()),
    ### key([mod, "control"], "h", lazy.layout.grow_left()),
    ### key([mod, "control"], "l", lazy.layout.grow_right()),

    ### key([mod, "shift"], "n", lazy.layout.normalize()),
    ### ### Key([mod], "Return", lazy.layout.toggle_split()),


    # Monal Tall Layout
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.reset()),
    Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()),


    ### # A list of available commands that can be bound to keys can be found
    ### # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    ### # Switch between windows
    ### Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    ### Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    ### Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    ### Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    #### # Move windows between left/right columns or move up/down in current stack.
    #### # Moving out of range in Columns layout will create new column.
    #### Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    #### Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    #### Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    #### Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    ### # Grow windows. If current window is on the edge of screen and direction
    ### # will be to screen edge - window would shrink.
    ### Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    ### Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    ### Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    ### Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    ### Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    # Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "a", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Alt tab for Workspaces
    Key(["mod1"], "Tab", lazy.screen.toggle_group()),
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
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    ### layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    ### layout.Bsp(),
    layout.MonadTall(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2, single_border_width=0),
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
        bottom=bar.Bar(
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
                # TODO: Make the script work and link here
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
follow_mouse_focus = True
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
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
