# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # Move windows up or down in current stack
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    # grow up the ratio of current stack
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod], "n", lazy.layout.normalize()),

    # Switch window focus to other pane(s) of stack
    Key(['mod1'], "Tab", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod], "Tab", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key( [mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Utils
    #Key(['control'], "Escape", lazy.spawn('xterm -rv')),
    Key([mod], "Escape", lazy.spawn('terminology')),
    Key(['control'], "Escape", lazy.spawn('yakuake')),
    Key([mod], "l", lazy.spawn('dolphin')),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),
    Key(['mod1'], "q", lazy.window.kill()),
    Key(['control'], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key(["control"], "space", lazy.spawncmd()),

    # Function keys
    Key([], 'XF86MonBrightnessUp', lazy.spawn("xbacklight -inc 5")),
    Key([], 'XF86MonBrightnessDown', lazy.spawn("xbacklight -dec 5")),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("pamixer -i 5")),
    Key([], 'XF86AudioLowerVolume', lazy.spawn("pamixer -d 5")),
    Key([], 'XF86AudioMute', lazy.spawn("pamixer -m")),
    Key([mod], 'XF86AudioMute', lazy.spawn("pamixer -u")),
]

groups = [Group(i) for i in '12345']

for i in groups:
    # ctrl + Fn of group = switch to group
    keys.append(
        Key(['control'], 'F' + i.name, lazy.group[i.name].toscreen())
    )
    # mod4 + Fn of group = switch to & move focused window to group
    keys.append(
        Key([mod], 'F' + i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.Columns(num_columns=3),
    layout.Matrix(),
    layout.xmonad.MonadTall()
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.CPUGraph(graph_color='FF3300', fill_color='#FF5500.3', line_width=1),
                widget.MemoryGraph(line_width=1),
                widget.NetGraph(graph_color='8CFF8C', fill_color='#8CFFC6.3', line_width=1),
                widget.BatteryIcon(),
                widget.Battery(format='{percent:2.0%}'),
                widget.Systray(),
                widget.Clock(format='%b %d %a %I:%M %p'),
            ],
            30,
                background=['#333333', '#000000']
        ),
        bottom=bar.Bar(
            [
                widget.WindowTabs(),
            ],
            30,
                background=['#000000', '#333333']
        )
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.CPUGraph(graph_color='FF3300', fill_color='#FF5500.3', line_width=1),
                widget.MemoryGraph(line_width=1),
                widget.NetGraph(graph_color='8CFF8C', fill_color='#8CFFC6.3', line_width=1),
                widget.BatteryIcon(),
                widget.Battery(format='{percent:2.0%}'),
                widget.Systray(),
                widget.Clock(format='%b %d %a %I:%M %p'),
            ],
            30,
                background=['#333333', '#000000']
        ),
        bottom=bar.Bar(
            [
                widget.WindowTabs(),
            ],
            30,
                background=['#000000', '#333333']
        )
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

