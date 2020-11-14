# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2017 Antonio Yang
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

from cpu import CPU
from memory import Memory

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
import subprocess
import re

IS_POK3R = None
try:
    AT_HOME = open("/tmp/screens").readlines()[0].startswith('home')
except:
    AT_HOME = False

# Detect keyboard type
device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<vender>\w+):(?P<id>\w+)\s(?P<tag>.+)$")

for device in subprocess.check_output("lsusb").decode().split("\n"):
    # Detect Pok3r
    if device_re.match(device):
        match = device_re.match(device)
        if match['vender'] == '04d9' and (
                match['tag'] == 'Holtek Semiconductor, Inc. USB-HID Keyboard'
                or match['tag'] == 'Holtek Semiconductor, Inc. USB Keyboard'):
            IS_POK3R = True
    if device_re.match(device):
        match = device_re.match(device)
        if match['vender'] == '05e3' and match['tag'] == 'Genesys Logic, Inc. Hub':
            IS_POK3R = True


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
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Utils
    Key([mod], "Escape", lazy.spawn('alacritty')),
    Key([mod], "l", lazy.spawn('pcmanfm')),
    Key([mod], "f", lazy.spawn('firefox')),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),
    Key(['control'], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key(["control"], "space", lazy.spawncmd()),

    Key([mod], "c", lazy.spawn("clipcat-menu")),
    Key([mod], "s", lazy.spawn("rofi -terminal alacritty -show ssh")),
    Key([mod], "w", lazy.spawn("rofi -show")),

    # Function keys
    # Hand on backlight for OLED screens
    # xrandr --output <output> --brightness .5 - dim to 50%
    Key([], 'XF86MonBrightnessUp', lazy.spawn("xbacklight -inc 5")),
    Key([], 'XF86MonBrightnessDown', lazy.spawn("xbacklight -dec 5")),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("pamixer -i 5")),
    Key([], 'XF86AudioLowerVolume', lazy.spawn("pamixer -d 5")),
    Key([], 'XF86AudioMute', lazy.spawn("pamixer -m")),
    Key([mod], 'XF86AudioMute', lazy.spawn("pamixer -u")),
]


if AT_HOME:
    for i in '1234':
        keys.append(Key(['control', 'mod1'], i, lazy.spawn('/home/yanganto/.usr/bin/move H' + i)))
else:
    for i in '12':
        keys.append(Key(['control', 'mod1'], i, lazy.spawn('/home/yanganto/.usr/bin/move O' + i)))

groups = [Group(i) for i in '12345']

for i in groups:
    # ctrl of group = switch to group
    keys.append(
        Key(['control'],
            i.name if IS_POK3R else 'F' + i.name,
            lazy.group[i.name].toscreen())
    )
    # mod4  of group = switch to & move focused window to group
    keys.append(
        Key([mod],
            i.name if IS_POK3R else 'F' + i.name,
            lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    layout.Matrix(),
    layout.xmonad.MonadTall(),
    layout.xmonad.MonadWide(),
]

widget_defaults = dict(
    font='Iosevka',
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
                CPU(),
                widget.CPUGraph(graph_color='FF3300', fill_color='#FF5500.3', line_width=1),
                Memory(),
                widget.MemoryGraph(line_width=1),
                widget.NetGraph(graph_color='8CFF8C', fill_color='#8CFFC6.3', line_width=1),
                widget.HDDBusyGraph(graph_color='FF00FF', fill_color='#FF00FF.3', line_width=1),
                widget.BatteryIcon(),
                widget.Battery(format='{percent:2.0%}'),
                widget.Systray(),
                widget.Clock(format='%b %d %a %I:%M:%S %p')
            ],
            30,
            background=['#333333', '#000000']
        ),
        bottom=bar.Bar(
            [
                widget.WindowTabs(),
                widget.Notify(default_timeout=10, background="#8B0000"),
                widget.CurrentLayout()
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
                CPU(),
                widget.CPUGraph(graph_color='FF3300', fill_color='#FF5500.3', line_width=1),
                Memory(),
                widget.MemoryGraph(line_width=1),
                widget.NetGraph(graph_color='8CFF8C', fill_color='#8CFFC6.3', line_width=1),
                widget.HDDBusyGraph(graph_color='FF00FF', fill_color='#FF00FF.3', line_width=1),
                widget.BatteryIcon(),
                widget.Battery(format='{percent:2.0%}'),
                widget.Systray(),
                widget.Clock(format='%b %d %a %I:%M %p')
            ],
            30,
            background=['#333333', '#000000']
        ),
        bottom=bar.Bar(
            [
                widget.WindowTabs(),
                widget.Notify(default_timeout=10, background="#8B0000"),
                widget.CurrentLayout()
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
                CPU(),
                widget.CPUGraph(graph_color='FF3300', fill_color='#FF5500.3', line_width=1),
                Memory(),
                widget.MemoryGraph(line_width=1),
                widget.NetGraph(graph_color='8CFF8C', fill_color='#8CFFC6.3', line_width=1),
                widget.HDDBusyGraph(graph_color='FF00FF', fill_color='#FF00FF.3', line_width=1),
                widget.BatteryIcon(),
                widget.Battery(format='{percent:2.0%}'),
                widget.Systray(),
                widget.Clock(format='%b %d %a %I:%M %p')
            ],
            30,
            background=['#333333', '#000000']
        ),
        bottom=bar.Bar(
            [
                widget.WindowTabs(),
                widget.Notify(default_timeout=10, background="#8B0000"),
                widget.CurrentLayout()
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
                #CPU(),
                #widget.CPUGraph(graph_color='FF3300', fill_color='#FF5500.3', line_width=1),
                #Memory(),
                #widget.MemoryGraph(line_width=1),
                # widget.NetGraph(graph_color='8CFF8C', fill_color='#8CFFC6.3', line_width=1),
                # widget.HDDBusyGraph(graph_color='FF00FF', fill_color='#FF00FF.3', line_width=1),
                widget.BatteryIcon(),
                widget.Battery(format='{percent:2.0%}'),
                widget.Systray(),
                widget.Clock(format='%b %d %a %I:%M %p')
            ],
            30,
            background=['#333333', '#000000']
        ),
        bottom=bar.Bar(
            [
                widget.WindowTabs(),
                widget.Notify(default_timeout=10, background="#8B0000"),
                widget.CurrentLayout()
            ],
            30,
            background=['#000000', '#333333']
        )
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
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
subprocess.run(["clipcatd"])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
